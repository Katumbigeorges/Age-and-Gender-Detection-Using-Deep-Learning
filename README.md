
# Age and Gender Detection Using Deep Learning

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red.svg)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Introduction

This project implements a **production-ready** web-based application that uses deep learning techniques to detect the age and gender of individuals from uploaded images or live video streams. Built with Flask and modern deep learning frameworks, this tool provides real-time predictions through an intuitive user interface with enhanced security, performance, and user experience.

> **Important Note**: This project is designed for educational and demonstration purposes. Predictions may vary in accuracy depending on image quality, lighting conditions, and facial orientation.

## 🚀 Project Overview

The Age and Gender Detection system demonstrates the practical application of deep learning in computer vision tasks. The project combines powerful neural network architectures with a user-friendly web interface, making advanced AI capabilities accessible through a simple upload-and-predict workflow.

### ✨ Key Features

#### 🖼️ **Image Analysis Capabilities**
- **Real-time age prediction** with 8 age categories
- **Gender classification** (Male/Female)
- **Support for multiple image formats** (PNG, JPG, JPEG, GIF, BMP)
- **Live webcam detection** with real-time processing
- **Batch processing** for uploaded images
- **High-accuracy face detection** using OpenCV DNN

#### 🎨 **Enhanced User Interface**
- **Modern, responsive web interface** with mobile support
- **Drag-and-drop file upload** with visual feedback
- **Live video streaming** for real-time detection
- **Loading indicators** and progress feedback
- **Clear error messages** and user guidance
- **Professional styling** with responsive design

#### 🔧 **Technical Components**
- **Deep learning-based prediction models** (Caffe)
- **Convolutional Neural Network (CNN) architecture**
- **Flask web framework** with modular design
- **Real-time processing capabilities**
- **Production-ready configuration**
- **Comprehensive error handling**
- **Security enhancements**

## 🛠️ Technology Stack

### **Backend**
- **Python 3.6+** with type hints
- **Flask 2.3.3** web framework
- **OpenCV 4.8.1** for computer vision
- **NumPy** for numerical operations
- **Pillow** for image processing

### **Frontend**
- **HTML5** with semantic markup
- **CSS3** with modern styling
- **JavaScript** for interactivity
- **Responsive design** for all devices

### **Model Architecture**
- **OpenCV DNN** for face detection
- **Caffe models** for age and gender prediction
- **CNN-based architecture** for feature extraction
- **Pre-trained models** for high accuracy

## 📋 System Requirements

### **Supported Operating Systems**
- ✅ **Windows** (10/11)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+)
- ✅ **macOS** (10.14+)

### **Hardware Requirements**
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space for models
- **CPU**: Multi-core processor recommended
- **GPU**: Optional (CPU processing supported)

## 🔧 Prerequisites

- **Python 3.6.8** or higher
- **PIP** (Python package manager)
- **Webcam** (for live detection)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 📦 Installation Steps

### **1. Clone the Repository**
```bash
git clone https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning.git
cd Age-and-Gender-Detection-Using-Deep-Learning
```

### **2. Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Or install manually
pip install Flask==2.3.3 opencv-python==4.8.1.78 numpy==1.24.3 Pillow==10.0.1
```

### **3. Verify Model Files**
Ensure the following model files are present:
- `opencv_face_detector.pbtxt`
- `opencv_face_detector_uint8.pb`
- `age_deploy.prototxt`
- `age_net.caffemodel`
- `gender_deploy.prototxt`
- `gender_net.caffemodel`

### **4. Run the Application**
```bash
# Development mode
python app.py

# Production mode
export FLASK_ENV=production
python app.py
```

### **5. Access the Application**
Open your browser and navigate to:
- **Local**: `http://localhost:5000`
- **Network**: `http://0.0.0.0:5000`

## 🎯 Usage Guide

### **Live Detection**
1. Click **"Go live to detect"** on the main page
2. Allow camera access when prompted
3. Position your face in front of the camera
4. View real-time age and gender predictions

### **Photo Upload**
1. Click **"Photo"** tab on the main page
2. Select an image file (PNG, JPG, JPEG, GIF, BMP)
3. Click **"Upload and detect"**
4. View the processed image with predictions

### **API Endpoints**
- `GET /` - Main application page
- `GET /webcam` - Live detection page
- `GET /upload` - Photo upload page
- `POST /upload` - Process uploaded image
- `GET /video_feed` - Live video stream
- `GET /health` - Health check endpoint

## 🔍 Technical Details

### **Model Architecture**
- **Face Detection**: OpenCV DNN with confidence thresholding
- **Age Prediction**: 8-category classification (0-2, 4-6, 8-12, 15-20, 25-32, 38-43, 48-53, 60-100)
- **Gender Classification**: Binary classification (Male/Female)
- **CNN Architecture**: Pre-trained Caffe models for high accuracy

### **Performance Optimizations**
- **Model Loading**: Loaded once at startup for efficiency
- **Memory Management**: Optimized resource usage
- **Caching**: Model instances cached for reuse
- **Error Recovery**: Graceful handling of edge cases

### **Security Features**
- **File Validation**: Strict file type and size checking
- **Input Sanitization**: Secure handling of user inputs
- **Error Handling**: Comprehensive error management
- **Configuration**: Environment-based settings

## 📊 Project Structure

```
Age-and-Gender-Detection-Using-Deep-Learning/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── models.py             # Model management
├── utils.py              # Utility functions
├── requirements.txt       # Dependencies
├── templates/
│   ├── index.html        # Main page
│   ├── webcam.html       # Live detection
│   └── photo.html        # Photo upload
├── static/
│   └── styles/
│       ├── style.css     # Main styles
│       └── aj.css        # Additional styles
└── README.md             # This file
```

## ⚠️ Limitations

- **Single Face Analysis**: Designed for one face per image
- **Image Quality Dependent**: Accuracy varies with image quality
- **Lighting Sensitivity**: Performance affected by lighting conditions
- **Demographic Variations**: Accuracy may vary across different demographics
- **Age Range Limitations**: Optimized for specific age ranges

## 🚀 Recent Improvements

### **v2.0 Enhancements**
- ✅ **Modular Architecture** with clean code organization
- ✅ **Enhanced Security** with file validation and input sanitization
- ✅ **Performance Optimizations** with efficient model loading
- ✅ **Improved UI/UX** with modern, responsive design
- ✅ **Comprehensive Error Handling** with user-friendly messages
- ✅ **Production Ready** with environment-based configuration
- ✅ **Health Monitoring** with status endpoints
- ✅ **Better Documentation** with detailed guides

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Clone the repository
git clone https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning.git

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Original Author**: [Katumbigeorges](https://github.com/Katumbigeorges)
- **OpenCV Community** for computer vision tools
- **Flask Community** for the web framework
- **Contributors** who helped improve this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning/discussions)
- **Documentation**: [Project Wiki](https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning/wiki)

---

⭐ **If you find this project helpful, please consider giving it a star on [GitHub](https://github.com/Katumbigeorges/Age-and-Gender-Detection-Using-Deep-Learning)!**

🔗 **Check out our [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed information about recent enhancements.**
