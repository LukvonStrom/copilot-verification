import uuid
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os

from models import CopilotCapture, Session, Base


app = Flask(__name__)

engine = create_engine('sqlite:///sessions.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

Base.metadata.create_all(bind=engine)

# Set the root directory you want to start listing files from
base_dir = os.getenv("BASE_DIR", os.getcwd())

ROOT_DIR = os.path.join(base_dir, "prompt")

@app.route('/captures', methods=['GET'])
def get_captures():
    captures = db_session.query(CopilotCapture).all()
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

    file = request.json['file']
    session_id = str(uuid.uuid4())
    original_file_path = os.path.join(os.getenv("BASE_DIR", os.getcwd()), 'uploads', session_id+'.py')
    os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
    with open(original_file_path, 'w') as f:
        f.write(file)

    new_session = Session(id=session_id, original_file_path=original_file_path)
    db_session.add(new_session)
    db_session.commit()

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
