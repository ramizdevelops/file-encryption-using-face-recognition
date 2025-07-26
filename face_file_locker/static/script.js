const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
  video.srcObject = stream;
});

function captureImage() {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0);
  return canvas.toDataURL("image/jpeg");
}

async function registerFace() {
  const image = captureImage();
  const res = await fetch("/register_face", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image })
  });
  const data = await res.json();
  alert(data.success ? "Face registered!" : "Failed: " + data.error);
}

async function encryptFile() {
  const fileInput = document.getElementById("encryptFile");
  if (!fileInput.files.length) return alert("Choose a file first.");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  const res = await fetch("/encrypt", {
    method: "POST",
    body: formData
  });
  if (res.ok) {
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "protected.zip";
    a.click();
  } else {
    alert("Encryption failed.");
  }
}

async function decryptFile() {
    const fileInput = document.getElementById("decryptFile");
    if (!fileInput.files.length) return alert("Choose a zip file.");
    
    // Capture the face image in base64
    const image = captureImage();
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("image", image);  // Append the base64 image to FormData
  
    const res = await fetch("/decrypt", {
      method: "POST",
      body: formData
    });
  
    if (!res.ok) {
      alert("Decryption failed.");
      return;
    }
  
    const data = await res.blob();
    const url = URL.createObjectURL(data);
    const a = document.createElement("a");
    a.href = url;
    a.download = "decrypted_file";
    a.click();
  }
  