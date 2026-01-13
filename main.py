import streamlit as st
import base64
from groq import Groq
from PyPDF2 import PdfReader

# =========================================================
# 1. PAGE CONFIGURATION (Mobile App Mode)
# =========================================================
st.set_page_config(
    page_title="Masood Alam Eye Diagnostics",
    layout="centered",
    page_icon="👁️"
)

# =========================================================
# 2. STYLING (Clean Mobile Look)
# =========================================================
st.markdown("""
<style>
/* Adjust padding for mobile screens */
.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
}
/* Hide Streamlit default menus */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Title */
h1 {
    text-align: center;
    font-size: 1.8rem !important;
    color: #0e1117;
}

/* Disclaimer Box */
.stAlert {
    border: 2px solid #ff4b4b;
    border-radius: 10px;
    font-size: 0.9rem;
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
# 3. API KEY SETUP
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# 4. MAIN INTERFACE
# =========================================================
st.title("👁️ Masood Alam Eye Diagnostics")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 20px;'>AI-Powered Ophthalmic Consultant</div>", unsafe_allow_html=True)

# --- DISCLAIMER (Top of Screen) ---
st.warning(
    """
    ⚠️ **AI MEDICAL DISCLAIMER**
    
    This tool is for **educational support only** and does not constitute a medical diagnosis. 
    **Always verify findings with clinical examination.**
    """
)

# --- MODALITY SELECTION (Main Body) ---
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

# =========================================================
# 5. LOGIC & PROMPTS
# =========================================================
SYSTEM_PROMPT = """
You are an expert Consultant Ophthalmologist (Dr. Masood Alam Shah).
Your task is to analyze the provided ophthalmic scan and generate a formal clinical report.

STRICT FORMATTING RULES:
1. **HEADLINES MUST BE BOLD AND UPPERCASE**.
2. **EXTRACT PATIENT DATA** if visible (Name, Age, ID).
3. **NO FLUFF**. Start directly with findings.
4. **PROFESSIONAL TONE** (Consultant level).

REQUIRED OUTPUT STRUCTURE:
**PATIENT DATA:** [Name, ID, Age - if visible]
**SCAN QUALITY:** [Signal strength, Artifacts, Centration]
**KEY FINDINGS:** [Bulleted list of anatomical/pathological findings]
**QUANTITATIVE ANALYSIS:** [Thickness values, indices, C/D ratio, etc.]
**CLINICAL IMPRESSION:** [Concise diagnostic summary]
**MANAGEMENT SUGGESTIONS:** [Recommendations for further investigation or treatment]
"""

MODALITY_INSTRUCTIONS = {
    "OCT Macula": "Focus on: CSMT, Retinal Layers (ILM, ELM
