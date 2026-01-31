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
div[role="radiogroup"]
