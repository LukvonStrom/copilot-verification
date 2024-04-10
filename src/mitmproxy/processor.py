from src.database.database import init_db
from src.database.session_manager import get_db
from src.database.models import CopilotCapture
import json

from mitmproxy import http
import time


init_db()


## Mitmproxy
class CaptureGitHubCopilot:
    def __init__(self):
        self.num = 1
        self.delta_text = ""

    def parse_stream(self, stream, is_codex=False):
        data_chunks = stream.split("data: ")[1:]
        response_items = []
        for chunk in data_chunks:
            try:
                json_data = json.loads(chunk)
                response_items.append(json_data)
                if is_codex:
                    self.delta_text += self.extract_and_preserve_structure_codex(
                        json_data
                    )
                else:
                    self.delta_text += self.extract_and_preserve_structure(json_data)
            except json.JSONDecodeError:
                pass
        return response_items

    def extract_and_preserve_structure(self, data):
        extracted_text = ""
        if isinstance(data, dict):
            for key, value in data.items():
                if (
                    key == "delta"
                    and "content" in value
                    and value["content"] is not None
                ):
                    extracted_text += value["content"]
                else:
                    extracted_text += self.extract_and_preserve_structure(value)
        elif isinstance(data, list):
            for item in data:
                extracted_text += self.extract_and_preserve_structure(item)
        return extracted_text

    def extract_and_preserve_structure_codex(self, data):
        extracted_text = ""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "choices" and "text" in value and value["text"] is not None:
                    extracted_text += value["text"]
                else:
                    extracted_text += self.extract_and_preserve_structure_codex(value)
        elif isinstance(data, list):
            for item in data:
                extracted_text += self.extract_and_preserve_structure_codex(item)
        return extracted_text

    def response(self, flow: http.HTTPFlow) -> None:
        if (
            "githubcopilot.com" in flow.request.pretty_host
            or "copilot-proxy.githubusercontent.com" in flow.request.pretty_host
        ):
            is_prompt = (
                "githubcopilot.com" in flow.request.pretty_host
                or "copilot-codex/completions" not in flow.request.pretty_url
            )
            if flow.response.stream:
                flow.response.stream = False
            self.delta_text = ""
            request_body = json.loads(flow.request.content.decode(errors="replace"))
            parsed_response = (
                self.parse_stream(flow.response.content.decode(errors="replace"))
                if is_prompt
                else flow.response.content.decode(errors="replace")
            )
            if "```" in self.delta_text:
                with get_db() as db_session:
                    capture = CopilotCapture(
                        time=str(int(time.time())),
                        running_id=str(self.num),
                        request_method=flow.request.method,
                        request_url=flow.request.pretty_url,
                        request_body=json.dumps(request_body),
                        response_status_code=flow.response.status_code,
                        response_headers=json.dumps(dict(flow.response.headers)),
                        response_body=json.dumps(parsed_response),
                        parsed_content=self.delta_text,
                    )
                    db_session.add(capture)
                    db_session.commit()
