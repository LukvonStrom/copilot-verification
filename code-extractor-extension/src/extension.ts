import * as vscode from 'vscode';
import { augmentSession, createSession } from './client';
import path from 'path';
import { sessionStart } from './extension-logic';

function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return (...args: Parameters<T>) => {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout !== null) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

export function activate(context: vscode.ExtensionContext) {
  console.log(
    'Congratulations, your extension "completion-verifier" is now active!'
  );

  const completionVerifierEventEmitter =
    new vscode.EventEmitter<void>();

  // Expose the event
  const completionVerifierEvent =
    completionVerifierEventEmitter.event;

  let completionCommandDisposable = vscode.commands.registerCommand(
    'completion-verifier.startCompletionVerifier',
    () =>
      sessionStart(context, () =>
        completionVerifierEventEmitter.fire()
      )
  );
  context.subscriptions.push(completionCommandDisposable);

  // context.subscriptions.push(
  //   // vscode.window.onDidChangeActiveTextEditor((editor) => console.log('onDidChangeActiveTextEditor:', editor)),
  //   // vscode.window.onDidChangeWindowState((state) => console.log('onDidChangeWindowState:', state)),

  //   // vscode.workspace.onDidChangeTextDocument((event) => console.log('onDidChangeTextDocument:', event)),
  //   // vscode.extensions.onDidChange((event) => console.log('onDidChangeExtensions:', event)),
  //   // vscode.workspace.onWillSaveTextDocument((event) => console.log('onWillSaveTextDocument:', event)),
  // );

  function setupDebouncedChangeListener() {
    let changeTextEditorSelection =
      vscode.window.onDidChangeTextEditorSelection(
        debounce(
          async (event: vscode.TextEditorSelectionChangeEvent) => {
            console.log('onDidChangeTextEditorSelection:', event);
            console.log(
              vscode.window.activeTextEditor?.document.getText()
            );
            const sessionId = context.workspaceState.get<string>(
              vscode?.window?.activeTextEditor?.document?.fileName ??
                'aaaa'
            );
            if (!sessionId) {
              vscode.window.showErrorMessage(
                'I am not aware of any session for this file. Please start a session first!'
              );
              return;
            }

            vscode.window.withProgress(
              {
                location: vscode.ProgressLocation.Notification,
                title: 'Verifying completion...',
                cancellable: false,
              },
              async (progress, token) => {
                progress.report({ increment: 0 });
                let prog = 0;
                const interval = setInterval(() => {
                  progress.report({ increment: 10 });
                  prog += 10;
                  if (prog >= 80) {
                    clearInterval(interval);
                  }
                }, 500);

                await augmentSession(
                  sessionId,
                  vscode.window.activeTextEditor?.document.getText()
                );
                progress.report({ increment: 100 });
              }
            );
          },
          2000
        )
      );

    context.subscriptions.push(changeTextEditorSelection);
  }

  // Attach the listener to the custom event
  context.subscriptions.push(completionVerifierEvent(setupDebouncedChangeListener));

  
}

// This method is called when your extension is deactivated
export function deactivate() {}
