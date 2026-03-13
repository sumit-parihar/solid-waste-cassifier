# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ImageEnhance

# ---------------- IMPORT PATH FIX ---------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ai_model.ai_model import analyze_waste

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Smart Waste Classifier",
    page_icon="🗑️",
    layout="wide"
)


# ======================================================
# STYLING
# ======================================================

def load_css():
    st.markdown("""
    <style>
    /* -------- App Background -------- */
    .stApp {
        background: linear-gradient(135deg,#1f2937,#0f172a);
        color: #ffffff;
    }

    /* -------- Main Title -------- */
    .main-title{
        text-align:center;
        font-size:48px;
        font-weight:800;
        background:linear-gradient(90deg,#22c55e,#4ade80);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .subtitle{
        text-align:center;
        font-size:18px;
        color:#e5e7eb;
        margin-bottom:40px;
    }

    /* -------- Card -------- */
    .card{
        background:#111827;
        padding:25px;
        border-radius:14px;
        box-shadow:0 0 20px rgba(0,0,0,0.3);
        border:1px solid rgba(255,255,255,0.08);
    }

    /* -------- File Uploader & Camera Input Fix -------- */
    .stFileUploader, .stCameraInput {
        background-color: #111827 !important;
        padding: 15px !important;
        border-radius: 14px;
    }

    /* Buttons inside uploader and camera input */
    .stFileUploader button, .stCameraInput button {
        background-color: #22c55e !important;
        color: #ffffff !important;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        height: 40px;
    }

    .stFileUploader button:hover, .stCameraInput button:hover {
        background-color: #16a34a !important;
        transform: scale(1.02);
        transition: 0.3s;
    }

    /* Input text inside uploader/camera */
    .stFileUploader input, .stCameraInput input {
        color: #ffffff !important;
    }

    /* -------- Main App Buttons -------- */
    .stButton>button{
        width:100%;
        height:50px;
        border-radius:12px;
        font-size:18px;
        font-weight:600;
        background:linear-gradient(90deg,#22c55e,#16a34a);
        color:white;
        border:none;
        transition:0.3s;
    }

    .stButton>button:hover{
        box-shadow:0 0 15px rgba(34,197,94,0.7);
        transform:scale(1.02);
    }

    /* -------- Image Card -------- */
    .image-card{
        padding:20px;
        border-radius:14px;
        background:#020617;
        border:1px solid rgba(255,255,255,0.05);
        box-shadow:0 0 25px rgba(0,0,0,0.4);
    }
    
    /* -------- AI Response Card -------- */
.response-card{
    margin-top:25px;
    padding:30px;
    border-radius:16px;
    background:linear-gradient(135deg,#020617,#111827);
    border:1px solid rgba(34,197,94,0.25);
    box-shadow:0 0 30px rgba(0,0,0,0.45);
}

.response-title{
    font-size:24px;
    font-weight:700;
    margin-bottom:15px;
    color:#4ade80;
}

.response-content{
    font-size:16px;
    line-height:1.6;
    color:#e5e7eb;
    white-space:pre-wrap;
}

    /* -------- Footer -------- */
    .footer{
        text-align:center;
        color:#cbd5e1;
        font-size:14px;
        margin-top:40px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()


# ======================================================
# UI DESIGN
# ======================================================

st.markdown('<div class="main-title">Smart Waste Classification</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Powered Waste Detection for Smart Recycling ♻</div>', unsafe_allow_html=True)

st.write("")

# Centered layout
left, center, right = st.columns([1, 3, 1])

with center:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📤 Upload Waste Image")

        uploaded_file = st.file_uploader(
            "Upload an image of the waste item",
            type=["jpg", "jpeg", "png"]
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📷 Scan with Camera")

        camera_image = st.camera_input("Take a photo")

        st.markdown('</div>', unsafe_allow_html=True)

st.write("")


# ======================================================
# LOGIC SECTION (UNCHANGED)
# ======================================================

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif camera_image is not None:
    image = Image.open(camera_image)


def preprocess_image(img, max_size=(512, 512), enhance=True):
    img = img.convert("RGB")
    img.thumbnail(max_size)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
    return img


if image is not None:
    image = preprocess_image(image)
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.image(image, caption="Preprocessed Image", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze = st.button("🔍 Analyze")

    if analyze:
        st.info("AI is analyzing the waste item...")

        image_path = "../temp/temp_image.png"
        image.save(image_path)

        result = analyze_waste(image_path)

        st.success("Analysis Complete")

        st.markdown(
            f"""
            <div class="response-card">
                <div class="response-title">🤖 AI Waste Analysis Report</div>
                <div class="response-content">
                {result}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ======================================================
# FOOTER
# ======================================================

st.markdown(
    """
    <div class="footer">
    🌍 Smart Waste Management System | ♻ Sustainable Future
    </div>
    """,
    unsafe_allow_html=True
)
