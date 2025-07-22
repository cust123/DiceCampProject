from flask import Flask, render_template, request
import os, requests, hashlib
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from flask import request as flask_request


load_dotenv()

app = Flask(__name__)
DATA_DIR = os.getenv("DATA_DIR", "/clientdata")
FILE_PATH = os.path.join(DATA_DIR, "received.txt")
FILENAME = "received.txt"
SERVER_URL = os.getenv("SERVER_HOST", "http://server:5001")
MONGO_URI = os.getenv("MONGO_URI")
try:
        client = MongoClient(MONGO_URI)
        db= client["Devops-user"]
        client.admin.command("ping")
        print("connection to MongoDB successful")
except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        
# db = client.filelogs




@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
def fetch():
    meta = requests.get(f"{SERVER_URL}/generate").json()
    checksum = meta["checksum"]

    r = requests.get(f"{SERVER_URL}/file")
    with open(FILE_PATH, "wb") as f:
        f.write(r.content)

    actual = hashlib.sha256(r.content).hexdigest()
    status = "Success" if actual == checksum else "Failed"

    db.logs.insert_one({
        "timestamp": datetime.utcnow(),
        "filename": FILENAME,
        "checksum": checksum,
        "verified": actual == checksum,
        "status": status,
        "client_ip": flask_request.remote_addr or "unknown"
    })

    return render_template("index.html", status=status, checksum=checksum)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
