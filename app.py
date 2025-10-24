"""
Age and Gender Detection Web Application

A Flask-based web application that uses deep learning models to detect
age and gender from images and live video streams.

Author: Katumbigeorges (Original)
Improved by: AI Assistant
"""

import cv2
import numpy as np
import argparse
import os
import logging
from flask import Flask, render_template, Response, request, jsonify, flash, redirect, url_for
from PIL import Image
import io

# Import custom modules
from config import config, Config
from models import model_manager
from utils import allowed_file, create_upload_folder, validate_image_file, format_age_gender_result

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])


# Legacy functions for backward compatibility
def highlightFace(net, frame, conf_threshold=0.7):
    """Legacy function - use model_manager.detect_faces instead"""
    return model_manager.detect_faces(frame, conf_threshold)

def predict_age_gender(face, age_net, gender_net):
    """Legacy function - use model_manager.predict_age_gender instead"""
    return model_manager.predict_age_gender(face)


# Gives input img to the prg for detection.
# Using argparse library which was imported.
parser = argparse.ArgumentParser()
# If the input argument is not given it will skip this and open webcam for detection
parser.add_argument('--image')

args = parser.parse_args()

'''
Each model comes with two files: weight file and model file
weight file stores the data of the deployment of the model
model file stores actual predication done by the model
We are using pre trained models 

The .prototxt file(s) which define the model architecture (i.e., the layers themselves)
The .caffemodel file which contains the weights for the actual layers
Both files are required when using models trained using Caffe for deep learning.
'''

def gen_frames():
    """Generate video frames for live detection"""
    if not model_manager.is_loaded():
        logger.error("Models not loaded")
        return
    
    try:
        video = cv2.VideoCapture(0)
        if not video.isOpened():
            logger.error("Could not open camera")
            return
            
        padding = Config.FACE_PADDING
        
        while True:
            hasFrame, frame = video.read()
            if not hasFrame:
                break

            # Detect faces
            resultImg, faceBoxes = model_manager.detect_faces(frame)
            
            if not faceBoxes:
                logger.info("No face detected")
            else:
                for faceBox in faceBoxes:
                    # Extract face region
                    face = frame[max(0, faceBox[1]-padding):
                               min(faceBox[3]+padding, frame.shape[0]-1), 
                               max(0, faceBox[0]-padding):
                               min(faceBox[2]+padding, frame.shape[1]-1)]

                    # Predict age and gender
                    gender, age = model_manager.predict_age_gender(face)
                    logger.info(f'Gender: {gender}, Age: {age[1:-1]} years')

                    # Draw prediction on frame with enhanced styling
                    result_text = format_age_gender_result(gender, age)
                    
                    # Calculate text size for background rectangle
                    font_scale = 0.8
                    thickness = 2
                    (text_width, text_height), baseline = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                    
                    # Draw background rectangle for better text visibility
                    padding = 10
                    cv2.rectangle(resultImg, 
                                 (faceBox[0] - padding, faceBox[1] - text_height - baseline - padding*2),
                                 (faceBox[0] + text_width + padding, faceBox[1] - padding),
                                 (0, 0, 0), -1)  # Black background
                    
                    # Draw text with better contrast
                    cv2.putText(resultImg, result_text, 
                               (faceBox[0], faceBox[1] - baseline - padding), 
                               cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), thickness, cv2.LINE_AA)

            if resultImg is None:
                continue

            ret, encodedImg = cv2.imencode('.jpg', resultImg)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImg) + b'\r\n')
                   
    except Exception as e:
        logger.error(f"Error in gen_frames: {str(e)}")
    finally:
        if 'video' in locals():
            video.release()


def process_image(img_file):
    """Process uploaded image and return annotated result"""
    if not model_manager.is_loaded():
        logger.error("Models not loaded")
        return None
    
    try:
        # Convert PIL image to OpenCV format
        frame = cv2.cvtColor(img_file, cv2.COLOR_RGB2BGR)
        padding = Config.FACE_PADDING
        
        # Detect faces
        resultImg, faceBoxes = model_manager.detect_faces(frame)
        
        if not faceBoxes:
            logger.info("No face detected in uploaded image")
            # Return original image with "No face detected" message
            cv2.putText(resultImg, "No face detected", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            for faceBox in faceBoxes:
                # Extract face region
                face = frame[max(0, faceBox[1]-padding):
                           min(faceBox[3]+padding, frame.shape[0]-1), 
                           max(0, faceBox[0]-padding):
                           min(faceBox[2]+padding, frame.shape[1]-1)]

                # Predict age and gender
                gender, age = model_manager.predict_age_gender(face)
                logger.info(f'Gender: {gender}, Age: {age[1:-1]} years')

                # Draw prediction on frame with enhanced styling
                result_text = format_age_gender_result(gender, age)
                
                # Calculate text size for background rectangle
                font_scale = 0.8
                thickness = 2
                (text_width, text_height), baseline = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                
                # Draw background rectangle for better text visibility
                padding = 10
                cv2.rectangle(resultImg, 
                             (faceBox[0] - padding, faceBox[1] - text_height - baseline - padding*2),
                             (faceBox[0] + text_width + padding, faceBox[1] - padding),
                             (0, 0, 0), -1)  # Black background
                
                # Draw text with better contrast
                cv2.putText(resultImg, result_text, 
                           (faceBox[0], faceBox[1] - baseline - padding), 
                           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), thickness, cv2.LINE_AA)

        # Encode result image
        ret, encodedImg = cv2.imencode('.jpg', resultImg)
        return encodedImg.tobytes()
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return None


@app.route('/')
def index():
    """Main page with options for live detection or photo upload"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route for live detection"""
    if not model_manager.is_loaded():
        return "Models not loaded. Please check the server logs.", 500
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    """Webcam detection page"""
    return render_template('webcam.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and processing"""
    if request.method == 'GET':
        return render_template('photo.html')
    
    if request.method == 'POST':
        # Validate file upload
        is_valid, message = validate_image_file(request.files.get('fileToUpload'))
        if not is_valid:
            flash(message)
            return redirect(request.url)
        
        file = request.files['fileToUpload']
        
        try:
            # Read and process image
            file_data = file.read()
            img = Image.open(io.BytesIO(file_data))
            img_array = np.asarray(img, dtype="uint8")
            
            # Process image
            result_bytes = process_image(img_array)
            
            if result_bytes is None:
                flash('Error processing image. Please try again.')
                return redirect(request.url)
            
            # Return processed image
            return Response(result_bytes, mimetype='image/jpeg')
            
        except Exception as e:
            logger.error(f"Error processing uploaded file: {str(e)}")
            flash('Error processing image. Please try again.')
            return redirect(request.url)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if model_manager.is_loaded() else 'unhealthy',
        'models_loaded': model_manager.is_loaded()
    })

if __name__ == '__main__':
    # Load models at startup
    if not model_manager.load_models():
        logger.error("Failed to load models. Exiting.")
        exit(1)
    
    # Create upload folder if it doesn't exist
    create_upload_folder()
    
    logger.info("Starting Flask application...")
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
