import json
from mitmproxy import http
import time
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import uuid
from flask import Flask, jsonify, request, abort
import os

from mitmproxy.addons import asgiapp
import ast
import subprocess
import json

# Run prospector via cli on a given file that is given as parameter
# The output structure is as follows:
def run_prospector(file_path):
  command = f"python -m prospector {file_path} -o json --zero-exit"
  result = subprocess.run(command, shell=True, capture_output=True, text=True)
  if result.returncode == 0:
    return True, None
  print("raw output", result)
  output = json.loads(result.stdout.strip())
  print(output["summary"]["message_count"], "issues found in", file_path)
  return False, output


# write a mypy parser from a string, split by newline then parse: {FILENAME}:{LINE_NUMBER}: error: {MESSAGE}
def parse_mypy_output(output):
  lines = output.split("\n")
  errors = []
  for line in lines:
    if "error" in line:
      parts = line.split(":")
      message = parts[3:]
      errors.append({
        "line_number": parts[1],
        "message": (("".join(message)).strip()).replace("  ", " ")
      })
  return errors

# write a method that parses a targetfile with ast and checks if there are any asserts statements
def check_asserts(file_path):
  with open(file_path, "r") as file:
    content = file.read()
    parsed_content = ast.parse(content)
    for node in ast.walk(parsed_content):
      if isinstance(node, ast.Assert):
        print(node)
        return True
  return False

# run crosshair via crosshair check {FILENAME} --analysis_kind asserts
def run_crosshair(file_path):

  if not check_asserts(file_path):
    # throw exception
    return False, f"No asserts found"
  command = f"crosshair check {file_path} --analysis_kind asserts"
  result = subprocess.run(command, shell=True, capture_output=True, text=True)
  returncode = result.returncode
  print("crosshair exit code", result.returncode)
  output = result.stdout.strip()
  print("crosshair output", output)
  output = parse_mypy_output(output)

  # if output is a list and empty and returncode is 1, rais exception
  if returncode == 1 and len(output) == 0:
    return False, "Verification failed. No issues triagable by Crosshair found."
  elif returncode == 0:
    return True, None
  return False, output




## SQLAlchemy
engine = create_engine('sqlite:///sessions.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))



app = Flask(__name__)
Base = declarative_base()

# Set the query property to use your session
Base.query = db_session.query_property()

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    original_file_path = Column(String(120), nullable=False)
    augmented_file_path = Column(String(120), nullable=True)

    def __repr__(self):
        return f'<Session {self.id}>'
    
class CopilotCapture(Base):
    __tablename__ = 'copilot_capture'
    
    id = Column(Integer, primary_key=True)
    time = Column(String(36), nullable=False)
    running_id = Column(String(36), nullable=False)
    request_method = Column(String(10))
    request_url = Column(String(255))
    request_body = Column(Text)
    response_status_code = Column(Integer)
    response_headers = Column(Text)
    response_body = Column(Text)
    parsed_content = Column(Text)

    def __repr__(self):
        return f'<CopilotCapture {self.id}>'


Base.metadata.create_all(bind=engine)


# Set the root directory you want to start listing files from
base_dir = os.getenv("BASE_DIR", os.getcwd())

ROOT_DIR = os.path.join(base_dir, "prompt")

@app.route('/captures', methods=['GET'])
def get_captures():
    captures = CopilotCapture.query.all()
    captures_list = [
        {
            'id': capture.id,
            'time': capture.time,
            'running_id': capture.running_id,
            'request_method': capture.request_method,
            'request_url': capture.request_url,
            'request_body': capture.request_body,
            'response_status_code': capture.response_status_code,
            'response_headers': capture.response_headers,
            'response_body': capture.response_body,
            'parsed_content': capture.parsed_content
        } for capture in captures
    ]
    return jsonify(captures_list), 200



@app.route('/session/', methods=['POST'])
def create_session():

    if 'file' not in request.json:
        return jsonify(error="No file in request"), 400
    
    # change this so instead it uses the request body key files
    file = request.json['file'] 
    
    print("received file")

    session_id = str(uuid.uuid4())
    original_file_path = os.path.join(base_dir, 'uploads', session_id+'.py')
    os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
    with open(original_file_path, 'w') as f:
        f.write(file)

    new_session = Session(id=session_id, original_file_path=original_file_path)
    db_session.add(new_session)
    db_session.commit()

    return jsonify(session_id=session_id)

@app.route('/session/<session_id>', methods=['PUT'])
def augment_session(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if session is None:
        abort(404)
    
    if 'file' not in request.json:
        return jsonify(error="No file in request"), 400
    
    # get current time
    
    # change this so instead it uses the request body key files
    file = request.json['file'] 

    augmented_file_path = os.path.join(base_dir, 'augmented-uploads', session_id+'.py')
    os.makedirs(os.path.dirname(augmented_file_path), exist_ok=True)
    with open(augmented_file_path, 'w') as f:
        f.write(file)

    session.augmented_file_path = augmented_file_path
    db_session.commit()

    original_prospector_valid, original_prospector_output = run_prospector(session.original_file_path)
    original_crosshair_valid, original_crosshair_output = run_crosshair(session.original_file_path)

    augmented_prospector_valid, augmented_prospector_output = run_prospector(session.augmented_file_path)
    augmented_crosshair_valid, augmented_crosshair_output = run_crosshair(session.augmented_file_path)




    # capture = CopilotCapture.query.filter_by(time=session_id).first()
    variables = {
        'session_id': session_id,
        'crosshair_output': [original_crosshair_output, augmented_crosshair_output],
        'prospector_output': [original_prospector_output, augmented_prospector_output],
        'crosshair_valid': [original_crosshair_valid, augmented_crosshair_valid],
        'prospector_valid': [original_prospector_valid, augmented_prospector_valid]
    }
    return jsonify(variables), 200

## Mitmproxy





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
                    extracted_text += value['text']
                else:
                    extracted_text += self.extract_and_preserve_structure_codex(value)
        elif isinstance(data, list):
            for item in data:
                extracted_text += self.extract_and_preserve_structure_codex(item)
        return extracted_text

    def response(self, flow: http.HTTPFlow) -> None:
        if "githubcopilot.com" in flow.request.pretty_host or "copilot-proxy.githubusercontent.com" in flow.request.pretty_host:
            is_prompt = "githubcopilot.com" in flow.request.pretty_host or "copilot-codex/completions" not in flow.request.pretty_url
            if flow.response.stream:
                flow.response.stream = False
            self.delta_text = ''
            request_body = json.loads(flow.request.content.decode(errors="replace"))
            parsed_response = self.parse_stream(flow.response.content.decode(errors="replace")) if is_prompt else flow.response.content.decode(errors="replace")
            if "```" in self.delta_text:
                capture = CopilotCapture(
                    time=str(int(time.time())), 
                    running_id=str(self.num),
                    request_method=flow.request.method,
                    request_url=flow.request.pretty_url,
                    request_body=json.dumps(request_body),
                    response_status_code=flow.response.status_code,
                    response_headers=json.dumps(dict(flow.response.headers)),
                    response_body=json.dumps(parsed_response),
                    parsed_content=self.delta_text
                )
                db_session.add(capture)
                db_session.commit()


            
addons = [
    CaptureGitHubCopilot(),
    asgiapp.WSGIApp(app, "example.com", 80),
]
