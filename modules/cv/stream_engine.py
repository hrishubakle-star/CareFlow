import cv2
import time
import numpy as np

# Use relative imports to target the new 'core' directory
from .core.pose_detector import PoseDetector
from .core.landmark_extractor import LandmarkExtractor
from .core.grip_zone_mapper import GripZoneMapper
from .core.safety_validator import SafetyValidator
from .core.visualization import Visualizer

# ==========================================
# GLOBAL AI INITIALIZATION
# ==========================================
print("Initializing AI Pipeline (This may take a moment to load into memory)...")
try:
    detector = PoseDetector()
    extractor = LandmarkExtractor()
    mapper = GripZoneMapper()
    validator = SafetyValidator()
    visualizer = Visualizer()
    AI_READY = True
except Exception as e:
    print(f"CRITICAL AI ERROR: {e}")
    AI_READY = False
    ai_error_msg = str(e)

# Create a global dictionary to hold the live data for the web browser
latest_telemetry = {
    "patient_safe": False,
    "patient_msg": "NO PATIENT DETECTED",
    "caretaker_warning": None
}

# ... (Keep your generate_error_frame and generate_frames functions exactly the same below here) ...
def generate_error_frame(message):
    """Generates a black frame with an error message to display on the webpage."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(frame, "VIDEO SOURCE ERROR:", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, message, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    ret, buffer = cv2.imencode('.jpg', frame)
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'

def generate_frames(video_source):
    """Generates an HTTP video stream from the AI pipeline."""
    
    # Safety Check: If the AI failed to load on startup, show the error on the website
    if not AI_READY:
        yield generate_error_frame("AI Init Failed. Check Terminal.")
        return

    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        source_name = "Webcam" if video_source == 0 else str(video_source)
        yield generate_error_frame(f"Could not load: {source_name}")
        return

    prev_time = 0
    
    try:
        while cap.isOpened():
            success, raw_frame = cap.read()
            if not success:
                if video_source != 0: # If it's a video file, loop it
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else: # If it's a webcam and it fails, stop
                    break
                
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time

            try:
                # --- PIPELINE ---
                frame, raw_results = detector.process_frame(raw_frame)
                
                # Extract and sort multi-person data
                extracted_data = extractor.extract(raw_results)
                
                # Validate safety for both people
                status = validator.validate_lift(extracted_data)

                # --- UPDATE TELEMETRY FOR THE WEB BROWSER ---
                global latest_telemetry
                latest_telemetry.update(status)
                
                # Map grip zones ONLY if patient is safe
                grip_zones = mapper.get_safe_zones(extracted_data['patient']) if status['patient_safe'] else []
                
                # Draw the new AR overlays
                frame = visualizer.draw_neon_skeletons(frame, extracted_data)
                frame = visualizer.draw_grip_zones(frame, grip_zones)
                frame = visualizer.draw_hud(frame, status, fps)
                
                # --- WEB ENCODING ---
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                       
            except Exception as e:
                print(f"Frame processing error: {e}")
                continue
                
    finally:
        # A 'finally' block ensures that when you switch from video to webcam, 
        # the camera hardware safely disconnects in the background.
        cap.release()