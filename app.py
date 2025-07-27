from flask import Flask, request, send_file, jsonify
import os
import tempfile
import gzip
from encrypted_decrypted import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
from flask import Flask, request, send_file, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("index.html")
def cleanup_file(path):
    """Helper function to remove files safely."""
    if os.path.exists(path):
        os.remove(path)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        file = request.files['file']
        password = request.form.get('password', '').strip()

        if not password:
            return jsonify({"error": "Password is required for encryption"}), 400
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            file.save(temp_input.name)
            output_path = temp_input.name + "_enc"
            encrypt_file(temp_input.name, output_path, password)
        
        response = send_file(output_path, as_attachment=True, download_name="encrypted.bin")
        cleanup_file(temp_input.name)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        file = request.files['file']
        password = request.form.get('password', '').strip()

        if not password:
            return jsonify({"error": "Password is required for decryption"}), 400

        original_filename = file.filename 
        decrypted_filename = original_filename + ".dec" 

        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            file.save(temp_input.name)
            output_path = temp_input.name + "_dec"

            success = decrypt_file(temp_input.name, output_path, password)
            if not success:
                return jsonify({"error": "Wrong password"}), 400

        response = send_file(output_path, as_attachment=True, download_name=decrypted_filename)
        cleanup_file(temp_input.name)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/compress", methods=["POST"])
def compress_file():
    try:
        file = request.files["file"]
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            file.save(temp_input.name)
            compressed_filepath = temp_input.name + ".gz"
            
            with open(temp_input.name, "rb") as f_in, gzip.open(compressed_filepath, "wb") as f_out:
                f_out.writelines(f_in)
        
        response = send_file(compressed_filepath, as_attachment=True, download_name="compressed.gz")
        cleanup_file(temp_input.name)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/decompress", methods=["POST"])
def decompress_file():
    try:
        file = request.files["file"]
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            file.save(temp_input.name)
            temp_input_path = temp_input.name  # Save path
        

       
        decompressed_filepath = temp_input_path + "_decompressed"

        # Decompress
        with gzip.open(temp_input_path, "rb") as f_in, open(decompressed_filepath, "wb") as f_out:
            f_out.writelines(f_in)

        # Return file
        response = send_file(decompressed_filepath, as_attachment=True, download_name="decompressed.txt")

        # Cleanup
        cleanup_file(temp_input_path)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
