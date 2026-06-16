import io
from PIL import Image

DELIMITER = "###ONYX_END###"

def text_to_binary(text: str) -> str:
    return ''.join([format(ord(c), "08b") for c in text])

def binary_to_text(binary_str: str) -> str:
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def embed_lsb(image_bytes: bytes, payload: str) -> bytes:
    # Append delimiter to payload
    payload += DELIMITER
    binary_payload = text_to_binary(payload)
    
    img = Image.open(io.BytesIO(image_bytes))
    # We must operate in RGB to use 3 channels.
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())
    
    new_pixels = []
    payload_idx = 0
    payload_len = len(binary_payload)
    
    # Check capacity
    if payload_len > len(pixels) * 3:
        raise ValueError("Image is too small to hold the payload.")
    
    for pixel in pixels:
        r, g, b = pixel
        
        if payload_idx < payload_len:
            r = (r & ~1) | int(binary_payload[payload_idx])
            payload_idx += 1
        if payload_idx < payload_len:
            g = (g & ~1) | int(binary_payload[payload_idx])
            payload_idx += 1
        if payload_idx < payload_len:
            b = (b & ~1) | int(binary_payload[payload_idx])
            payload_idx += 1
            
        new_pixels.append((r, g, b))
        
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    out_io = io.BytesIO()
    # Save as PNG to avoid lossy compression breaking LSB
    new_img.save(out_io, format="PNG")
    return out_io.getvalue()

def extract_lsb(image_bytes: bytes) -> str | None:
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())
    
    binary_str = []
    extracted_text = ""
    
    for pixel in pixels:
        r, g, b = pixel
        binary_str.append(str(r & 1))
        binary_str.append(str(g & 1))
        binary_str.append(str(b & 1))
        
        # Every time we accumulate at least 8 bits, convert to char
        while len(binary_str) >= 8:
            byte = "".join(binary_str[:8])
            binary_str = binary_str[8:]
            
            char = chr(int(byte, 2))
            
            # Since some bits could be junk if interpreted as ascii, only append if valid
            extracted_text += char
            
            if extracted_text.endswith(DELIMITER):
                return extracted_text[:-len(DELIMITER)]
                
    return None # Delimiter not found
