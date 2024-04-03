import * as vscode from 'vscode';
import { createSession } from './client';
import path from 'path';

export async function sessionStart(
  context: vscode.ExtensionContext,
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

    const activeCode = activeEditor.document.getText();
    console.log('Active code:', activeCode);
    const currentFile = activeEditor.document.fileName;
    console.log('Current file:', currentFile);

    vscode.commands.executeCommand('vscode.editorChat.start');

    const { session_id } = await createSession(activeCode);
    context.workspaceState.update(`${currentFile}`, session_id);

    vscode.window.showInformationMessage(
      'Successfully activated the completion verifier! Now go ahead and prompt Copilot to complete some code.'
    );

    setTimeout(() => callback(), 1000);
  }
}
