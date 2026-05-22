"""Local JSON-RPC server the Flutter desktop UI talks to.

Listens on 127.0.0.1 by default. Methods:

- `start_recording(duration_s: int) -> {ok: true}`
- `stop_and_generate(target?: str, provider?: str) -> {files: [...]}`
- `gen(image_path: str, target: str, provider: str) -> {files: [...]}`
- `list_displays() -> [...]`
- `version() -> str`

Wire format is JSON-RPC 2.0. Use `mimic serve` to start.
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from mimic import __version__
from mimic.codegen import list_targets
from mimic.pipeline import Pipeline
from mimic.vision.base import VisionInput

log = logging.getLogger("mimic.server")


@dataclass
class ServerState:
    capture_task: asyncio.Task[Any] | None = None
    captured_frames: list[Any] | None = None
    last_target: str = "flutter"
    last_provider: str = "mock:dashboard"


class _Handler(BaseHTTPRequestHandler):
    state: ServerState
    loop: asyncio.AbstractEventLoop

    def log_message(self, fmt: str, *args: Any) -> None:
        log.info("%s - %s", self.address_string(), fmt % args)

    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            envelope = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send_error(-32700, "Parse error")
            return

        method = envelope.get("method")
        params = envelope.get("params") or {}
        rid = envelope.get("id")

        if not isinstance(method, str):
            self._send_error(-32600, "Invalid request: method missing", rid)
            return

        try:
            result = self._dispatch(method, params)
        except _RpcError as e:
            self._send_error(e.code, e.message, rid)
            return
        except Exception as exc:
            log.exception("Unhandled error in method %s", method)
            self._send_error(-32603, f"Internal error: {exc!s}", rid)
            return

        self._send_result(result, rid)

    def _dispatch(self, method: str, params: dict[str, Any]) -> Any:
        if method == "version":
            return __version__
        if method == "list_targets":
            return list(list_targets())
        if method == "list_displays":
            from mimic.capture import list_displays
            return [
                {
                    "index":      d.index,
                    "name":       d.name,
                    "bounds":     d.bounds,
                    "dpi_scale":  d.dpi_scale,
                    "is_primary": d.is_primary,
                }
                for d in list_displays()
            ]
        if method == "start_recording":
            return self._start_recording(int(params.get("duration_s", 15)))
        if method == "stop_and_generate":
            return self._stop_and_generate(
                target=params.get("target") or self.state.last_target,
                provider=params.get("provider") or self.state.last_provider,
            )
        if method == "gen":
            image_path = params.get("image_path")
            if not isinstance(image_path, str):
                raise _RpcError(-32602, "Invalid params: image_path required")
            return self._gen_from_image(
                image=Path(image_path),
                target=params.get("target", "flutter"),
                provider=params.get("provider", "claude"),
            )
        raise _RpcError(-32601, f"Method not found: {method}")

    def _start_recording(self, duration_s: int) -> dict[str, Any]:
        if self.state.capture_task and not self.state.capture_task.done():
            raise _RpcError(-32000, "A recording is already in progress")

        async def go() -> list[Any]:
            from mimic.capture import record_screen
            return await asyncio.get_running_loop().run_in_executor(
                None, record_screen, duration_s
            )

        self.state.capture_task = asyncio.run_coroutine_threadsafe(  # type: ignore[assignment]
            go(), self.loop
        )
        return {"ok": True, "duration_s": duration_s}

    def _stop_and_generate(self, target: str, provider: str) -> dict[str, Any]:
        task = self.state.capture_task
        if task is None:
            raise _RpcError(-32000, "No recording started")
        frames = task.result(timeout=60)  # type: ignore[attr-defined]
        self.state.captured_frames = frames
        self.state.last_target = target
        self.state.last_provider = provider

        source = VisionInput.from_frames(frames)
        result = asyncio.run_coroutine_threadsafe(
            Pipeline(provider=provider, target=target).run(source), self.loop
        ).result(timeout=120)

        self.state.capture_task = None
        return _result_payload(result.files)

    def _gen_from_image(self, image: Path, target: str, provider: str) -> dict[str, Any]:
        if not image.exists():
            raise _RpcError(-32602, f"image_path not found: {image}")
        source = VisionInput.from_image(image)
        result = asyncio.run_coroutine_threadsafe(
            Pipeline(provider=provider, target=target).run(source), self.loop
        ).result(timeout=120)
        return _result_payload(result.files)

    def _send_result(self, result: Any, rid: Any) -> None:
        body = json.dumps({"jsonrpc": "2.0", "id": rid, "result": result}).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, code: int, message: str, rid: Any = None) -> None:
        body = json.dumps(
            {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}}
        ).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class _RpcError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _result_payload(files: list[Any]) -> dict[str, Any]:
    return {
        "files": [
            {"path": f.path, "content": f.content, "language": f.language}
            for f in files
        ]
    }


def serve(host: str = "127.0.0.1", port: int = 54321) -> None:
    """Run the JSON-RPC server forever. Blocks the calling thread."""
    state = ServerState()

    loop = asyncio.new_event_loop()
    executor = ThreadPoolExecutor(max_workers=2)
    loop.set_default_executor(executor)
    loop_thread = threading.Thread(
        target=lambda: (asyncio.set_event_loop(loop), loop.run_forever()),
        daemon=True,
        name="mimic-rpc-loop",
    )
    loop_thread.start()

    handler_cls = type(
        "MimicHandler", (_Handler,), {"state": state, "loop": loop}
    )

    httpd = ThreadingHTTPServer((host, port), handler_cls)
    log.info("mimic RPC server listening on %s:%d", host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        loop.call_soon_threadsafe(loop.stop)


def _b64_encode_str(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")
