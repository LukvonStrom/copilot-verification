// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log(
    'Congratulations, your extension "completion-verifier" is now active!'
  );

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  let disposable = vscode.commands.registerCommand(
    'completion-verifier.startCompletionVerifier',
    () => {
      // The code you place here will be executed every time your command is executed
      // Display a message box to the user

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
        vscode.window.withProgress(
          {
            location: vscode.ProgressLocation.Notification,
            title: 'Loading...',
            cancellable: false
          },
          async (progress) => {
            // Perform your loading logic here
            // For example, you can make an API call or load data from a file
            // Update the progress message as needed
            progress.report({ message: 'Loading data...' });

            // Simulate a delay for demonstration purposes
            await new Promise((resolve) => setTimeout(resolve, 2000));

            // Once the loading is complete, show a success message
            vscode.window.showInformationMessage('Loading complete!');
          }
        );
        vscode.window.showInformationMessage(
          'Successfully activated the completion verifier! Now go ahead and prompt Copilot to complete some code.'
        );
      }
    }
  );

  context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
