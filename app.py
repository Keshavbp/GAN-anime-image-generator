import torch
import torch.nn as nn
import numpy as np
from flask import Flask, render_template, jsonify
import base64
from PIL import Image
import io
import os

app = Flask(__name__)

# Generator matching the checkpoint (outputs 64x64)
class Generator(nn.Module):
    def __init__(self, z_dim=100, channels=3):
        super(Generator, self).__init__()
        self.z_dim = z_dim
        self.main = nn.Sequential(
            nn.ConvTranspose2d(z_dim, 512, 4, 1, 0, bias=False),  # [batch, 512, 4, 4]
            nn.BatchNorm2d(512),
            nn.ReLU(True),
            nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False),    # [batch, 256, 8, 8]
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),   # [batch, 128, 16, 16]
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),    # [batch, 64, 32, 32]
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 3, 4, 2, 1, bias=False),      # [batch, 3, 64, 64]
            nn.Tanh()
        )

    def forward(self, x):
        return self.main(x)

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the Generator
generator = Generator(z_dim=100).to(device)
generator.load_state_dict(torch.load("models/netG_epoch_0.pth", map_location=device))
generator.eval()
print("Model loaded successfully.")

# Function to generate an image
def generate_anime_image():
    with torch.no_grad():
        z = torch.randn(1, 100, 1, 1).to(device)
        print(f"Input z shape: {z.shape}")
        fake_img = generator(z)  # [1, 3, 64, 64]
        print(f"Generated image shape: {fake_img.shape}")
        print(f"Generated image min: {fake_img.min().item()}, max: {fake_img.max().item()}")
        print(f"Generated image mean: {fake_img.mean().item()}")

        # Denormalize and convert to numpy
        fake_img = torch.clamp(fake_img * 0.5 + 0.5, 0.0, 1.0)  # Clamp to [0, 1]
        print(f"Denormalized image min: {fake_img.min().item()}, max: {fake_img.max().item()}")
        print(f"Denormalized image mean: {fake_img.mean().item()}")
        fake_img = fake_img.squeeze(0).permute(1, 2, 0).cpu().numpy()  # [64, 64, 3]
        print(f"Numpy array shape: {fake_img.shape}")
        fake_img = (fake_img * 255).astype(np.uint8)
        print(f"After scaling to uint8 min: {fake_img.min()}, max: {fake_img.max()}")
        print(f"After scaling to uint8 mean: {np.mean(fake_img)}")

        # Resize to 512x512 for frontend
        img = Image.fromarray(fake_img)
        img = img.resize((512, 512), Image.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(f"Base64 string length: {len(img_str)}")
        return img_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    img_base64 = generate_anime_image()
    return jsonify({'image': img_base64})

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)