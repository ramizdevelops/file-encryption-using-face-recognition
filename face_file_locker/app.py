# app.py
from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
import pickle
import base64
from cryptography.fernet import Fernet
import zipfile
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"
DECRYPTED_FOLDER = "decrypted"
TEMP_FOLDER = "temp"
FACE_DATA_FILE = "face_data.pkl"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

FACE_THRESHOLD = 23000

# Utility function to decode base64 image
def decode_base64_image(data_url):
    header, encoded = data_url.split(",")
    img_data = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img

# Resize and flatten face image
def process_face_image(img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    for (x, y, w, h) in faces:
        face_crop = img[y:y+h, x:x+w]
        face_resized = cv2.resize(face_crop, (100, 100)).flatten()
        return face_resized
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register_face", methods=["POST"])
def register_face():
    data = request.json
    image_data = data.get("image")
    img = decode_base64_image(image_data)
    processed = process_face_image(img)
    if processed is not None:
        with open(FACE_DATA_FILE, "wb") as f:
            pickle.dump(processed, f)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Face not detected."})

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if FACE_DATA_FILE not in os.listdir():
        return jsonify({"success": False, "error": "No face registered."})

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    key = Fernet.generate_key()
    cipher = Fernet(key)

    with open(filepath, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())

    encrypted_filename = file.filename + ".enc"
    encrypted_path = os.path.join(TEMP_FOLDER, encrypted_filename)
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    zip_name = file.filename + "_protected.zip"
    zip_path = os.path.join(ENCRYPTED_FOLDER, zip_name)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(encrypted_path, encrypted_filename)
        zipf.write(FACE_DATA_FILE)
        with open(os.path.join(TEMP_FOLDER, "secret.key"), "wb") as kf:
            kf.write(key)
        zipf.write(os.path.join(TEMP_FOLDER, "secret.key"), "secret.key")

    os.remove(encrypted_path)
    os.remove(filepath)
    os.remove(os.path.join(TEMP_FOLDER, "secret.key"))

    return send_file(zip_path, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        data = request.form
        image_data = data.get("image")
        zip_file = request.files['file']

        zip_path = os.path.join(TEMP_FOLDER, zip_file.filename)
        zip_file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(TEMP_FOLDER)

        with open(os.path.join(TEMP_FOLDER, "face_data.pkl"), "rb") as f:
            reference_face = pickle.load(f)

        uploaded_face = process_face_image(decode_base64_image(image_data))
        if uploaded_face is None:
            shutil.rmtree(TEMP_FOLDER)
            os.makedirs(TEMP_FOLDER, exist_ok=True)
            return jsonify({"success": False, "error": "Face not detected."}), 400

        similarity = np.linalg.norm(reference_face - uploaded_face)
        if similarity >= FACE_THRESHOLD:
            shutil.rmtree(TEMP_FOLDER)
            os.makedirs(TEMP_FOLDER, exist_ok=True)
            return jsonify({"success": False, "error": "Face mismatch."}), 400

        with open(os.path.join(TEMP_FOLDER, "secret.key"), "rb") as kf:
            key = kf.read()
        cipher = Fernet(key)

        enc_file = next((f for f in os.listdir(TEMP_FOLDER) if f.endswith(".enc")), None)
        if not enc_file:
            raise Exception("Encrypted file not found.")

        decrypted_path = os.path.join(DECRYPTED_FOLDER, enc_file.replace(".enc", ""))

        with open(os.path.join(TEMP_FOLDER, enc_file), "rb") as ef:
            decrypted_data = cipher.decrypt(ef.read())

        with open(decrypted_path, "wb") as df:
            df.write(decrypted_data)

        shutil.rmtree(TEMP_FOLDER)
        os.makedirs(TEMP_FOLDER, exist_ok=True)

        return send_file(decrypted_path, as_attachment=True)

    except Exception as e:
        print("❌ Exception:", e)  # This will show up in the terminal
        return jsonify({"success": False, "error": str(e)}), 500
