import * as vscode from 'vscode';
import { VerifierClient } from './client';
import { checkDiagnostics } from './diagnostics/diagnostics';
import { setupDebouncedChangeListener } from './changeEventListener';
import { sessionStart } from './session-start';
import { handleVerify } from './verification/handleVerification';

export async function activateExtension(
  context: vscode.ExtensionContext
) {
  console.log(
    'Congratulations, your extension "completion-verifier" is now active!'
  );

  const backendUri =
    vscode.workspace
      .getConfiguration()
      .get<string>('llmverifier.apiBackendUri') ??
    'http://localhost:8000';

  const debounceTime =
    vscode.workspace
      .getConfiguration()
      .get<number>('llmverifier.debounceTime') ?? 3500;

  const saveResults =
    vscode.workspace
      .getConfiguration()
      .get<boolean>('llmverifier.saveResults') ?? true;

  console.log('Config', { backendUri, debounceTime, saveResults });

  const verifierClient = new VerifierClient(backendUri);
  const diagnosticCollection =
    vscode.languages.createDiagnosticCollection('assertCheck');

  context.subscriptions.push(diagnosticCollection);

  const wrappedCheckDiagnostics = async (
    document: vscode.TextDocument
  ) =>
    await checkDiagnostics(
      document,
      diagnosticCollection,
      verifierClient
    );

  // Subscribe to text document open and save events to update diagnostics
  context.subscriptions.push(
    vscode.workspace.onDidOpenTextDocument(wrappedCheckDiagnostics)
  );
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(wrappedCheckDiagnostics)
  );

  const completionVerifierEventEmitter =
    new vscode.EventEmitter<void>();

  // Expose the event
  const completionVerifierEvent =
    completionVerifierEventEmitter.event;

  let completionCommandDisposable = vscode.commands.registerCommand(
    'completion-verifier.startCompletionVerifier',
    () =>
      sessionStart(
        context,
        verifierClient,
        diagnosticCollection,
        () => completionVerifierEventEmitter.fire()
      )
  );
  context.subscriptions.push(completionCommandDisposable);

  let forceValidateCommandDisposable =
    vscode.commands.registerCommand(
      'completion-verifier.forceVerify',
      () => {
        const sessionId = context.workspaceState.get<string>(
          vscode?.window?.activeTextEditor?.document?.fileName ??
            'aaaa'
        );
        if (!sessionId) {
          sessionStart(
            context,
            verifierClient,
            diagnosticCollection,
            () => completionVerifierEventEmitter.fire()
          );
        }
        handleVerify(context, verifierClient, saveResults);
      }
    );
  context.subscriptions.push(forceValidateCommandDisposable);

  // Attach the listener to the custom event
  context.subscriptions.push(
    completionVerifierEvent(() =>
      setupDebouncedChangeListener(
        context,
        verifierClient,
        debounceTime,
        saveResults
      )
    )
  );

  // Initial check for already open documents
  await Promise.allSettled(
    vscode.workspace.textDocuments.map((doc: vscode.TextDocument) =>
      wrappedCheckDiagnostics(doc)
    )
  );
}
