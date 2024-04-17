import * as vscode from 'vscode';
import { VerifierClient } from './client';
import { checkDiagnostics } from './diagnostics/diagnostics';

async function handleDiagnostics(
  activeDocument: vscode.TextDocument | undefined,
  diagnosticCollection: vscode.DiagnosticCollection,
  verifierClient: VerifierClient
) {
  const diagCollection = await checkDiagnostics(
    activeDocument,
    diagnosticCollection,
    verifierClient
  );

  if (
    activeDocument &&
    diagCollection &&
    diagCollection.has(activeDocument.uri)
  ) {
    vscode.window.showErrorMessage(
      `Asserts missing for Crosshair - I annotated the occurrences in the current file.`
    );
  }
}

async function startEditorChat() {
  await vscode.commands.executeCommand('vscode.editorChat.start');
}

async function createVerifierSession(
  activeCode: string,
  activeFileName: string,
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient
) {
  try {
    const { session_id } = await verifierClient.createSession(
      activeCode
    );
    await context.workspaceState.update(activeFileName, session_id);
  } catch (e: any) {
    vscode.window.showErrorMessage(e.message);
  }
}

export async function sessionStart(
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient,
  diagnosticCollection: vscode.DiagnosticCollection,
  callback: () => void
) {
  const activeEditor = vscode.window.activeTextEditor;
  const activeDocument = activeEditor?.document;
  const activeCode = activeDocument?.getText() ?? '';
  const activeFileName = activeDocument?.fileName ?? 'unknown-file';

  await handleDiagnostics(
    activeDocument,
    diagnosticCollection,
    verifierClient
  );
  await createVerifierSession(
    activeCode,
    activeFileName,
    context,
    verifierClient
  );
  await startEditorChat();

  vscode.window.showInformationMessage(
    'Successfully activated the completion verifier! Now go ahead and prompt Copilot to complete some code.'
  );

  setTimeout(() => callback(), 1000);
}
