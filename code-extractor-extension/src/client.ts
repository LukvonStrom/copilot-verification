import { HttpsProxyAgent } from 'https-proxy-agent';
import * as vscode from 'vscode';
import { getProxyHttpAgent } from 'proxy-http-agent';

async function fetchWithVscodeProxy(
  url: string,
  options?: any
): Promise<any> {
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

  return await import('node-fetch').then(({ default: fetch }) =>
    fetch(url, options)
  );
}

const BASE_URL = 'http://example.com';

export async function fetchDiagnosticsForAsserts(
  fileContent: string,
  filePath: string
): Promise<{
  method: 'textDocument/publishDiagnostics';
  params: {
    uri: string;
    diagnostics: vscode.Diagnostic[];
  };
}> {
  const response = await fetchWithVscodeProxy(`${BASE_URL}/asserts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ file: fileContent, filePath }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  let diagnosticsResponse = await response.json();
  diagnosticsResponse.params.diagnostics =
    diagnosticsResponse.params.diagnostics.map(
      (diagnostic: vscode.Diagnostic) => {
        // get end of line from fileContent
        let endOfLine =
          fileContent.split('\n')[diagnostic.range.end.line].length ?? diagnostic.range.end.character;
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

export async function fetchCaptures() {
  try {
    const response = await fetchWithVscodeProxy(
      `${BASE_URL}/captures`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const captures = await response.json();
    return captures;
  } catch (error: any) {
    if (error.name === 'AbortError') {
      console.error('Fetch aborted');
    } else {
      console.error('Error fetching captures:', error);
    }
  }
}

// Function to create a session
export async function createSession(
  fileContent: string
): Promise<any> {
  try {
    const response = await fetchWithVscodeProxy(
      `${BASE_URL}/session/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file: fileContent }),
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const sessionData = await response.json();
    return sessionData;
  } catch (error: any) {
    if (error.name === 'AbortError') {
      console.error('Fetch aborted');
    } else {
      console.error('Error creating session:', error);
    }
  }
}

// Function to augment a session
export async function augmentSession(
  sessionId: string,
  augmentedFileContent: any
) {
  try {
    const response = await fetchWithVscodeProxy(
      `${BASE_URL}/session/${sessionId}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file: augmentedFileContent }),
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    console.log('Response:', response);
    const augmentedData = await response.json();
    return augmentedData;
  } catch (error: any) {
    if (error.name === 'AbortError') {
      console.error('Fetch aborted');
    } else {
      console.error('Error augmenting session:', error);
    }
  }
}
