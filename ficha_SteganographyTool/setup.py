# setup.py
from setuptools import setup, find_packages

setup(
    name="ficha",
    version="1.0.0",
    description="Advanced Steganography Tool for Kali Linux - Hide any file type with strong encryption",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "cryptography>=43.0.0",
        "argon2-cffi>=23.1.0",
        "numpy>=1.26.0",
    ],
    entry_points={
        'console_scripts': [
            'ficha = ficha:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security :: Cryptography",
    ],
)
