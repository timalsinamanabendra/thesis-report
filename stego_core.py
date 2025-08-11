# stego_core.py
import cv2
import numpy as np
import random

_SENTINEL = "#####"

def _message_to_bits(message: str) -> str:
    data = (message + _SENTINEL).encode("utf-8")
    return "".join(format(b, "08b") for b in data)

def _bits_to_message(bits: str) -> str:
    # Consume bits in groups of 8 -> bytes
    bytes_list = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        bytes_list.append(int(chunk, 2))
    try:
        msg = bytes(bytes_list).decode("utf-8", errors="ignore")
    except Exception:
        msg = ""
    return msg.split(_SENTINEL)[0]

def _xor_bits(bits: str, key: int) -> str:
    random.seed(key)
    return "".join(str(int(b) ^ random.randint(0, 1)) for b in bits)

def _embed_bits_into_image(img: np.ndarray, bits: str) -> np.ndarray:
    h, w, c = img.shape
    capacity = h * w * c
    if len(bits) > capacity:
        raise ValueError("Message too long for selected image (capacity exceeded).")
    flat = img.flatten()
    bits_list = list(map(int, bits))
    flat[:len(bits_list)] = (flat[:len(bits_list)] & 0xFE) | bits_list
    return flat.reshape(img.shape)

def _extract_bits_from_image(img: np.ndarray) -> str:
    flat = img.flatten()
    return "".join(str(pixel & 1) for pixel in flat)

def encode_image(image_path: str, message: str, key: int) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read image. Please select a valid image file.")
    bits = _message_to_bits(message)
    enc_bits = _xor_bits(bits, key)
    stego = _embed_bits_into_image(img, enc_bits)
    return stego

def decode_image(image_path: str, key: int) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read stego image. Please select a valid image file.")
    bits = _extract_bits_from_image(img)
    dec_bits = _xor_bits(bits, key)
    return _bits_to_message(dec_bits)
# stego_core.py
import cv2
import numpy as np
import random

_SENTINEL = "#####"

def _message_to_bits(message: str) -> str:
    data = (message + _SENTINEL).encode("utf-8")
    return "".join(format(b, "08b") for b in data)

def _bits_to_message(bits: str) -> str:
    # Consume bits in groups of 8 -> bytes
    bytes_list = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        bytes_list.append(int(chunk, 2))
    try:
        msg = bytes(bytes_list).decode("utf-8", errors="ignore")
    except Exception:
        msg = ""
    return msg.split(_SENTINEL)[0]

def _xor_bits(bits: str, key: int) -> str:
    random.seed(key)
    return "".join(str(int(b) ^ random.randint(0, 1)) for b in bits)

def _embed_bits_into_image(img: np.ndarray, bits: str) -> np.ndarray:
    h, w, c = img.shape
    capacity = h * w * c
    if len(bits) > capacity:
        raise ValueError("Message too long for selected image (capacity exceeded).")
    flat = img.flatten()
    bits_list = list(map(int, bits))
    flat[:len(bits_list)] = (flat[:len(bits_list)] & 0xFE) | bits_list
    return flat.reshape(img.shape)

def _extract_bits_from_image(img: np.ndarray) -> str:
    flat = img.flatten()
    return "".join(str(pixel & 1) for pixel in flat)

def encode_image(image_path: str, message: str, key: int) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read image. Please select a valid image file.")
    bits = _message_to_bits(message)
    enc_bits = _xor_bits(bits, key)
    stego = _embed_bits_into_image(img, enc_bits)
    return stego

def decode_image(image_path: str, key: int) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read stego image. Please select a valid image file.")
    bits = _extract_bits_from_image(img)
    dec_bits = _xor_bits(bits, key)
    return _bits_to_message(dec_bits)
