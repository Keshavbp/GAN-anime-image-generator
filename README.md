# GAN Anime Image Generator

This project is a Flask-based web application that generates 64x64 anime-style images using a Generative Adversarial Network (GAN) built with PyTorch. It scales generated images to 512x512 and directly streams them to the frontend using Base64 encoding.

## Features
- Deep Convolutional Generative Adversarial Network (DCGAN) generating images from random noise.
- Flask backend exposing a REST API endpoint for image generation.
- Responsive web interface to seamlessly visualize the generated anime images.

## Project Structure
```text
.
├── app.py                  # Main Flask application and PyTorch Generator architecture
├── models/                 # Directory containing the saved PyTorch model weights (e.g., netG_epoch_0.pth)
├── static/                 # Static assets (CSS, JS)
├── templates/              # HTML templates (index.html)
└── requirements.txt        # (Optional) Python dependencies
```

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8+
- PyTorch
- Flask
- Pillow
- NumPy

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Keshavbp/GAN-anime-image-generator.git
   cd GAN-anime-image-generator
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   If you have a `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   If not, manually install the required libraries:
   ```bash
   pip install torch torchvision numpy flask pillow
   ```

## Ensuring the Model Exists
Make sure your pre-trained generator weights are placed inside the `models/` folder. The application expects to find the weights at `models/netG_epoch_0.pth`.

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

3. Click the "Generate" button on the web interface to request a new anime image from the model.

## Troubleshooting
- **No Model Found:** If you encounter `FileNotFoundError` for the model weights, make sure that `models/netG_epoch_0.pth` exists in the project root.
- **CUDA/GPU issues:** The script automatically attempts to use a CUDA-enabled GPU if available. If none is found, it will default to CPU inference without any required code changes.
