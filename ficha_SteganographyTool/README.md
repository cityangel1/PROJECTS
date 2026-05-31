# Ficha - Advanced Steganography Tool

**Ficha** is a powerful, modern steganography application designed for Kali Linux. It allows you to hide **any file type** (images, videos, documents, code, archives, etc.) inside carrier images with military-grade encryption.

## Features

- Hide **any file** inside PNG/JPG images
- AES-256-GCM + Argon2id encryption
- Multiple steganography methods (Adaptive Randomized LSB, etc.)
- Beautiful GUI + Professional CLI
- Strong anti-detection (randomized embedding + shuffling)
- Password confirmation & error handling

## Installation

```bash
# Clone the repository
git clone https://github.com/cityangel1/PROJECTS.git
cd PROJECTS/ficha_SteganographyTool

# Install dependencies
pip3 install -r requirements.txt

# Install the tool
pip3 install -e .

# Make main script executable
chmod +x ficha.py
