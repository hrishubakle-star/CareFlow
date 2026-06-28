import os
from flask import Blueprint, render_template, Response, jsonify, current_app
from .stream_engine import generate_frames, latest_telemetry 

# Initialize the Blueprint
cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/')
def dashboard():
    """Renders the main CV UI."""
    return render_template('cv/dashboard.html')

@cv_bp.route('/video_feed/<source>')
def video_feed(source):
    """Streams the AI-processed video feed."""
    if source == 'camera':
        video_source = 0
    else:
        # Dynamically map the video path to the static folder
        video_source = os.path.join(current_app.root_path, 'static', 'cv_assets', 'abc.mp4')
        
    return Response(generate_frames(video_source), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@cv_bp.route('/status_data')
def status_data():
    """Returns the raw AI status as a JSON object."""
    return jsonify(latest_telemetry)