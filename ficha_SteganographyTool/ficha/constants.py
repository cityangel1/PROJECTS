# ficha/constants.py
BACKGROUND_COLOR = "#FFF1E6"
TEXT_COLOR = "#a0522d"
ACCENT_COLOR = "#8B4513"

ENCRYPTION_ALGOS = {
    "AES-256-GCM + Argon2id": "Best security (recommended)",
    "AES-256-CBC + PBKDF2": "Good compatibility"
}

STEGO_ALGOS = {
    "Adaptive Randomized LSB": "Most stealthy - random positions + adaptive bit depth",
    "Standard LSB": "Fast but more detectable",
    "LSB with Pixel Shuffling": "Good balance"
}
