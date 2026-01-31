import streamlit as st
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from PyPDF2 import PdfReader

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Masood Alam Shah Eye Diagnostics",
    layout="wide",
    page_icon="👁️"
)

# =========================================================
# 2. STYLING (Animations & Colors)
# =========================================================
st.markdown("""
<style>
/* 1. Mobile Padding Fix */
.block-container {
    padding-top: 1rem;
    padding-bottom: 5rem;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 2. Custom Title */
h1 {
    text-align: center;
    font-size: 2.2rem !important;
    color: #0e1117;
}

/* 3. Blinking Animation for Warning Triangle */
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
.blink-icon {
    animation: blink 1s infinite;
    color: #ff4b4b;
    font-weight: bold;
    font-size: 1.2rem;
}

/* 4. Center the Disclaimer Text */
.disclaimer-box {
    border: 2px solid #ff4b4b;
    border-radius: 10px;
    background-color: #fff8f8;
    padding: 15px;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;
    max-width: 800px;
}

/* 5. Vibrant Colors for Radio Buttons */
div[role="radiogroup"] > label > div:first-child {
    display: none; 
}
div[role="radiogroup"] > label {
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-weight: bold;
    color: white !important; /* FORCED WHITE TEXT */
    transition: transform 0.1s;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}
div[role="radiogroup"] > label:hover {
    transform: scale(1.02);
}

/* Assigning Specific Vibrant Colors to Each Option */
div[role="radiogroup"] > label:nth-child(1) { background-color: #FF5733; } /* OCT Macula - Red/Orange */
div[role="radiogroup"] > label:nth-child(2) { background-color: #33FF57; } /* OCT ONH - Green */
div[role="radiogroup"] > label:nth-child(3) { background-color: #3357FF; } /* Visual Field - Blue */
div[role="radiogroup"] > label:nth-child(4) { background-color: #FF33A8; } /* Corneal Topo - Pink */
div[role="radiogroup"] > label:nth-child(5) { background-color: #FFC300; } /* FFA - Yellow/Gold */
div[role="radiogroup"] > label:nth-child(6) { background-color: #8E44AD; } /* OCTA - Purple */
div[role="radiogroup"] > label:nth-child(7) { background-color: #00C3FF; } /* B-Scan - Cyan */

/* 6. Button Styling */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. API & EMAIL SETUP
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    email_user = st.secrets["EMAIL_USER"]
    email_pass = st.secrets["EMAIL_PASSWORD"]
except KeyError:
    st.error("Missing Secrets (GROQ_API_KEY, EMAIL_USER, or EMAIL_PASSWORD). Please check Streamlit Settings.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# 4. MAIN INTERFACE (HEADER)
# =========================================================
st.title("👁️ Masood Alam Shah Eye Diagnostics 🇵🇰")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 20px;'>AI-Powered Ophthalmic Assistant</div>", unsafe_allow_html=True)

# DISCLAIMER
st.markdown(
    """
    <div class="disclaimer-box">
        <span class="blink-icon">⚠️</span> 
        <strong>AI MEDICAL DISCLAIMER</strong> 
        <span class="blink-icon">⚠️</span>
        <br><br>
        This tool is for <strong>educational support only</strong> and does not constitute a medical diagnosis. 
        <br>
        <strong>Always verify findings with clinical examination.</strong>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# 5. SPLIT LAYOUT (SIDE-BY-SIDE)
# =========================================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.write("### 1. Select Imaging Type")
    modality = st.radio(
        "Tap to select:",
        [
            "OCT Macula",
            "OCT ONH (Glaucoma)",
            "Visual Field (Perimetry)",
            "Corneal Topography",
            "Fluorescein Angiography (FFA)",
            "OCT Angiography (OCTA)",
            "Ultrasound B-Scan"
        ],
        index=0
    )

with col2:
    st.write(f"### 2. Upload {modality} Scan")
    
    ack = st.checkbox("✅ I acknowledge the disclaimer above.")
    
    if ack:
        image_file = st.file_uploader("Tap to select image", type=["jpg", "jpeg", "png"])

        if image_file:
            st.image(image_file, caption="Scan Preview", use_container_width=True)
            
            if st.button("Analyze Scan", type="primary", use_container_width=True):
                with st.spinner("Dr. Masood Alam Shah's AI is analyzing..."):
                    
                    def encode_image(file):
                        return base64.b64encode(file.getvalue()).decode("utf-8")

                    def load_reference_text(path="REFERNCE.pdf"):
                        try:
                            reader = PdfReader(path)
                            text = ""
                            for i, page in enumerate(reader.pages):
                                if i > 50: break
                                text += page.extract_text() or ""
                            return text[:5000]
                        except:
                            return ""

                    SYSTEM_PROMPT = """
                    You are an expert Consultant Ophthalmologist.
                    Analyze the ophthalmic scan professionally.
                    STRICT FORMATTING:
                    **PATIENT DATA:** [Name/ID/Age if visible]
                    **SCAN QUALITY:**
