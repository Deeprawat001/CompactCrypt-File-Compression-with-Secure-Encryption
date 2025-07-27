# CompactCrypt 🔐📦

**CompactCrypt** is a simple Python tool that compresses files with **Huffman Encoding** and secures them with **AES Encryption** — keeping your data **small and private**.

---

## ⚡ Features

- Compress files (Huffman)
- Encrypt compressed files (AES)
- Decrypt & decompress to original
- Works on any text file

---

## Project Structure

📁 CompactCrypt/
├── compress.py # Huffman compression & decompression
├── encrypt.py # AES encryption logic
├── decrypt.py # AES decryption logic
├── main.py # Orchestrates the full workflow
├── requirements.txt # Python dependencies
├── README.md # This file!
└── sample_file.txt # Example file to test with

🚀 How It Works
1️⃣ Input: Choose or upload a file (sample_file.txt).
2️⃣ Compress: The file is compressed with Huffman Encoding — size is reduced without losing data.
3️⃣ Encrypt: The compressed output is encrypted using AES for confidentiality.
4️⃣ Decrypt: The encrypted file is decrypted back to compressed form.
5️⃣ Decompress: The original file is fully restored.

Outputs:
compressed.bin
encrypted.bin
decrypted.bin
decompressed.txt


