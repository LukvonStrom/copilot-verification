import * as vscode from 'vscode';
import { createSession } from './client';
import path from 'path';

export async function sessionStart(
  context: vscode.ExtensionContext,
  checkDiagnosticsCallback: (
    document: vscode.TextDocument
  ) => Promise<vscode.DiagnosticCollection | undefined>,
  callback: () => void
) {
  const activeEditor = vscode.window.activeTextEditor;
  console.log('Active editor:', activeEditor);
  if (activeEditor) {
    if (activeEditor.document.languageId !== 'python') {
      vscode.window.showErrorMessage(
        'This is not a python file - this verifier only works with a Python file!'
      );
      return;
    }

    checkDiagnosticsCallback(activeEditor.document).then(
      (diagCollection) => {
        if (
          diagCollection &&
          diagCollection.has(activeEditor.document.uri)
        ) {
          vscode.window.showErrorMessage(
            `Asserts missing for Crosshair - I annotated the occurences in the current file.`
          );
        }
      }
    );

    const activeCode = activeEditor.document.getText();
    console.log('Active code:', activeCode);

    vscode.commands.executeCommand('vscode.editorChat.start');

    const { session_id } = await createSession(activeCode);
    context.workspaceState.update(activeEditor.document.fileName, session_id);

    vscode.window.showInformationMessage(
      'Successfully activated the completion verifier! Now go ahead and prompt Copilot to complete some code.'
    );

    setTimeout(() => callback(), 1000);
  }
}
