import { HttpsProxyAgent } from 'https-proxy-agent';
import * as vscode from 'vscode';
import { getProxyHttpAgent } from 'proxy-http-agent';
import { error } from 'console';

interface SessionCreationResponse {
  session_id: string;
}

interface SessionAugmentationResponse {
  crosshair_output: [string, string];
  crosshair_valid: [boolean, boolean];
  prospector_output: [string, string];
  prospector_valid: [boolean, boolean];
  session_id: string;
}

interface DiagnosticResponse {
  method: 'textDocument/publishDiagnostics';
  params: {
    uri: string;
    diagnostics: vscode.Diagnostic[];
  };
}

export class VerifierClient {
  constructor(private baseUri: string) {}

  private async fetchWithVscodeProxy(
    path: string,
    options?: any
  ): Promise<Response> {
    // Read VSCode proxy settings
    const config = vscode.workspace.getConfiguration('http');
    const proxySetting = config.get('proxy');

    if (proxySetting) {
      process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
      // If a proxy is configured and enabled, set up the proxy agent
      let agent = getProxyHttpAgent({
        proxy: proxySetting as string,
        endServerProtocol: 'https:',
      });
      options.agent = agent;
    }

    // Use fetch as normal, now configured to use the proxy if needed

    return (await import('node-fetch').then(({ default: fetch }) =>
      fetch(`${this.baseUri}${path}`, options)
    )) as Response;
  }

  public async fetchDiagnosticsForAsserts(
    fileContent: string,
    filePath: string
  ): Promise<DiagnosticResponse> {
    const response = await this.fetchWithVscodeProxy(`/asserts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ file: fileContent, filePath }),
    });
    if (!response.ok) {
      const responseText = await response.text();
      throw new Error(
        `Error ${response.status} while trying to check asserts ${response.statusText} - ${responseText}`
      );
    }
    let diagnosticsResponse =
      (await response.json()) as DiagnosticResponse;
    diagnosticsResponse.params.diagnostics =
      diagnosticsResponse.params.diagnostics.map(
        (diagnostic: vscode.Diagnostic) => {
          // get end of line from fileContent
          let endOfLine =
            fileContent.split('\n')[diagnostic.range.end.line]
              .length ?? diagnostic.range.end.character;
          // return new vscode.Diagnostic with end of line
          return new vscode.Diagnostic(
            new vscode.Range(
              diagnostic.range.start.line,
              diagnostic.range.start.character,
              diagnostic.range.end.line,
              endOfLine
            ),
            diagnostic.message,
            diagnostic.severity
          );
        }
      );
    return diagnosticsResponse;
  }

  // Function to create a session
  public async createSession(
    fileContent: string
  ): Promise<SessionCreationResponse> {
    const response = await this.fetchWithVscodeProxy(`/session/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ file: fileContent }),
    });
    if (!response.ok) {
      const responseText = await response.text();
      throw new Error(
        `Error ${response.status} while creating session ${response.statusText} - ${responseText}`
      );
    }
    const sessionData =
      (await response.json()) as SessionCreationResponse;
    return sessionData;
  }

  // Function to augment a session
  public async augmentSession(
    sessionId: string,
    augmentedFileContent: any
  ): Promise<SessionAugmentationResponse> {
    const response = await this.fetchWithVscodeProxy(
      `/session/${sessionId}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file: augmentedFileContent }),
      }
    );
    if (!response.ok) {
      const responseText = await response.text();
      throw new Error(
        `Error ${response.status} while verifying ${response.statusText} - ${responseText}`
      );
    }
    console.log('Response:', response);
    const augmentedData =
      (await response.json()) as SessionAugmentationResponse;
    return augmentedData;
  }
}
