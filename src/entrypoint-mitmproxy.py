import sys
from pathlib import Path

# Determine the absolute path to your project's root directory
root_dir = Path(__file__).resolve().parent.parent  # Adjust as necessary

# Add the project's root directory to sys.path
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))
print(root_dir)

from mitmproxy.addons import asgiapp
from src.flask import create_app
from src.mitmproxy.processor import CaptureGitHubCopilot

app = create_app()

addons = [
    CaptureGitHubCopilot(),
    asgiapp.WSGIApp(app, "example.com", 80),
]
