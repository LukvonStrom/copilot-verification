# copilot-verification


## Preamble
:warning: **Disclaimer**: The code contained in this repository is provided for educational purposes only. By executing or using the code, you assume full responsibility for any consequences that may arise. The creators, contributors, or any associated parties shall not be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this code. Any liabilities arising from the violation of any plausible terms of use of GitHub Copilot or related services are explicitly disclaimed. Use this code at your own risk. :warning:

## Setup
The docker container depends on being run with `docker run --rm -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -p 8080:8080 ghcr.io/lukvonstrom/copilot-verification:main` please be aware that currently only amd64 architectures are supported.


### ARM based Macs
For ARM based Macs, intel emulation via rosetta needs to be used, as microsoft provides only `z3-solver` binaries for macos arm, but not for linux arm via pip.
Building Z3 from source is quite expensive, therefore emulation can be used like this (given that you manage docker via colima https://github.com/abiosoft/colima and have rosetta installed already https://support.apple.com/en-gb/102527):
`colima start --profile amd64 -a x86_64 -c 4 -m 6`

### Installing mitmproxy root certificates
Please follow this tutorial to make sure that the system trusts mitmproxy: https://docs.mitmproxy.org/stable/concepts-certificates/

### Setup VSCode Proxy

Please follow the steps outlined here: (alternative link: https://device.harmonyos.com/en/docs/documentation/guide/vscode_proxy-0000001074231144 - specify the server as `https://localhost:8080` and disable strict ssl checking)
![./static/proxy.gif](./static/proxy.gif)


### Basic test of the extension
Now that everything is setup we can conduct a basic test as shown below:
![./static/basic-demo.gif](./static/basic-demo.gif)

The steps shown in the video are:
- Open the cloned repository in vscode.
- Open the folder containing the extension in vscode via `code code-extractor-extension`
- Click on `Run & Debug` - and there on the Play icon next to `Run Extension`
- In the newly spawned VsCode instance with the extension in debug mode, open a new python file
- Open the Command Bar with `CMD-SHIFT-P` 
- Select `copilot-verifier: Start Verification Session`
- A notification should appear and the Github Copilot Inline Chat Window should open itself.
- Prompt Copilot
- After a short delay, the verification will start, which is signified by a loading notification
- Next, a markdown with the verification results from the backend will open.


### Syntax Highlighting for missing pre- or postconditions
The extension automatically validates in the background that two `assert` statements are present in any method in the code.
If this is not the case, a syntax error will be displayed in the Editor at the specific method.
![./static/conditions-error.jpg](./static/conditions-error.jpg)

The error is verbose on purpose to facilitate an easier fix with Copilot. 
To now prompt copilot to fix this error, one simply has to invoke it inline by clicking on the impacted line and executing `CMD-I`.
Copilot subsequently will attempt to generate sensible pre- and postconditions to fix the error.

![./static/copilot-conditions.jpg](./static/copilot-conditions.jpg)

## Changed Copilot System Prompt for shorter files

```
{"role": "user", "content": "I have the following code in the selection:\n```python\n# FILEPATH: /Users/lukasfruntke/Postman/test.py\n# BEGIN: ed8c6549bwf9\nimport os\nimport os\n\ncurrent_path = os.getcwd()\nprint(\"Current path:\", current_path)\n# END: ed8c6549bwf9\n```"}, 
```

```
Only change the code inside of the selection, delimited by markers '# BEGIN: ed8c6549bwf9' and '# END: ed8c6549bwf9'. The code block with the suggested changes should also contain the markers.
```