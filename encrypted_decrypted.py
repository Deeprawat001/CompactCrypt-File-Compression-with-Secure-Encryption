from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

HEADER = b"HENC"
BLOCK_SIZE = 16

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt_file(input_file, output_file, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    plaintext = HEADER + plaintext
    padded = pad(plaintext)
    ciphertext = cipher.encrypt(padded)
    with open(output_file, 'wb') as f:
        f.write(salt + iv + ciphertext)
    print("Encryption successful ->", output_file)

def decrypt_file(input_file, output_file, password):
    try:
        with open(input_file, 'rb') as f:
            salt = f.read(16)
            iv = f.read(16)
            ciphertext = f.read()
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        unpadded = unpad(decrypted)
        if not unpadded.startswith(HEADER):
            raise ValueError("Invalid password or file corrupted")
        original_data = unpadded[len(HEADER):]
        with open(output_file, 'wb') as f:
            f.write(original_data)
        print("Decryption successful ->", output_file)
        return True  # ✅ success
    except Exception as e:
        print("Decryption failed: Wrong password or corrupted file!")
        return False  # ❌ failure

if __name__ == "__main__":
    print("Secure File Encryptor")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Enter choice: ")
    password = input("Enter password: ")
    if choice == '1':
        encrypt_file("compressed.bin", "encrypted.bin", password)
    elif choice == '2':
        decrypt_file("encrypted.bin", "decrypted.bin", password)
    else:
        print("Invalid choice")
