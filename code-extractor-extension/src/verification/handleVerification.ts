import * as vscode from 'vscode';
import { ToolOutput } from '../types';
import { VerifierClient } from '../client';
import path from 'path';

type ProspectorLocation = {
  character: number;
  function: string | null;
  line: number;
  module: string | null;
  path: string;
};

type ProspectorMessage = {
  code: string;
  location: ProspectorLocation;
  message: string;
  source: string;
};

type ProspectorSummary = {
  completed: string;
  formatter: string;
  libraries: string[];
  message_count: number;
  profiles: string;
  started: string;
  strictness: string;
  time_taken: number;
  tools: string[];
};

// Function to create a Markdown table of error messages
function generateMarkdownTable(
  messages: ProspectorMessage[]
): string {
  let markdown = `| Code | Line | Message | Source |\n| ---- | ---- | ------- | ------ |\n`;
  messages.forEach((msg) => {
    markdown += `| ${msg.code} | ${
      msg.location.line
    } | ${msg.message.replace('\n', ' ')} | ${msg.source.replace(
      '\n',
      ' '
    )} |\n`;
  });
  return markdown;
}

export const handleVerify = async (
  context: vscode.ExtensionContext,
  verifierClient: VerifierClient,
  saveResults: boolean
) => {
  const startTime = process.hrtime();

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

      console.log('-----------------------------------');
      console.log('Tool Output:', tooloutput);
      console.log('-----------------------------------');
      const completedBothProspector =
        tooloutput.prospector_valid[0] &&
        tooloutput.prospector_valid[1];
      const completedBothCrosshair =
        tooloutput.crosshair_valid[0] &&
        tooloutput.crosshair_valid[1];

      const hrend = process.hrtime(startTime);
      const elapsedTime = hrend[0] + hrend[1] / Math.pow(10, 9);

      const outputMarkdown = `# Completion Verifier Output

| Tool | Passed Before Completion | Passed After Completion |
|---|---|---|
| Prospector (Code Quality) | ${
        tooloutput.prospector_valid[0] &&
        tooloutput.prospector_output[0].messages.length < 1
          ? '✅'
          : '❌'
      } | ${
        tooloutput.prospector_valid[1] &&
        tooloutput.prospector_output[1].messages.length < 1
          ? '✅'
          : '❌'
      } |
| Crosshair (Symbolic Execution) | ${
        tooloutput.crosshair_valid[0] ? '✅' : '❌'
      } | ${tooloutput.crosshair_valid[1] ? '✅' : '❌'} |

## Prospector Output
### Before Completion

${generateMarkdownTable(tooloutput.prospector_output[0].messages)}

\`\`\` 
${JSON.stringify(tooloutput.prospector_output[0], null, 2)}
\`\`\`
### After Completion
${generateMarkdownTable(tooloutput.prospector_output[1].messages)}

\`\`\`
${JSON.stringify(tooloutput.prospector_output[1], null, 2)}
\`\`\`

## Crosshair Output
### Before Completion
\`\`\`
${JSON.stringify(tooloutput.crosshair_output[0], null, 2)}
\`\`\`
### After Completion
\`\`\`
${JSON.stringify(tooloutput.crosshair_output[1], null, 2)}
\`\`\`

--- 

Session ID: \`${sessionId}\`

Time taken: ${elapsedTime.toFixed(2)} seconds
`;

      let document: vscode.TextDocument | undefined;

      if (saveResults) {
        const fullPath =
          vscode.window.activeTextEditor?.document.fileName;
        console.log('Full Path', fullPath);
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
          console.log('Saved to', newFilePath);

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
