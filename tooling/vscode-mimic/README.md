# mimic for VS Code

Right-click any screenshot in the Explorer → **mimic: Generate** → pick a framework. Generated files open in the editor seconds later.

Wraps the [mimic](https://github.com/Cyber-Lord/mimic) CLI. Requires `mimic` on your PATH (or set `mimic.binaryPath` in settings).

## Install

```bash
pip install mimic-cli
```

Then install this extension from the marketplace, or build locally:

```bash
cd tooling/vscode-mimic
npm install
npm run package
code --install-extension vscode-mimic-*.vsix
```

## Commands

| Command                                    | What it does                                       |
| ------------------------------------------ | -------------------------------------------------- |
| `mimic: Generate from screenshot…`          | Pick image + target, generates code                |
| `mimic: Generate Flutter from this screenshot` | Right-click context menu on PNG/JPG             |
| `mimic: Generate HTML from this screenshot`    | Same, HTML target                                |
| `mimic: Generate React from this screenshot`   | Same, React target                               |
| `mimic: Doctor`                                | Run `mimic doctor` in the output panel           |

## Configuration

- `mimic.binaryPath` — path to the `mimic` CLI (default: `mimic` from PATH)
- `mimic.defaultTarget` — `flutter` (default), `html`, or `react`
- `mimic.defaultProvider` — `claude`, `openai`, or `mock:<fixture>` for offline use
- `mimic.outputDirectory` — where generated files go. Supports `${workspaceFolder}`.

## License

MIT — same as the parent project.
