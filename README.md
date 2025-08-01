# File Encryption & Decryption using Face Recognition

Authors - 
<br>
Ramiz Shaikh
<br>
Neha Singh
<br>
Daksh Meshram
<br>
Amol Nagaonkar
<br>

A web-based file locker that combines **biometric face authentication** with **Fernet encryption** to provide secure encryption and decryption of files — all through a simple and elegant interface.

---

## Features

-  **Face-based authentication** for decryption (no password required)
-  **Fernet symmetric encryption** ensures file confidentiality and integrity
-  Local ZIP archive with encrypted file, face data, and secret key
-  Smart biometric matching using Euclidean distance
-  Face registration and live verification using webcam
-  Fully local — no cloud storage or external APIs required

---

## Technologies Used

Flask
A lightweight Python web framework used to build the backend server, handle routing, and manage HTTP requests.

OpenCV
Handles webcam access and performs face detection using Haar cascades.

NumPy
Used for numerical operations like face vector processing and similarity computation.

Cryptography
Provides Fernet encryption and decryption to securely lock and unlock files.

HTML / CSS / JavaScript
Powers the frontend of the application — the web interface users interact with.

Bootstrap 5
Used for styling and responsive design to ensure the interface works across all devices.

---

## GUI Preview

<p align="center">
  <img src="images/system_architecture.png" alt="System Architecture" width="600">
  <br>
  <em>Figure 1: System Architecture of Face File Locker</em>
</p>

<p align="center">
  <img src="images/flow_chart.png" alt="Project Flow Chart" width="600">
  <br>
  <em>Figure 2: Project Flow Chart</em>
</p>

<p align="center">
  <img src="images/webpage_layout.jpg" alt="Webpage Layout" width="600">
  <br>
  <em>Figure 3: Webpage Layout</em>
</p>

<p align="center">
  <img src="images/Encryption_file_selection.jpg" alt="Encryption File Selection" width="500">
  <br>
  <em>Figure 4: Encryption File Selection</em>
</p>

<p align="center">
  <img src="images/Decryption_file_selection.jpg" alt="Decryption File Selection" width="500">
  <br>
  <em>Figure 5: Decryption File Selection</em>
</p>

<p align="center">
  <img src="images/face_registration.jpg" alt="Face Registration" width="600">
  <br>
  <em>Figure 6: Face Registration</em>
</p>

<p align="center">
  <img src="images/Encryption_of_selected_file.jpg" alt="Encryption of Selected File" width="500">
  <br>
  <em>Figure 7: Encryption of Selected File</em>
</p>

<p align="center">
  <img src="images/saving_encrypted_file.jpg" alt="Saving Encrypted File" width="450">
  <br>
  <em>Figure 8: Saving Encrypted File</em>
</p>

<p align="center">
  <img src="images/decrypted_the_saved_file.jpg" alt="Decrypting and Downloading the Saved File" width="500">
  <br>
  <em>Figure 9: Decrypting and Downloading the Saved File</em>
</p>


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/face-file-locker.git
   cd face-file-locker

2. **Install required libraries**

3. **Run the Application**

   Then open your browser and go to:
   http://127.0.0.1:5000
   
## How it works

Face Registration
Click "Register Face" to open your webcam

Your face is captured and processed into a 100x100 grayscale vector

Stored locally as face_data.pkl for matching

🔹 File Encryption
Upload a file using "Encrypt File"

A random Fernet key is generated

File is encrypted, bundled with the key + face data into a ZIP archive

ZIP is downloaded (e.g., myfile_protected.zip)

🔹 File Decryption
Upload the encrypted ZIP and face image (captured via webcam)

System compares your current face with stored face data using Euclidean distance

If matched:

Secret key is used to decrypt the encrypted file

Decrypted file is available for download

## Security Overview

Biometric Lock: Only the registered face can decrypt files

Face Matching: Done locally using Haar Cascade + distance metric

Fernet Encryption: Strong symmetric encryption with built-in tamper detection

Temporary Folder Cleanup: All temp files are deleted after use

## Project flow

1. Face Registration
     ↓
2. Encrypt File (Face not needed)
     ↓
3. Decrypt File (Face Verification Required)
     ↓
4. Download Decrypted File (if face matches)


## Notes

- Make sure your webcam is working.

- Lighting conditions affect face detection accuracy.

- This project is for educational/demo use, not production-grade security.

## License
This project is licensed under the MIT License.