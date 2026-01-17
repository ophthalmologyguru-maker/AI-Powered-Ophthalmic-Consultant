import streamlit as st
import base64
from groq import Groq
from PyPDF2 import PdfReader

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Zubaida Eye Diagnostics",
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
# 3. GROQ API SETUP
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
st.title("👁️ Zubaida Eye Diagnostics")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 20px;'>AI-Powered Ophthalmic Consultant</div>", unsafe_allow_html=True)

st.warning(
    """
    ⚠️ **AI MEDICAL DISCLAIMER**
    
    This tool is for **educational support only** and does not constitute a medical diagnosis. 
    **Always verify findings with clinical examination.**
    """
)

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
# UPDATED: Generic Expert Persona (No Name)
SYSTEM_PROMPT = """
You are an expert Consultant Ophthalmologist.
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
    "OCT Macula": """Focus on: CSMT, Retinal Layers (ILM, ELM, IS/OS), Fluid (IRF/SRF), and RPE status.""",
    "OCT ONH (Glaucoma)": """Focus on: RNFL Thickness (Average & Quadrants), Cup-to-Disc Ratio, and ISNT rule.""",
    "Visual Field (Perimetry)": """Focus on: Reliability indices, GHT, Mean Deviation (MD), PSD, and defect patterns.""",
    "Corneal Topography": """Focus on: K-max, Thinnest Pachymetry, and Anterior/Posterior Elevation maps.""",
    "Fluorescein Angiography (FFA)": """Focus on: Phases, Leakage, Staining, Pooling, and Ischemia.""",
    "OCT Angiography (OCTA)": """Focus on: Vascular density, FAZ size, and Neovascular networks.""",
    "Ultrasound B-Scan": """Focus on: Retinal attachment, Vitreous echoes, and Mass lesions."""
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
# 6. UPLOAD & ANALYZE
# =========================================================
st.divider()
st.write(f"### 2. Upload {modality} Scan")

ack = st.checkbox("✅ I acknowledge the disclaimer above.")

if ack:
    image_file = st.file_uploader("Tap to select image", type=["jpg", "jpeg", "png"])

    if image_file:
        st.image(image_file, caption="Scan Preview", use_container_width=True)
        
        if st.button("Analyze Scan", type="primary", use_container_width=True):
            # UPDATED: Generic Spinner Text
            with st.spinner("Zubaida AI is analyzing..."):
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

                    # Using Llama 4 Scout (Current Working Model)
                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=messages,
                        temperature=0.1
                    )

                    st.success("Analysis Complete")
                    st.markdown("### 📋 Clinical Report")
                    st.markdown(response.choices[0].message.content)
                    st.warning("Verify all findings clinically.")

                except Exception as e:
                    st.error(f"Analysis Error: {e}")
else:
    st.info("Please accept the disclaimer to proceed.")
