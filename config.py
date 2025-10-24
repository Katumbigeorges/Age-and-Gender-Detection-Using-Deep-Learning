"""
Configuration settings for the Age and Gender Detection application
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Upload settings
    UPLOAD_FOLDER = './UPLOAD_FOLDER'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # Model settings
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    FACE_CONFIDENCE_THRESHOLD = 0.7
    FACE_PADDING = 20
    
    # Age and gender categories
    AGE_CATEGORIES = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
                     '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    GENDER_CATEGORIES = ['Male', 'Female']
    
    # Model file paths
    FACE_PROTO = "opencv_face_detector.pbtxt"
    FACE_MODEL = "opencv_face_detector_uint8.pb"
    AGE_PROTO = "age_deploy.prototxt"
    AGE_MODEL = "age_net.caffemodel"
    GENDER_PROTO = "gender_deploy.prototxt"
    GENDER_MODEL = "gender_net.caffemodel"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
