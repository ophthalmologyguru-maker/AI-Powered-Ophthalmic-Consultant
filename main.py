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

/* Share Button */
.share-btn a {
    text-decoration: none;
    background-color: #25D366;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 15px;
}

/* Button Styling */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
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
        for i
