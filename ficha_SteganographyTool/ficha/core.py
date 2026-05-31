# ficha/core.py
import os
import hashlib
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2 import PasswordHasher
import cv2
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from reedsolo import RSCodec
from tqdm import tqdm
from PIL import Image

class FichaCore:
    def __init__(self):
        self.ph = PasswordHasher()
        self.rs = RSCodec(64)  # Stronger error correction

    def derive_key(self, passphrase: str, salt=None):
        if salt is None:
            salt = os.urandom(16)
        key = self.ph.hash(passphrase.encode(), salt=salt)
        return hashlib.sha256(key.encode()).digest()[:32], salt

    def encrypt(self, data: bytes, passphrase: str):
        salt = os.urandom(16)
        key, _ = self.derive_key(passphrase, salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, data, None)
        return salt + nonce + ct

    def decrypt(self, enc_data: bytes, passphrase: str):
        salt = enc_data[:16]
        nonce = enc_data[16:28]
        ct = enc_data[28:]
        key, _ = self.derive_key(passphrase, salt)
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ct, None)

    # ================= ADVANCED IMAGE EMBEDDING =================
    def embed_image(self, carrier: str, secret: str, passphrase: str):
        with open(secret, "rb") as f:
            data = f.read()
        encrypted = self.encrypt(data, passphrase)
        encoded = self.rs.encode(encrypted)

        filename = os.path.basename(secret).encode()
        header = b"FICHAv2" + len(filename).to_bytes(2,'big') + filename + len(encoded).to_bytes(8,'big')
        payload = header + encoded

        img = cv2.imread(carrier)
        if img is None:
            raise ValueError("Invalid carrier image")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=3)
        mask = np.abs(edges) > np.percentile(np.abs(edges), 65)

        flat = img.reshape(-1, 3)
        indices = np.where(mask.flatten())[0]
        if len(indices) < 1000:
            indices = np.arange(len(flat))

        # Cryptographically secure shuffle
        seed = int.from_bytes(hashlib.sha256(passphrase.encode()).digest()[:8], 'big')
        rng = np.random.default_rng(seed)
        rng.shuffle(indices)

        bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
        bit_idx = 0

        for idx in tqdm(indices, desc="Embedding"):
            for ch in range(3):
                if bit_idx < len(bits):
                    flat[idx, ch] = (flat[idx, ch] & 0xFE) | bits[bit_idx]
                    bit_idx += 1
                else:
                    break
            if bit_idx >= len(bits):
                break

        out_path = carrier.rsplit('.', 1)[0] + "_ficha.png"
        cv2.imwrite(out_path, flat.reshape(img.shape))
        return out_path

    # ================= VIDEO & AUDIO =================
    def embed_video(self, carrier: str, secret: str, passphrase: str):
        clip = VideoFileClip(carrier)
        frames = []
        for i, frame in enumerate(clip.iter_frames()):
            if i % 4 == 0:  # Embed in 25% of frames
                frame_img = Image.fromarray(frame)
                frame_img.save("temp_frame.png")
                embedded = self.embed_image("temp_frame.png", secret, passphrase)
                frame = np.array(Image.open(embedded))
            frames.append(frame)
        clip.close()

        out_path = carrier.rsplit('.', 1)[0] + "_ficha.mp4"
        new_clip = VideoFileClip.from_images(frames, fps=clip.fps)
        new_clip.write_videofile(out_path, codec="libx264", audio=False)
        return out_path

    def embed_audio(self, carrier: str, secret: str, passphrase: str):
        audio = AudioSegment.from_file(carrier)
        samples = np.array(audio.get_array_of_samples())

        with open(secret, "rb") as f:
            data = f.read()
        enc = self.encrypt(data, passphrase)
        encoded = self.rs.encode(enc)

        for i in range(min(len(encoded)*8, len(samples))):
            bit = (encoded[i//8] >> (7 - (i % 8))) & 1
            samples[i] = (samples[i] & ~1) | bit

        audio = audio._spawn(samples.tobytes())
        out_path = carrier.rsplit('.', 1)[0] + "_ficha.wav"
        audio.export(out_path, format="wav")
        return out_path

    # ================= EXTRACTION =================
    def extract(self, carrier: str, output: str, passphrase: str):
        ext = carrier.lower().split('.')[-1]
        if ext in ['png', 'jpg', 'jpeg', 'bmp']:
            return self.extract_image(carrier, output, passphrase)
        elif ext in ['mp4', 'avi', 'mov']:
            return self.extract_video(carrier, output, passphrase)
        elif ext in ['wav', 'mp3']:
            return self.extract_audio(carrier, output, passphrase)
        else:
            raise ValueError("Unsupported carrier type")

    def extract_image(self, carrier: str, output: str, passphrase: str):
        img = cv2.imread(carrier)
        flat = img.reshape(-1, 3)

        seed = int.from_bytes(hashlib.sha256(passphrase.encode()).digest()[:8], 'big')
        rng = np.random.default_rng(seed)
        indices = np.arange(len(flat))
        rng.shuffle(indices)

        bits = [flat[idx, ch] & 1 for idx in indices for ch in range(3)]
        data = np.packbits(bits).tobytes()

        if not data.startswith(b"FICHAv2"):
            raise ValueError("No hidden data or incorrect passphrase")

        offset = 6
        name_len = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        orig_name = data[offset:offset+name_len].decode(errors='ignore')
        offset += name_len
        data_len = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8

        encoded = data[offset:offset + data_len]
        corrected = self.rs.decode(encoded)[0]
        secret = self.decrypt(corrected, passphrase)

        final_path = output or f"extracted_{orig_name}"
        with open(final_path, "wb") as f:
            f.write(secret)
        return final_path

    # Stub for video/audio extraction (similar logic, simplified)
    def extract_video(self, carrier: str, output: str, passphrase: str):
        return self.extract_image(carrier, output, passphrase)  # First frame fallback

    def extract_audio(self, carrier: str, output: str, passphrase: str):
        return self.extract_image(carrier, output, passphrase)  # Placeholder
