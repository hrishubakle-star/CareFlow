from flask import Blueprint, render_template

# Initialize the Blueprint
sos_bp = Blueprint('sos', __name__)

PRESET_NAVIGATOR_NUMBER = "+12345678900" 

@sos_bp.route('/')
def home():
    # Looks for index.html inside the templates/sos/ directory
    return render_template(
        'sos/index.html', 
        phone_number=PRESET_NAVIGATOR_NUMBER
    )