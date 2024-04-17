import * as vscode from 'vscode';
import { ToolOutput } from '../types';
import { VerifierClient } from '../client';
import path from 'path';

export const handleVerify = async (
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient,
  saveResults: boolean
) => {
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

  const handleVerifyCallback = async (
    progress: vscode.Progress<{
      message?: string | undefined;
      increment?: number | undefined;
    }>,
    token: vscode.CancellationToken
  ) => {
    progress.report({ increment: 0 });
    let prog = 0;
    const interval = setInterval(() => {
      progress.report({ increment: 10 });
      prog += 10;
      if (prog >= 80) {
        clearInterval(interval);
      }
    }, 500);
    try {
      tooloutput = (await verifierClient.augmentSession(
        sessionId,
        vscode.window.activeTextEditor?.document.getText()
      )) as ToolOutput;
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

      let document: vscode.TextDocument | undefined;

      if (saveResults) {
        const fullPath =
          vscode.window.activeTextEditor?.document.fileName;
        if (fullPath) {
          const directory = path.dirname(fullPath);
          const filenameWithoutExtension = path.basename(
            fullPath,
            path.extname(fullPath)
          );
          const newFilename = `${filenameWithoutExtension}-results.md`;
          const newFilePath = path.join(directory, newFilename);
          const uri = vscode.Uri.file(newFilePath);
          await vscode.workspace.fs.writeFile(
            uri,
            new TextEncoder().encode(outputMarkdown)
          );

          document = await vscode.workspace.openTextDocument(uri);
        }
      } else {
        document = await vscode.workspace.openTextDocument({
          content: outputMarkdown,
          language: 'markdown',
        });
      }
      if (!document) {
        return;
      }

      // Execute the command to show markdown preview
      await vscode.commands.executeCommand(
        'markdown.showPreview',
        document.uri
      );
    } catch (e: any) {
      vscode.window.showErrorMessage(e.message);
    } finally {
      clearInterval(interval);
      progress.report({ increment: 100 });
    }
  };

  vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: 'Verifying completion...',
      cancellable: false,
    },
    handleVerifyCallback
  );
};
