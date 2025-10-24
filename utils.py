"""
Utility functions for the Age and Gender Detection application
"""

import os
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def create_upload_folder():
    """Create upload folder if it doesn't exist"""
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def validate_image_file(file):
    """Validate uploaded image file"""
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"Invalid file type. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    
    # Check file size (handled by Flask MAX_CONTENT_LENGTH)
    return True, "File is valid"

def format_age_gender_result(gender, age):
    """Format age and gender result for display"""
    age_range = age[1:-1] if age.startswith('(') and age.endswith(')') else age
    return f"{gender}, {age_range} years"
