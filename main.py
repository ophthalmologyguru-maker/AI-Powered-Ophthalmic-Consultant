import streamlit as st
import base64
import streamlit.components.v1 as components 
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
# 2. STYLING (CSS)
# =========================================================
st.markdown("""
<style>
/* Mobile Padding Fix */
.block-container {
    padding-top: 1rem;
    padding-bottom: 5rem;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Title */
h1 {
    text-align: center;
    font-size: 2.2rem !important;
    color: #0e1117;
}

/* Blinking Animation */
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

/* Disclaimer Box */
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

/* Button Styling */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

/* --- RADIO BUTTON STYLING --- */
/* Hide default radio circle */
div[role="radiogroup"] > label > div:first-child {
    display: none; 
}

/* Base style for buttons */
div[role="radiogroup"] > label {
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-weight: bold;
    color: white !important; 
    transition: all 0.2s ease-in-out;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    opacity: 0.5; 
    transform: scale(0.98);
    border: 2px solid transparent;
}

/* Hover Effect */
div[role="radiogroup"] > label:hover {
    opacity: 0.8;
    transform: scale(1.0);
    cursor: pointer;
}

/* SELECTED State (Bright & Shadowed) */
div[role="radiogroup"] > label:has(input:checked) {
    opacity: 1.0;             
    transform: scale(1.03);   
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3); 
    border: 2px solid white;  
    z-index: 10;
}

/* Specific Colors for Imaging Types */
div[role="radiogroup"] label:nth-child(1) { background-color: #FF5733; } /* OCT Macula */
div[role="radiogroup"] label:nth-child(2) { background-color: #33FF57; } /* OCT ONH */
div[role="radiogroup"] label:nth-child(3) { background-color: #3357FF; } /* Visual Field */
div[role="radiogroup"] label:nth-child(4) { background-color: #FF33A8; } /* Corneal Topo */
div[role="radiogroup"] label:nth-child(5) { background-color: #FFC300; } /* FFA */
div[role="radiogroup"] label:nth-child(6) { background-color: #8E44AD; } /* OCTA */
div[role="radiogroup"] label:nth-child(7) { background-color: #00C3FF; } /* B-Scan */
div[role="radiogroup"] label:nth-child(8) { background-color: #5D6D7E; } /* ERG */
div[role="radiogroup"] label:nth-child(9) { background-color: #D35400; } /* VEP */
div[role="radiogroup"] label:nth-child(10) { background-color: #16A085; } /* EOG */

/* INPUT METHOD SELECTOR STYLING (The 2nd Radio Group) */
/* We target the 2nd radio group specifically to make it look different/cleaner if needed */
/* For now, it will inherit the vibrant button style which is good for visibility */

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. API SETUP
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Missing Secrets (GROQ_API_KEY). Please check Streamlit Settings.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# 4. FUNCTIONS
# =========================================================
def encode_image(file):
    return base64.b64encode(file.getvalue()).decode("utf-8")

def load_reference_text(path="REFERNCE.pdf"):
    try:
        reader = PdfReader(path)
        text = ""
        for i, page in enumerate(reader.pages):
            if i > 50: break
            text += page.extract_text() or ""
        return text[:10000] 
    except:
        return ""

# =========================================================
# 5. MAIN INTERFACE (HEADER)
# =========================================================
st.title("👁️ Masood Alam Shah Eye Diagnostics 🇵🇰")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 5px;'>AI-Powered Ophthalmic Assistant</div>", unsafe_allow_html=True)

# SHARE BUTTON
share_link = "https://wa.me/?text=Check%20out%20Dr.%20Masood's%20Eye%20Diagnostics%20App!"
st.markdown(f"<div style='text-align: center;'><span class='share-btn'><a href='{share_link}' target='_blank'>📲 Share App on WhatsApp</a></span></div>", unsafe_allow_html=True)

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
    unsafe_allow_
