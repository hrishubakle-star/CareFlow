from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load environment variables once at startup
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Import blueprints
from modules.sos.routes import sos_bp
from modules.doc.routes import doc_bp
from modules.cv.routes import cv_bp   # NEW

# Register blueprints with URL prefixes
app.register_blueprint(sos_bp, url_prefix='/sos')
app.register_blueprint(doc_bp, url_prefix='/doc')
app.register_blueprint(cv_bp, url_prefix='/cv') # NEW

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # CRITICAL FIX: use_reloader=False
    # If this is True, Flask starts two processes, loading your YOLO model twice, 
    # taking up double the RAM, and crashing your webcam. Keep it False!
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)