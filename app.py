import uuid
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    original_file_path = db.Column(db.String(120), nullable=False)
    augmented_file_path = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Session {self.id}>'

# Set the root directory you want to start listing files from
base_dir = os.getenv("BASE_DIR", os.getcwd())

ROOT_DIR = os.path.join(base_dir, "prompt")


def get_file_contents(file_path):
    """Reads the contents of a file and returns it."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)

@app.route('/files', methods=['GET'])
def list_files():
    app.logger.debug('Listing files '+ ROOT_DIR)
    items = []
    print(ROOT_DIR)
    # Walk through the directory
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            app.logger.debug('Listing file '+ file)
            # Construct the file's path relative to ROOT_DIR
            rel_dir = os.path.relpath(root, ROOT_DIR)
            rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
            # Get the full path to read the file
            full_path = os.path.join(root, file)
            # Append file path and contents to the list
            items.append({
                "path": rel_file,
                # "contents": get_file_contents(full_path)
            })
    
    return jsonify(items)

@app.route('/files/<path:file_path>', methods=['GET'])
def get_file(file_path):
    app.logger.debug('Getting file '+ file_path)
    full_path = os.path.join(ROOT_DIR, file_path)
    return jsonify({
        "path": file_path,
        "contents": get_file_contents(full_path)
    })

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
