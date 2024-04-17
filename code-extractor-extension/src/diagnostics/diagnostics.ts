import * as vscode from 'vscode';
import { VerifierClient } from '../client';

export async function checkDiagnostics(
  document: vscode.TextDocument | undefined,
  diagnosticCollection: vscode.DiagnosticCollection,
  verifierClient: VerifierClient
) {
  if (!document) {
    return;
  }

  if (document.languageId !== 'python') {
    return;
  }
  if (diagnosticCollection.has(document.uri)) {
    diagnosticCollection.delete(document.uri);
  }
  try {
    const diagnosticResponse =
      await verifierClient.fetchDiagnosticsForAsserts(
        document.getText(),
        document.fileName
      );
    console.log('Got', diagnosticResponse);

    // Set the diagnostics for this document in the collection
    diagnosticCollection.set(
      document.uri,
      diagnosticResponse.params.diagnostics
    );

    return diagnosticCollection;
  } catch (e: any) {
    vscode.window.showErrorMessage(e.message);
    return;
  }
}
