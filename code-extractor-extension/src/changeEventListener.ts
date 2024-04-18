import * as vscode from 'vscode';
import { handleVerify } from './verification/handleVerification';
import { VerifierClient } from './client';
import { debounce } from './util/debounce';

const handleDebouncedChangeEvent = async (
  selfDisposable: vscode.Disposable,
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient,
  saveResults: boolean
) => {
  console.log('Spawining Info Message');

  const sessionId = context.workspaceState.get<string>(
    vscode?.window?.activeTextEditor?.document?.fileName ?? 'aaaa'
  );

  if (sessionId) {
    const selection = await vscode.window.showInformationMessage(
      'It seems like a completion was generated - do you want to verify it?',
      'Yes',
      'No'
    );
    if (selection === 'Yes') {
      await handleVerify(context, verifierClient, saveResults);
    } else if (selection === 'No') {
      vscode.window.showInformationMessage(
        'Okay, session ended. You can start a new session anytime!'
      );
      if (vscode.window?.activeTextEditor?.document?.fileName)
        context.workspaceState.update(
          vscode.window?.activeTextEditor?.document?.fileName,
          undefined
        );
      selfDisposable.dispose();
    }
  }
};

export function setupDebouncedChangeListener(
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient,
  debounceTime: number,
  saveResults: boolean
) {
  let changeTextEditorSelection =
    vscode.window.onDidChangeTextEditorSelection(
      debounce(
        async () =>
          await handleDebouncedChangeEvent(
            changeTextEditorSelection,
            context,
            verifierClient,
            saveResults
          ),
        debounceTime
      )
    );
  context.subscriptions.push(changeTextEditorSelection);
}
