from flask import Blueprint, jsonify, request, abort
import os
import uuid
from flask import current_app

from src.database.models import Session, CopilotCapture
from src.database.session_manager import get_db
from src.testing.check_asserts import check_asserts
from src.testing.tools import run_crosshair, run_prospector

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/asserts", methods=["POST"])
def check_asserts_route():
    if "file" not in request.json:
        return jsonify(error="No file in request"), 400

    file = request.json["file"]
    filePath = request.json["filePath"]
    assert_found = check_asserts(file, filePath)

    return jsonify(assert_found), 200


@main_bp.route("/captures", methods=["GET"])
def get_captures():
    with get_db() as db_session:
        captures = db_session.query(CopilotCapture).all()
        captures_list = [
            {
                "id": capture.id,
                "time": capture.time,
                "running_id": capture.running_id,
                "request_method": capture.request_method,
                "request_url": capture.request_url,
                "request_body": capture.request_body,
                "response_status_code": capture.response_status_code,
                "response_headers": capture.response_headers,
                "response_body": capture.response_body,
                "parsed_content": capture.parsed_content,
            }
            for capture in captures
        ]
        return jsonify(captures_list), 200


@main_bp.route("/session/", methods=["POST"])
def create_session():

    if "file" not in request.json:
        return jsonify(error="No file in request"), 400

    file = request.json["file"]

    session_id = str(uuid.uuid4())
    base_dir = current_app.config["BASE_DIR"]
    original_file_path = os.path.join(base_dir, "uploads", session_id + ".py")
    os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
    with open(original_file_path, "w", encoding="utf-8") as f:
        f.write(file)
    with get_db() as db_session:
        new_session = Session(id=session_id, original_file_path=original_file_path)
        db_session.add(new_session)
        db_session.commit()

    return jsonify(session_id=session_id)


@main_bp.route("/session/<session_id>", methods=["PUT"])
def augment_session(session_id):
    with get_db() as db_session:
        session = db_session.query(Session).filter_by(id=session_id).first()
        if session is None:
            abort(404)

        if "file" not in request.json:
            return jsonify(error="No file in request"), 400

        file = request.json["file"]
        base_dir = current_app.config["BASE_DIR"]
        augmented_file_path = os.path.join(
            base_dir, "augmented-uploads", session_id + ".py"
        )
        os.makedirs(os.path.dirname(augmented_file_path), exist_ok=True)
        with open(augmented_file_path, "w", encoding="utf-8") as f:
            f.write(file)

        session.augmented_file_path = augmented_file_path
        db_session.commit()

        original_prospector_valid, original_prospector_output = run_prospector(
            session.original_file_path
        )
        original_crosshair_valid, original_crosshair_output = run_crosshair(
            session.original_file_path
        )

        augmented_prospector_valid, augmented_prospector_output = run_prospector(
            session.augmented_file_path
        )
        augmented_crosshair_valid, augmented_crosshair_output = run_crosshair(
            session.augmented_file_path
        )

        variables = {
            "session_id": session_id,
            "crosshair_output": [original_crosshair_output, augmented_crosshair_output],
            "prospector_output": [
                original_prospector_output,
                augmented_prospector_output,
            ],
            "crosshair_valid": [original_crosshair_valid, augmented_crosshair_valid],
            "prospector_valid": [original_prospector_valid, augmented_prospector_valid],
        }
        return jsonify(variables), 200
