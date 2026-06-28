"""
Core Vision Module: Handles pose estimation using YOLOv8.
Upgraded for multi-person tracking with PyTorch Bypass and CPU Turbo Boost.
"""
import cv2
import torch

# PyTorch 2.6 Monkey Patch (Keep this intact!)
_original_load = torch.load

def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)

torch.load = _patched_load

from ultralytics import YOLO
from ..config import settings

class PoseDetector:
    def __init__(self):
        print("Loading YOLOv8 Nano Pose Model...")
        self.model = YOLO('yolov8n-pose.pt')

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        
        # --- THE TURBO BOOST ---
        # By setting imgsz=320, we quarter the mathematical workload for the i3 CPU.
        # device='cpu' forces the model to ignore any missing GPU drivers.
        results = self.model.predict(
            source=frame, 
            conf=settings.MIN_DETECTION_CONFIDENCE,
            imgsz=320, 
            device='cpu',
            verbose=False
        )
        
        return frame, results[0]
        
    def release(self):
        pass