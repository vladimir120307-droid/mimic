import json
import socket
import threading
import time
import urllib.request
from contextlib import contextmanager

import pytest

from mimic.server import serve


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@contextmanager
def running_server():
    port = _free_port()
    thread = threading.Thread(
        target=serve, kwargs={"host": "127.0.0.1", "port": port}, daemon=True
    )
    thread.start()
    for _ in range(20):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.1).close()
            break
        except OSError:
            time.sleep(0.05)
    yield port


def _rpc(port: int, method: str, params: dict | None = None):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/",
        data=json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
        ).encode(),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read())


@pytest.mark.timeout(10)
def test_server_responds_to_version():
    with running_server() as port:
        result = _rpc(port, "version")
        assert "result" in result
        assert isinstance(result["result"], str)


@pytest.mark.timeout(10)
def test_server_lists_targets():
    with running_server() as port:
        result = _rpc(port, "list_targets")
        assert "flutter" in result["result"]
        assert "html" in result["result"]
        assert "react" in result["result"]


@pytest.mark.timeout(10)
def test_server_unknown_method_returns_error():
    with running_server() as port:
        result = _rpc(port, "no_such_method")
        assert "error" in result
        assert result["error"]["code"] == -32601


@pytest.mark.timeout(10)
def test_server_gen_works_with_mock(tmp_path):
    img = tmp_path / "x.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")
    with running_server() as port:
        result = _rpc(
            port,
            "gen",
            {
                "image_path": str(img),
                "target":     "html",
                "provider":   "mock:login",
            },
        )
        assert "result" in result, result
        files = result["result"]["files"]
        assert any(f["path"] == "index.html" for f in files)
