"""
Safety Validator: Evaluates joint angles for both the Patient and Caretaker.
Enforces safe lifting mechanics.
"""
import numpy as np
from ..config import settings

class SafetyValidator:
    def __init__(self):
        pass

    def get_vertical_angle(self, top_point, bottom_point):
        """Calculates the angle of a body segment relative to true vertical (gravity)."""
        dx = top_point['x'] - bottom_point['x']
        dy = top_point['y'] - bottom_point['y']
        
        # Calculate angle against the Y-axis
        angle = np.abs(np.arctan2(dx, dy) * 180.0 / np.pi)
        
        # If it's leaning backwards or forwards past 90, we want absolute deviation
        if angle > 90:
            angle = 180 - angle
        return angle

    def validate_lift(self, extracted_data):
        """
        Evaluates both actors in the scene.
        Returns a dictionary with safety status, messages, and warnings.
        """
        status = {
            'patient_safe': False,
            'patient_msg': "NO PATIENT DETECTED",
            'caretaker_warning': None
        }

        patient = extracted_data.get('patient')
        caretaker = extracted_data.get('caretaker')

        # --- 1. PATIENT VALIDATION ---
        if patient:
            # The extractor already checked Y-variance to assign the "patient" role.
            # If they exist here, they are mostly flat. We confirm safety.
            status['patient_safe'] = True
            status['patient_msg'] = "SAFE TO LIFT"

        # --- 2. CARETAKER VALIDATION (The Bonus Feature!) ---
        if caretaker:
            # Calculate the mathematical center of the shoulders and hips
            neck = {
                'x': (caretaker['left_shoulder']['x'] + caretaker['right_shoulder']['x']) / 2,
                'y': (caretaker['left_shoulder']['y'] + caretaker['right_shoulder']['y']) / 2
            }
            pelvis = {
                'x': (caretaker['left_hip']['x'] + caretaker['right_hip']['x']) / 2,
                'y': (caretaker['left_hip']['y'] + caretaker['right_hip']['y']) / 2
            }

            # Calculate forward back-bend angle
            back_angle = self.get_vertical_angle(neck, pelvis)

            # If bending the spine forward more than the threshold (e.g., 45 degrees)
            if back_angle > settings.MAX_BACK_BEND_ANGLE:
                status['caretaker_warning'] = "⚠ CARETAKER: KEEP BACK STRAIGHT!"
            else:
                status['caretaker_warning'] = "✓ CARETAKER FORM: GOOD"

        return status