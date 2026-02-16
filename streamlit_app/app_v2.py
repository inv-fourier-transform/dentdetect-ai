import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.model_helper import predict_damage
import streamlit as st
import os

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="🚗 DentDetect AI | Smart Vehicle Damage Assessment",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Theme-Aware CSS - Works in both Light & Dark modes
# -------------------------------------------------
theme_css = """
<style>
    :root {
        --primary-color: #ff6b6b;
        --secondary-color: #4ecdc4;
        --accent-color: #45b7d1;
    }

    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }

    .brand-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(78,205,196,0.1) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(128,128,128,0.2);
    }

    .brand-logo {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }

    .brand-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }

    .brand-tagline {
        color: #6b7280;
        font-size: 1rem;
        font-weight: 500;
    }

    .upload-container {
        background: rgba(128,128,128,0.05);
        border: 2px dashed rgba(128,128,128,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .upload-container:hover {
        border-color: #ff6b6b;
        background: rgba(255,107,107,0.05);
    }

    .result-card {
        background: rgba(128,128,128,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border-left: 5px solid #4ecdc4;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .prediction-label {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }

    .prediction-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: inherit;
    }

    .damage-severe {
        border-left-color: #ef4444;
    }

    .damage-moderate {
        border-left-color: #f59e0b;
    }

    .damage-minor {
        border-left-color: #10b981;
    }

    .footer-disclaimer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(128,128,128,0.2);
        font-style: italic;
        color: #9ca3af;
        font-size: 0.85rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(128,128,128,0.3);
        border-radius: 4px;
    }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# -------------------------------------------------
# Brand Header with Logo
# -------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div class="brand-logo">🚗🔍</div>
    <h1 class="brand-title">DentDetect AI</h1>
    <p class="brand-tagline">Smart Vehicle Damage Assessment & Analysis</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Main Content
# -------------------------------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

with st.container():
    st.info("📤 Upload a vehicle image to instantly detect and assess damage severity.")

uploaded_image = st.file_uploader(
    "📸 Choose a vehicle image (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear image of the vehicle damage for accurate assessment"
)

if uploaded_image:
    image_path = "temp_file.jpg"

    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("##### 📷 Uploaded Image")
        st.image(uploaded_image, use_container_width=True, caption="Vehicle Image")

    with st.spinner("🔍 Analyzing damage..."):
        damage_prediction = predict_damage(image_path)

    prediction_lower = str(damage_prediction).lower()

    # Explicit mapping based on your labels:
    # - "Normal"  -> green dot, green left border
    # - "Breakage"/"Crushed" -> red dot, red left border
    if "normal" in prediction_lower:
        severity_class = "damage-minor"
        severity_emoji = "🟢"
    elif "breakage" in prediction_lower or "crushed" in prediction_lower:
        severity_class = "damage-severe"
        severity_emoji = "🔴"
    else:
        # Fallback for any other labels
        severity_class = "damage-moderate"
        severity_emoji = "🟡"

    with col2:
        st.markdown("##### 🎯 Assessment Result")
        st.markdown(
            f"""
            <div class="result-card {severity_class}">
                <div class="prediction-label">Detected Condition</div>
                <div class="prediction-value">{severity_emoji} {damage_prediction}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("✅ Analysis complete using AI-powered computer vision")

    if os.path.exists(image_path):
        os.remove(image_path)

else:
    st.markdown(
        """
        <div class="upload-container">
            <h3>📸 Drop your image here</h3>
            <p>or click to browse files</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("💡 Tips for best results"):
        st.markdown(
            """
            - 📷 Ensure good lighting conditions  
            - 🎯 Capture the damaged area clearly  
            - 📐 Include multiple angles if possible  
            - 🔍 Avoid blurry or obstructed images
            """
        )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Footer Disclaimer
# -------------------------------------------------
st.markdown(
    """
<div class="footer-disclaimer">
    <p>📝 <em>Disclaimer: The images used to train this model belong to their respective owners. 
    This tool is for assessment purposes only and does not constitute an official insurance evaluation.</em></p>
    <p style="margin-top: 0.5rem; font-size: 0.75rem;">
        © 2026 DentDetect AI. All rights reserved.
    </p>
</div>
""",
    unsafe_allow_html=True,
)
