import { exec } from 'node:child_process';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { promisify } from 'node:util';
import * as vscode from 'vscode';

const execP = promisify(exec);
type Target = 'flutter' | 'html' | 'react';

export function activate(context: vscode.ExtensionContext): void {
  const register = (command: string, handler: (uri?: vscode.Uri) => Promise<void>) => {
    context.subscriptions.push(vscode.commands.registerCommand(command, handler));
  };

  register('mimic.generate',         (uri) => generate(uri, undefined));
  register('mimic.generateFlutter',  (uri) => generate(uri, 'flutter'));
  register('mimic.generateHtml',     (uri) => generate(uri, 'html'));
  register('mimic.generateReact',    (uri) => generate(uri, 'react'));
  register('mimic.doctor',           () => doctor());
}

export function deactivate(): void {
  /* no-op */
}

async function generate(uri: vscode.Uri | undefined, target: Target | undefined): Promise<void> {
  const cfg = vscode.workspace.getConfiguration('mimic');
  const bin       = cfg.get<string>('binaryPath',       'mimic');
  const provider  = cfg.get<string>('defaultProvider',  'claude');
  const defTarget = cfg.get<string>('defaultTarget',    'flutter') as Target;
  const outPattern = cfg.get<string>('outputDirectory', '${workspaceFolder}/mimic-output');

  const imagePath = await resolveImagePath(uri);
  if (!imagePath) {
    return;
  }
  const chosenTarget: Target =
    target ?? ((await pickTarget(defTarget)) || defTarget);

  const outDir = await resolveOutputDir(outPattern, chosenTarget, imagePath);

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title:    `mimic → ${chosenTarget}`,
      cancellable: false,
    },
    async (progress) => {
      progress.report({ message: 'Calling vision model…' });
      const cmd =
        `"${bin}" gen "${imagePath}" --provider "${provider}" ` +
        `--target ${chosenTarget} --out "${outDir}"`;
      try {
        const { stdout } = await execP(cmd, { maxBuffer: 16 * 1024 * 1024 });
        progress.report({ message: 'Opening result…' });
        await openFirstGenerated(outDir, chosenTarget);
        vscode.window.showInformationMessage(`mimic: generated in ${outDir}`);
        if (stdout) {
          getOutputChannel().appendLine(stdout);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        getOutputChannel().appendLine(`ERROR: ${message}`);
        vscode.window.showErrorMessage(
          `mimic failed. Run "mimic doctor" or open the mimic output panel for details.`
        );
      }
    }
  );
}

async function doctor(): Promise<void> {
  const cfg = vscode.workspace.getConfiguration('mimic');
  const bin = cfg.get<string>('binaryPath', 'mimic');
  const ch  = getOutputChannel();
  ch.show(true);
  try {
    const { stdout } = await execP(`"${bin}" doctor`);
    ch.appendLine(stdout);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    ch.appendLine(`mimic doctor failed: ${message}`);
    ch.appendLine(`\nIs mimic installed? Try: pip install mimic-cli`);
  }
}

async function resolveImagePath(uri: vscode.Uri | undefined): Promise<string | undefined> {
  if (uri && uri.scheme === 'file') return uri.fsPath;

  const picked = await vscode.window.showOpenDialog({
    canSelectFiles: true,
    canSelectMany:  false,
    title:          'Pick a screenshot for mimic',
    filters:        { Images: ['png', 'jpg', 'jpeg', 'webp'] },
  });
  return picked && picked.length > 0 ? picked[0].fsPath : undefined;
}

async function pickTarget(initial: Target): Promise<Target | undefined> {
  const items: vscode.QuickPickItem[] = [
    { label: 'flutter', description: 'Material 3 Flutter app'  },
    { label: 'html',    description: 'Single-file Tailwind page' },
    { label: 'react',   description: 'Vite project, react-router'  },
  ];
  const choice = await vscode.window.showQuickPick(items, {
    title:       'mimic: which framework?',
    placeHolder: initial,
  });
  return choice ? (choice.label as Target) : undefined;
}

async function resolveOutputDir(
  pattern: string,
  target: Target,
  imagePath: string
): Promise<string> {
  const ws = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? path.dirname(imagePath);
  const base = pattern.replace('${workspaceFolder}', ws);
  const stamp = path.basename(imagePath, path.extname(imagePath));
  const dir = path.join(base, `${stamp}-${target}`);
  await fs.mkdir(dir, { recursive: true });
  return dir;
}

async function openFirstGenerated(outDir: string, target: Target): Promise<void> {
  const heroFile = ({
    flutter: 'lib/screens',
    html:    'index.html',
    react:   'src/App.jsx',
  } as Record<Target, string>)[target];

  const candidate = path.join(outDir, heroFile);
  try {
    const stat = await fs.stat(candidate);
    if (stat.isDirectory()) {
      const entries = await fs.readdir(candidate);
      if (entries.length === 0) return;
      await vscode.window.showTextDocument(
        vscode.Uri.file(path.join(candidate, entries[0]))
      );
    } else {
      await vscode.window.showTextDocument(vscode.Uri.file(candidate));
    }
  } catch {
    /* file may not exist yet — skip silently */
  }
}

let _channel: vscode.OutputChannel | undefined;
function getOutputChannel(): vscode.OutputChannel {
  if (!_channel) {
    _channel = vscode.window.createOutputChannel('mimic');
  }
  return _channel;
}
