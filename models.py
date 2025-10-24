"""
Model management module for Age and Gender Detection
"""

import cv2
import numpy as np
import logging
import os
try:
    from config import Config
except ImportError:
    # Fallback configuration if config.py is not available
    class Config:
        FACE_PADDING = 20
        FACE_CONFIDENCE_THRESHOLD = 0.7
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        AGE_CATEGORIES = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
                         '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        GENDER_CATEGORIES = ['Male', 'Female']
        FACE_PROTO = "opencv_face_detector.pbtxt"
        FACE_MODEL = "opencv_face_detector_uint8.pb"
        AGE_PROTO = "age_deploy.prototxt"
        AGE_MODEL = "age_net.caffemodel"
        GENDER_PROTO = "gender_deploy.prototxt"
        GENDER_MODEL = "gender_net.caffemodel"

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages loading and using of deep learning models"""
    
    def __init__(self):
        self.face_net = None
        self.age_net = None
        self.gender_net = None
        self.model_loaded = False
        
    def load_models(self):
        """Load all required models"""
        try:
            # Check if model files exist
            model_files = [
                Config.FACE_PROTO, Config.FACE_MODEL,
                Config.AGE_PROTO, Config.AGE_MODEL,
                Config.GENDER_PROTO, Config.GENDER_MODEL
            ]
            
            for file_path in model_files:
                if not os.path.exists(file_path):
                    logger.error(f"Model file not found: {file_path}")
                    return False
            
            # Load networks
            self.face_net = cv2.dnn.readNet(Config.FACE_MODEL, Config.FACE_PROTO)
            self.age_net = cv2.dnn.readNet(Config.AGE_MODEL, Config.AGE_PROTO)
            self.gender_net = cv2.dnn.readNet(Config.GENDER_MODEL, Config.GENDER_PROTO)
            
            self.model_loaded = True
            logger.info("All models loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False
    
    def detect_faces(self, frame, conf_threshold=None):
        """Detect faces in a frame"""
        if not self.model_loaded:
            raise RuntimeError("Models not loaded")
        
        if conf_threshold is None:
            conf_threshold = Config.FACE_CONFIDENCE_THRESHOLD
            
        frame_copy = frame.copy()
        frame_height = frame_copy.shape[0]
        frame_width = frame_copy.shape[1]
        
        # Convert frame to blob for face detection
        blob = cv2.dnn.blobFromImage(frame_copy, 1.0, (300, 300), 
                                   [104, 117, 123], True, False)
        
        # Pass blob through network
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        face_boxes = []
        
        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                # Compute bounding box coordinates
                x1 = int(detections[0, 0, i, 3] * frame_width)
                y1 = int(detections[0, 0, i, 4] * frame_height)
                x2 = int(detections[0, 0, i, 5] * frame_width)
                y2 = int(detections[0, 0, i, 6] * frame_height)
                
                face_boxes.append([x1, y1, x2, y2])
                # Enhanced bounding box with better styling
                box_thickness = max(2, int(round(frame_height/150)))
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2),
                            (0, 255, 0), box_thickness, cv2.LINE_AA)
        
        return frame_copy, face_boxes
    
    def predict_age_gender(self, face):
        """Predict age and gender for a single face"""
        if not self.model_loaded:
            raise RuntimeError("Models not loaded")
        
        # Preprocess face for prediction
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), Config.MODEL_MEAN_VALUES, swapRB=False)
        
        # Predict gender
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = Config.GENDER_CATEGORIES[gender_preds[0].argmax()]
        
        # Predict age
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        age = Config.AGE_CATEGORIES[age_preds[0].argmax()]
        
        return gender, age
    
    def is_loaded(self):
        """Check if models are loaded"""
        return self.model_loaded

# Global model manager instance
model_manager = ModelManager()
