from flask import Flask, jsonify, send_file
import os, random, string, hashlib

app = Flask(__name__)
DATA_DIR = "/serverdata"
FILE_NAME = "data.txt"
FILE_PATH = os.path.join(DATA_DIR, FILE_NAME)

@app.route("/generate", methods=["GET"])
def generate_file():
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
    with open(FILE_PATH, "w") as f:
        f.write(data)

    with open(FILE_PATH, "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()

    return jsonify({
        "message": "File generated",
        "checksum": checksum,
        "file_path": FILE_PATH
    })

@app.route("/file", methods=["GET"])
def get_file():
    return send_file(FILE_PATH, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5001)
