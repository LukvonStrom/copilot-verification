import json
from mitmproxy import http
import time
from models import Base, CopilotCapture
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import uuid
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os

from models import CopilotCapture, Session, Base
from mitmproxy.addons import asgiapp



## SQLAlchemy
engine = create_engine('sqlite:///sessions.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)
db.Model = Base
# Set the query property to use your session
Base.query = db_session.query_property()
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
            'session_id': capture.session_id,
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
    db.session.add(new_session)
    db.session.commit()

    return jsonify(session_id=session_id)

@app.route('/session/<session_id>/augment', methods=['POST'])
def augment_session(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if session is None:
        abort(404)
    
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    augmented_file_path = os.path.join(base_dir, 'augmented-uploads', session_id+'.py')
    os.makedirs(os.path.dirname(augmented_file_path), exist_ok=True)
    file.save(augmented_file_path)

    session.augmented_file_path = augmented_file_path
    db.session.commit()

    return jsonify(session_id=session_id, augmented=True)


with app.app_context():
    db.create_all()

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
            capture = CopilotCapture(
                session_id=str(int(time.time())) + str(self.num),
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
    asgiapp.WSGIApp(app, "sessions.copilot", 80),
]
