import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .services import generate_todo

# Initialize the Blueprint
doc_bp = Blueprint('doc', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@doc_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Dynamically get the isolated upload path
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'doc')
            os.makedirs(upload_dir, exist_ok=True)
            
            save_path = os.path.join(upload_dir, filename)
            file.save(save_path)
            
            # Redirect explicitly to the doc blueprint's result route
            return redirect(url_for('doc.result', filename=filename))
        else:
            flash('Only PNG/JPG/JPEG files allowed')

    return render_template('doc/upload.html')


@doc_bp.route('/result/<filename>')
def result(filename):
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'doc')
    image_path = os.path.join(upload_dir, filename)

    try:
        data = generate_todo(image_path)
    except Exception as e:
        return f"Error occurred: {str(e)}"

    return render_template(
        'doc/result.html',
        filename=filename,
        result=data
    )