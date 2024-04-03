import uuid
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os

from models import CopilotCapture, Session, Base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
db.Model = Base



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
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    session_id = str(uuid.uuid4())
    original_file_path = os.path.join(base_dir, 'uploads', session_id+'.py')
    os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
    file.save(original_file_path)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)
