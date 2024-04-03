import json
from mitmproxy import http
import time
import os

class CaptureGitHubCopilot:
    def __init__(self):
        self.num = 1
        self.delta_text = ''

    def parse_stream(self, stream, is_codex=False):
        data_chunks = stream.split('data: ')[1:]
        response_items = []
        for chunk in data_chunks:
          try:
              json_data = json.loads(chunk)
              response_items.append(json_data)
              if is_codex:
                  self.delta_text += self.extract_and_preserve_structure_codex(json_data)
              else:
                self.delta_text += self.extract_and_preserve_structure(json_data)
          except json.JSONDecodeError:
              # Optionally log or handle the error here
              pass
        return response_items
    
    def extract_and_preserve_structure(self, data):
      extracted_text = ''

      if isinstance(data, dict):
          for key, value in data.items():
              if key == 'delta' and 'content' in value and value['content'] is not None:
                  extracted_text += value['content']
              else:
                  extracted_text += self.extract_and_preserve_structure(value)
      elif isinstance(data, list):
          for item in data:
              extracted_text += self.extract_and_preserve_structure(item)

      return extracted_text
    
    def extract_and_preserve_structure_codex(self, data):
      extracted_text = ''

      if isinstance(data, dict):
          for key, value in data.items():
              if key == 'choices' and 'text' in value and value['text'] is not None:
                  extracted_text += value
              else:
                  extracted_text += self.extract_and_preserve_structure_codex(value)
      elif isinstance(data, list):
          for item in data:
              extracted_text += self.extract_and_preserve_structure_codex(item)

      return extracted_text

    def response(self, flow: http.HTTPFlow) -> None:
        # Check if the request is to githubcopilot.com
        if "githubcopilot.com" in flow.request.pretty_host or "copilot-proxy.githubusercontent.com" in flow.request.pretty_host:
            is_prompt = False
            if "githubcopilot.com" in flow.request.pretty_host:
                is_prompt = True
            if "copilot-codex/completions" in flow.request.pretty_url:
                is_prompt = False
            # Wait for the entire response body to be received
            if flow.response.stream:
                flow.response.stream = False

            self.delta_text = ''

            base_dir = os.getenv("BASE_DIR", os.getcwd())

            prompt_dir = os.path.join(base_dir, "prompt")
            completion_dir = os.path.join(base_dir, "completion")

            os.makedirs(prompt_dir, exist_ok=True)
            os.makedirs(completion_dir, exist_ok=True)

            timestamp = int(time.time())
            directory = f"{prompt_dir}/copilot_completion_capture_{timestamp}"
            if not is_prompt:
                directory = f"{completion_dir}/copilot_capture_{timestamp}"
            os.makedirs(directory, exist_ok=True)

            

            request_body = json.loads(flow.request.content.decode(errors="replace"))
            if is_prompt:

                with open(os.path.join(directory, f"prompt-{self.num}.txt"), "w") as f:
                    f.write(request_body['messages'][0]['content'])

            
            if is_prompt:
              parsed_response = self.parse_stream(flow.response.content.decode(errors="replace"))
            else:
              parsed_response = flow.response.content.decode(errors="replace")

            with open(os.path.join(directory, f"serialized-answer-{self.num}.md"), "w") as f:
                f.write(self.delta_text)
            print("Wrote serialized reply", os.path.join(directory, f"serialized-answer-{self.num}.md"))

                
            # add timestamps to the files
            for filename in os.listdir(directory):
                os.rename(os.path.join(directory, filename), os.path.join(directory, f"{timestamp}_{filename}"))


            # Create a JSON object with request and response details
            data = {
                "request": {
                    "method": flow.request.method,
                    "url": flow.request.pretty_url,
                    "body": request_body
                },
                "response": {
                    "status_code": flow.response.status_code,
                    "headers": dict(flow.response.headers),
                    "body": parsed_response
                }
            }

            # Save the JSON object to a file
            filename = f"github_copilot_capture_{self.num}.json"
            self.num += 1
            with open(os.path.join(directory, filename), "w") as f:
                json.dump(data, f, indent=4)
            print(f"Saved capture to {filename}")

# Add the addon to mitmproxy
addons = [
    CaptureGitHubCopilot()
]
