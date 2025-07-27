# CompactCrypt

**CompactCrypt** is a simple Python tool that compresses files with **Huffman Encoding** and secures them with **AES Encryption** — keeping your data **small and private**.

---

## 🖼️ Screenshot

![CompactCrypt GUI](https://github.com/Deeprawat001/CompactCrypt-File-Compression-with-Secure-Encryption/blob/4cf708cf835852c1cea6f8be49ca93b99f9f0d5e/Screenshot%202025-07-27%20150701.png)

-  **Top bar:** project title.
-  **Compress File:** Select a file and compress it with Huffman Encoding.
-  **Encrypt File:** Upload a file, enter password, and encrypt using AES.
-  **Decrypt File:** Upload encrypted file, enter password, and decrypt it.
-  **Decompress File:** Restore the original file after decryption.

---

## ⚡ Features

- Compress files (Huffman)
- Encrypt compressed files (AES)
- Decrypt & decompress to original
- Works on any text file

---

## Project Structure

📁 CompactCrypt/<br>
├── compress.py  # Huffman compression & decompression<br>
├── encrypt.py # AES encryption logic<br>
├── decrypt.py # AES decryption logic<br>
├── main.py # Orchestrates the full workflow<br>
├── requirements.txt # Python dependencies<br>
├── README.md # This file!<br>
└── sample_file.txt # Example file to test with<br>

🚀 How It Works<br>
1️⃣ Input: Choose or upload a file (sample_file.txt).<br>
2️⃣ Compress: The file is compressed with Huffman Encoding — size is reduced without losing data.<br>
3️⃣ Encrypt: The compressed output is encrypted using AES for confidentiality.<br>
4️⃣ Decrypt: The encrypted file is decrypted back to compressed form.<br>
5️⃣ Decompress: The original file is fully restored.<br>

Outputs:<br>
compressed.bin<br>
encrypted.bin<br>
decrypted.bin<br>
decompressed.txt<br>


