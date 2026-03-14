# ai_model.py
import requests
from pyngrok import ngrok
from fastapi import FastAPI, UploadFile, File
import threading
import ollama
import time
import os

# ---------------------------
# Start FastAPI + ngrok inside Python
# ---------------------------
app = FastAPI()

# Set ngrok auth token if available
authtoken = os.environ.get("NGROK_AUTHTOKEN")
if authtoken:
    ngrok.set_auth_token(authtoken)

# --- API ENDPOINT ---
@app.post("/analyze")
async def analyze_waste_api(file: UploadFile = File(...)):
    temp_file = os.path.join("temp", f"{os.path.basename(file.filename)}")
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    prompt = """
    You are an AI system for Smart Waste Management.

    Analyze the uploaded waste image and produce a professional report.

    Return the output in Markdown format.

    # 🧠 Smart Waste Analysis Report

    ### 🔍 Detected Item
    Provide the name of the waste item detected.

    ### ♻ Context-Aware Waste Classification
    Explain which waste category it belongs to:
    - Organic
    - Recyclable
    - Hazardous
    - E-Waste
    - Landfill

    ### 🧾 AI Explanation Layer
    Explain how the AI identified the object using visible characteristics.

    ### 🌍 Environmental Impact Feedback
    Explain the environmental impact if disposed incorrectly.

    ### 🔋 Energy Recovery Potential
    Explain if the waste can be converted to energy or reused.

    Make the explanation clear, concise, and professional.
    Only return the formatted report.
    """

    response = ollama.chat(
        model="minicpm-v",
        messages=[{"role": "user", "content": prompt, "images": [temp_file]}],
        options={"num_predict": 150}
    )

    return {"report": response["message"]["content"]}


# ---------------------------
# Function to run FastAPI in a thread
# ---------------------------
def start_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ---------------------------
# Start FastAPI and ngrok automatically
# ---------------------------
# Start FastAPI in a background thread
threading.Thread(target=start_api, daemon=True).start()

# Give FastAPI some time to start
time.sleep(2)

# Start ngrok tunnel
tunnels = ngrok.get_tunnels()
if not tunnels:
    NGROK_URL = ngrok.connect(8000, "http").public_url + "/analyze"
else:
    NGROK_URL = tunnels[0].public_url + "/analyze"

print(f"Ngrok public URL: {NGROK_URL}")


# ---------------------------
# Function Streamlit will call
# ---------------------------
def analyze_waste(image_path):
    """Send the image to the internal Ollama API via ngrok"""
    with open(image_path, "rb") as f:
        files = {"file": (image_path, f, "image/jpeg")}
        response = requests.post(NGROK_URL, files=files)

    if response.status_code == 200:
        return response.json()["report"]
    else:
        return f"Error: {response.status_code} - {response.text}"
