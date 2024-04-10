import * as vscode from 'vscode';
import {
  augmentSession,
  createSession,
  fetchDiagnosticsForAsserts,
} from './client';
import path from 'path';
import { sessionStart } from './extension-logic';
import { ToolOutput } from './types';
import { clear } from 'console';

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

  const diagnosticCollection =
    vscode.languages.createDiagnosticCollection('assertCheck');

  // Subscribe to text document open and save events to update diagnostics
  context.subscriptions.push(
    vscode.workspace.onDidOpenTextDocument(checkDiagnostics)
  );
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(checkDiagnostics)
  );

  async function checkDiagnostics(document: vscode.TextDocument) {
    if (document.languageId !== 'python') {
      return;
    }
    if (diagnosticCollection.has(document.uri)) {
      diagnosticCollection.delete(document.uri);
    }
    const diagnosticResponse = await fetchDiagnosticsForAsserts(
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
  }

  // Initial check for already open documents
  vscode.workspace.textDocuments.map((doc: vscode.TextDocument) =>
    checkDiagnostics(doc)
  );

  const completionVerifierEventEmitter =
    new vscode.EventEmitter<void>();

  // Expose the event
  const completionVerifierEvent =
    completionVerifierEventEmitter.event;

  let completionCommandDisposable = vscode.commands.registerCommand(
    'completion-verifier.startCompletionVerifier',
    () =>
      sessionStart(context, checkDiagnostics, () =>
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

  const handleVerify = async () => {
    console.log('window state', vscode.window.state);
    console.log('text editor', vscode.window.activeTextEditor);
    console.log(vscode.window.activeTextEditor?.document.getText());
    const sessionId = context.workspaceState.get<string>(
      vscode?.window?.activeTextEditor?.document?.fileName ?? 'aaaa'
    );
    if (!sessionId) {
      vscode.window.showErrorMessage(
        'I am not aware of any session for this file. Please start a session first!'
      );
      return;
    }

    let tooloutput: ToolOutput;

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

        tooloutput = (await augmentSession(
          sessionId,
          vscode.window.activeTextEditor?.document.getText()
        )) as ToolOutput;
        clearInterval(interval);
        progress.report({ increment: 100 });

        const completedBothProspector =
          tooloutput.prospector_valid[0] &&
          tooloutput.prospector_valid[1];
        const completedBothCrosshair =
          tooloutput.crosshair_valid[0] &&
          tooloutput.crosshair_valid[1];

        const outputMarkdown = `# Completion Verifier Output
    
| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ${
          tooloutput.prospector_valid[0] ? '✅' : '❌'
        } | ${tooloutput.prospector_valid[1] ? '✅' : '❌'} |
| Crosshair (Symbolic Execution) | ${
          tooloutput.crosshair_valid[0] ? '✅' : '❌'
        } | ${tooloutput.crosshair_valid[1] ? '✅' : '❌'} |


## Prospector Output
${
  completedBothProspector
    ? '🎉🎉🎉 Congratulations! No Prospector remarks! 🎉🎉🎉'
    : `### Before Completion
\`\`\`
${JSON.stringify(tooloutput.prospector_output[0], null, 2)}
\`\`\`
### After Completion
\`\`\`
${JSON.stringify(tooloutput.prospector_output[1], null, 2)}
\`\`\`
`
}


## Crosshair Output
### Before Completion
\`\`\`
${JSON.stringify(tooloutput.crosshair_output[0], null, 2)}
\`\`\`
### After Completion
\`\`\`
${JSON.stringify(tooloutput.crosshair_output[1], null, 2)}
\`\`\`
`;

        // Open a new text document with markdown content
        const document = await vscode.workspace.openTextDocument({
          content: outputMarkdown,
          language: 'markdown',
        });

        // Execute the command to show markdown preview
        await vscode.commands.executeCommand(
          'markdown.showPreview',
          document.uri
        );
      }
    );
  };

  function setupDebouncedChangeListener() {
    let changeTextEditorSelection =
      vscode.window.onDidChangeTextEditorSelection(
        debounce(async () => {
          console.log('Spawining Info Message');
          const selection =
            await vscode.window.showInformationMessage(
              'It seems like a completion was generated - do you want to verify it?',
              'Yes',
              'No'
            );
          if (selection === 'Yes') {
            await handleVerify();
          } else {
            vscode.window.showInformationMessage(
              'Okay, session ended. You can start a new session anytime!'
            );
            if (vscode.window?.activeTextEditor?.document?.fileName)
              context.workspaceState.update(
                vscode.window?.activeTextEditor?.document?.fileName,
                undefined
              );
            changeTextEditorSelection.dispose();
          }
        }, 3555)
      );

    context.subscriptions.push(changeTextEditorSelection);
  }

  // Attach the listener to the custom event
  context.subscriptions.push(
    completionVerifierEvent(setupDebouncedChangeListener)
  );
}

// This method is called when your extension is deactivated
export function deactivate() {}
