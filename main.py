import streamlit as st
import base64
from groq import Groq
from PyPDF2 import PdfReader

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Masood Alam Eye Diagnostics",
    layout="centered",  # Changed to centered for better mobile app look
    page_icon="👁️"
)

# =========================================================
# STYLING (Mobile App Look)
# =========================================================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
}
/* Hide default elements for app-like feel */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Title Style */
h1 {
    text-align: center;
    font-size: 2rem !important;
    color: #0e1117;
}

/* Disclaimer Box Styling */
.stAlert {
    border: 2px solid #ff4b4b;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# API KEY
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found. Please add it to Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# MAIN APP INTERFACE
# =========================================================
# 1. Title
st.title("👁️ Masood Alam Eye Diagnostics")
st.markdown("<p style='text-align: center; color: grey;'>AI-Powered Ophthalmic Consultant</p>", unsafe_allow_html=True)

# 2. Disclaimer (Now in Main Body, NOT Sidebar)
st.warning(
    """
    ⚠️ **AI MEDICAL DISCLAIMER**
    
    This tool is for **educational support only** and does not constitute a medical diagnosis. 
    Verify all findings with clinical examination.
    """
)

# 3. Modality Selection (Main Body)
st.write("### 1. Select Imaging Type")
modality = st.radio(
    "Choose modality:",
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

# 4. Style Selection
report_style = st.selectbox(
    "Report Style:",
    ["Consultant Clinical Report", "Exam-Oriented (FCPS / MRCOphth)"]
)

# =========================================================
# SYSTEM PROMPTS & INSTRUCTIONS
# =========================================================
SYSTEM_PROMPT = """
You are an expert Consultant Ophthalmologist (Dr. Masood Alam Shah).
Your task is to analyze the provided ophthalmic scan and generate a formal clinical report.

STRICT FORMATTING RULES:
1. HEADLINES MUST BE BOLD AND UPPERCASE.
2. EXTRACT PATIENT DATA if visible.
3. NO FLUFF. Start directly with findings.
4. PROFESSIONAL TONE.

REQUIRED OUTPUT STRUCTURE:
**PATIENT DATA:** [Name, ID, Age - if visible]
**SCAN QUALITY:** [Signal, Artifacts]
**KEY FINDINGS:** [Bulleted list]
**QUANTITATIVE ANALYSIS:** [Numbers/Thickness/Indices]
**CLINICAL IMPRESSION:** [Diagnosis]
**MANAGEMENT SUGGESTIONS:** [Next steps]
"""

MODALITY_INSTRUCTIONS = {
    "OCT Macula": "Focus on: CSMT, Retinal Layers (ILM, ELM, IS/OS), Fluid (IRF/SRF), and RPE status.",
    "OCT ONH (Glaucoma)": "Focus on: RNFL Thickness (Average & Quadrants), Cup-to-Disc Ratio, and ISNT rule.",
    "Visual Field (Perimetry)": "Focus on: Reliability indices, GHT, Mean Deviation (MD), PSD, and defect patterns.",
    "Corneal Topography": "Focus on: K-max, Thinnest Pachymetry, and Anterior/Posterior Elevation maps.",
    "Fluorescein Angiography (FFA)": "Focus on: Phases, Leakage, Staining, Pooling, and Ischemia.",
    "OCT Angiography (OCTA)": "Focus on: Vascular density, FAZ size, and Neovascular networks.",
    "Ultrasound B-Scan": "Focus on: Retinal attachment, Vitreous echoes, and Mass lesions."
}

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

# =========================================================
# UPLOAD & ANALYZE
# =========================================================
st.divider()
st.write(f"### 2. Upload {modality} Scan")

# Mandatory Checkbox
acknowledgement = st.checkbox("✅ I accept the medical disclaimer.")

if acknowledgement:
    image_file = st.file_uploader("Tap to select image", type=["jpg", "jpeg", "png"])

    if image_file:
        st.image(image_file, caption="Preview", use_column_width=True)
        
        if st.button("Analyze Scan", type="primary", use_container_width=True):
            with st.spinner("Dr. Masood's AI is analyzing..."):
                try:
                    encoded_image = encode_image(image_file)
                    reference_text = load_reference_text()
                    
                    user_prompt = f"MODALITY: {modality}\nCONTEXT: {MODALITY_INSTRUCTIONS[modality]}\nREF: {reference_text}"

                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{encoded_image}"
                                    }
                                }
                            ]
                        }
                    ]

                    # --- FIXED MODEL NAME ---
                    response = client.chat.completions.create(
                        model="llama-3.2-90b-vision-preview",
                        messages=messages,
                        temperature=0.1
                    )

                    st.success("Analysis Complete")
                    st.markdown("### 📋 Clinical Report")
                    st.markdown(response.choices[0].message.content)
                    st.warning("Verify findings clinically.")
