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

/* --- RADIO BUTTON STYLING (Scan Type) --- */
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
    
    /* Dim unselected items */
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
    opacity: 1.0;             /* Full Brightness */
    transform: scale(1.03);   /* Slightly Larger */
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3); /* Add Shadow */
    border: 2px solid white;  /* White border highlight */
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
    st.error("Missing Secrets (GROQ_API_KEY). Please check Streamlit
