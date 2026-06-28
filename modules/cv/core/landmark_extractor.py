"""
Extracts and normalizes joints from YOLOv8 multi-person pose data.
Includes hardened failsafes for empty frames.
"""
import numpy as np

class LandmarkExtractor:
    def __init__(self):
        self.kp_map = {
            'nose': 0, 'left_shoulder': 5, 'right_shoulder': 6,
            'left_hip': 11, 'right_hip': 12, 'left_knee': 13, 'right_knee': 14
        }

    def extract(self, yolo_results):
        extracted_data = {'patient': None, 'caretaker': None}
        
        # FAILSAFE 1: If no humans are detected, stop immediately
        if len(yolo_results) == 0 or yolo_results.keypoints is None:
            return extracted_data
            
        # FAILSAFE 2: If humans are detected but joints failed to render, stop
        if yolo_results.keypoints.xy.shape[1] == 0:
            return extracted_data

        h, w = yolo_results.orig_shape
        all_keypoints = yolo_results.keypoints.xy.cpu().numpy()
        
        if yolo_results.keypoints.conf is not None:
            all_confs = yolo_results.keypoints.conf.cpu().numpy()
        else:
            all_confs = np.ones((len(all_keypoints), 17))

        people = []
        for i in range(len(all_keypoints)):
            person_kps = all_keypoints[i]
            person_conf = all_confs[i]
            
            # FAILSAFE 3: Prevent the "index 0 out of bounds" crash 
            # if the person array collapses
            if len(person_kps) < 17:
                continue
                
            person_dict = {}
            for name, idx in self.kp_map.items():
                person_dict[name] = {
                    'x': person_kps[idx][0] / w,
                    'y': person_kps[idx][1] / h,
                    'visibility': person_conf[idx]
                }

            person_dict['spine'] = {
                'x': np.mean([person_dict['left_shoulder']['x'], person_dict['right_shoulder']['x'], 
                              person_dict['left_hip']['x'], person_dict['right_hip']['x']]),
                'y': np.mean([person_dict['left_shoulder']['y'], person_dict['right_shoulder']['y'], 
                              person_dict['left_hip']['y'], person_dict['right_hip']['y']]),
                'visibility': min(person_dict['left_shoulder']['visibility'], person_dict['left_hip']['visibility'])
            }
            people.append(person_dict)

        for person in people:
            y_coords = [
                person['left_shoulder']['y'], person['right_shoulder']['y'],
                person['left_hip']['y'], person['right_hip']['y']
            ]
            y_variance = max(y_coords) - min(y_coords)
            
            if y_variance < 0.20:
                extracted_data['patient'] = person
            else:
                if extracted_data['caretaker'] is None:
                    extracted_data['caretaker'] = person

        return extracted_data