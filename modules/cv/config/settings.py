"""
Configuration settings for the Patient Lift Guidance System.
Optimized for Intel i3 CPU (No GPU).
"""

# ==========================================
# 📷 CAMERA SETTINGS
# ==========================================
# Resolution lowered to 640x480 to significantly reduce CPU load 
# while providing enough pixel density for pose estimation.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ==========================================
# 🤖 MEDIA PIPE POSE ESTIMATION
# ==========================================
# Model Complexity: 
# 0 = Lite (Fastest, lowest CPU load, ~15-22 FPS on i3)
# 1 = Full (Balanced, but will likely drop your FPS to ~6-10)
# 2 = Heavy (Highest accuracy, unsuitable for real-time CPU)
MODEL_COMPLEXITY = 0

# Confidence Thresholds [0.0 to 1.0]
# Set to 0.6 to balance reducing false positives while maintaining 
# tracking when a patient's limbs might be partially obscured during a lift.
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# ==========================================
# ⚖️ SAFETY ENGINE & RULE THRESHOLDS
# ==========================================
# Lying Flat Threshold:
# The maximum allowed variance in the Y-axis between the Head, Spine, and Hips.
# MediaPipe normalizes coordinates from 0.0 to 1.0. A value of 0.15 means 
# a 15% variance across the height of the frame is permitted.
MAX_FLAT_Y_VARIANCE = 0.15 

# Lift Mechanics Thresholds:
# Used to calculate if the person performing the lift is using safe body mechanics.
MIN_KNEE_BEND_ANGLE = 90   # Minimum degree of bend to ensure lifting with legs
MAX_BACK_BEND_ANGLE = 45   # Maximum forward tilt of the spine

# ==========================================
# 🎨 VISUALIZATION COLORS (BGR Format for OpenCV)
# ==========================================
# Note: OpenCV uses BGR (Blue, Green, Red) instead of standard RGB
COLOR_SAFE = (0, 255, 0)       # Green (Good form / Safe zones)
COLOR_WARNING = (0, 255, 255)  # Yellow (Approaching unsafe angles)
COLOR_DANGER = (0, 0, 255)     # Red (Unsafe form / Stop)
COLOR_SKELETON = (255, 200, 0) # Cyan-ish (MediaPipe skeleton connections)
COLOR_TEXT = (255, 255, 255)   # White (HUD text)