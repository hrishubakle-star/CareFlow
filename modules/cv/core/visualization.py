"""
Handles drawing the AR HUD, multi-person neon skeletons, and grip zones.
"""
import cv2
from ..config import settings

class Visualizer:
    def __init__(self):
        # We define a distinct color for the caretaker (MedLens Blue)
        self.caretaker_color = (255, 151, 0) # BGR for #0097ff

    def draw_neon_skeletons(self, frame, extracted_data):
        """Draws AR structural lines over the detected bodies."""
        h, w, _ = frame.shape
        
        # Connections to draw the torso box
        connections = [
            ('left_shoulder', 'right_shoulder'),
            ('left_hip', 'right_hip'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip')
        ]

        for role, person in extracted_data.items():
            if not person: 
                continue
            
            # Caretaker is Blue, Patient is Neon Green
            color = self.caretaker_color if role == 'caretaker' else settings.COLOR_SAFE
            
            # Draw the skeletal lines
            for pt1, pt2 in connections:
                if pt1 in person and pt2 in person:
                    x1, y1 = int(person[pt1]['x'] * w), int(person[pt1]['y'] * h)
                    x2, y2 = int(person[pt2]['x'] * w), int(person[pt2]['y'] * h)
                    # Glowing neon line effect
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 6, cv2.LINE_AA)
                    cv2.line(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
                    
        return frame

    def draw_grip_zones(self, frame, zones):
        """(KEEP YOUR EXACT PREVIOUS NEON GRIP ZONE CODE HERE)"""
        if not zones:
            return frame
            
        h, w, _ = frame.shape
        pixel_zones = [(int(z['x'] * w), int(z['y'] * h)) for z in zones]
        
        x_coords = [p[0] for p in pixel_zones]
        y_coords = [p[1] for p in pixel_zones]
        
        box_pt1 = (min(x_coords) - 30, min(y_coords) - 30)
        box_pt2 = (max(x_coords) + 30, max(y_coords) + 30)
        
        cv2.rectangle(frame, box_pt1, box_pt2, (0, 100, 0), 10, cv2.LINE_AA)
        cv2.rectangle(frame, box_pt1, box_pt2, settings.COLOR_SAFE, 4, cv2.LINE_AA)
        cv2.rectangle(frame, box_pt1, box_pt2, (200, 255, 200), 1, cv2.LINE_AA)

        for cx, cy in pixel_zones:
            cv2.circle(frame, (cx, cy), 18, (0, 100, 0), cv2.FILLED)         
            cv2.circle(frame, (cx, cy), 12, settings.COLOR_SAFE, cv2.FILLED) 
            cv2.circle(frame, (cx, cy), 6, (200, 255, 200), cv2.FILLED)      
            
            arrow_end = (cx, cy - 45)
            cv2.arrowedLine(frame, (cx, cy), arrow_end, (0, 100, 0), 6, tipLength=0.3, line_type=cv2.LINE_AA)
            cv2.arrowedLine(frame, (cx, cy), arrow_end, settings.COLOR_SAFE, 2, tipLength=0.3, line_type=cv2.LINE_AA)
            
        return frame

    def draw_hud(self, frame, status, fps):
        """Draws the safety status, warnings, and FPS counter."""
        # Main Patient Status Box
        color = settings.COLOR_SAFE if status['patient_safe'] else settings.COLOR_DANGER
        cv2.rectangle(frame, (0, 0), (640, 50), (0, 0, 0), -1)
        cv2.putText(frame, f"PATIENT: {status['patient_msg']}", (10, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
                    
        # Caretaker Status Box (Appears at the bottom of the screen)
        if status['caretaker_warning']:
            warn_color = settings.COLOR_WARNING if "KEEP BACK STRAIGHT" in status['caretaker_warning'] else self.caretaker_color
            cv2.rectangle(frame, (0, 430), (640, 480), (0, 0, 0), -1)
            cv2.putText(frame, status['caretaker_warning'], (10, 465), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, warn_color, 2, cv2.LINE_AA)
                    
        # Display FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (530, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, settings.COLOR_TEXT, 2)
                    
        return frame