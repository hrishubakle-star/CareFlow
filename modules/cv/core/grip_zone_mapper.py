"""
Calculates the physical grip points for a safe patient lift based on extracted landmarks.
Updated to read the new YOLOv8 multi-person data structure.
"""

class GripZoneMapper:
    def __init__(self):
        # We shift the upper grip slightly down from the shoulder towards the hip
        # to target the shoulder blade area.
        self.shoulder_drop_ratio = 0.20 

    def get_safe_zones(self, patient_data):
        """
        Calculates safe lifting anchor points for the patient.
        
        Args:
            patient_data (dict): The extracted joints for the patient.
            
        Returns:
            list: A list of dicts containing 'x' and 'y' coordinates for grip targets.
        """
        # Safety check: if there is no patient detected, return empty zones
        if not patient_data:
            return []

        zones = []

        # 1. Left Upper Back (Below Left Shoulder)
        left_shoulder = patient_data['left_shoulder']
        left_hip = patient_data['left_hip']
        
        left_upper_grip = {
            'x': left_shoulder['x'],
            'y': left_shoulder['y'] + ((left_hip['y'] - left_shoulder['y']) * self.shoulder_drop_ratio),
            'label': 'Left Upper'
        }
        zones.append(left_upper_grip)

        # 2. Right Upper Back (Below Right Shoulder)
        right_shoulder = patient_data['right_shoulder']
        right_hip = patient_data['right_hip']
        
        right_upper_grip = {
            'x': right_shoulder['x'],
            'y': right_shoulder['y'] + ((right_hip['y'] - right_shoulder['y']) * self.shoulder_drop_ratio),
            'label': 'Right Upper'
        }
        zones.append(right_upper_grip)

        # 3. Left Hip / Pelvis
        zones.append({
            'x': left_hip['x'],
            'y': left_hip['y'],
            'label': 'Left Lower'
        })

        # 4. Right Hip / Pelvis
        zones.append({
            'x': right_hip['x'],
            'y': right_hip['y'],
            'label': 'Right Lower'
        })

        return zones