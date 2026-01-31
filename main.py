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
        for i, page in enumerate(reader.pages):
            if i > 50: break
            text += page.extract_text() or ""
        return text[:5000]
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
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# 6. SPLIT LAYOUT (SIDE-BY-SIDE)
# =========================================================
col1, col2 = st.columns(2, gap="large")

# --- LEFT COLUMN: Imaging Selection ---
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

# --- RIGHT COLUMN: Upload, Analyze ---
with col2:
    st.write(f"### 2. Upload {modality} Scan")
    
    ack = st.checkbox("✅ I acknowledge the disclaimer above.")
    
    if ack:
        image_file = st.file_uploader("Tap to select image", type=["jpg", "jpeg", "png"])

        if image_file:
            st.image(image_file, caption="Scan Preview", use_container_width=True)
            
            if st.button("Analyze Scan", type="primary", use_container_width=True):
                with st.spinner("Dr. Masood Alam Shah's AI is analyzing..."):
                    
                    SYSTEM_PROMPT = """
                    You are an expert Consultant Ophthalmologist.
                    Analyze the ophthalmic scan professionally.
                    STRICT FORMATTING:
                    **PATIENT DATA:** [Name/ID/Age if visible]
                    **SCAN QUALITY:** [Signal, Artifacts]
                    **KEY FINDINGS:** [Bulleted list]
                    **QUANTITATIVE ANALYSIS:** [Thickness, Indices]
                    **CLINICAL IMPRESSION:** [Diagnosis]
                    **MANAGEMENT SUGGESTIONS:** [Next steps]
                    """
                    
                    MODALITY_INSTRUCTIONS = {
                        "OCT Macula": "Focus on: CSMT, Retinal Layers, Fluid, RPE.",
                        "OCT ONH (Glaucoma)": "Focus on: RNFL, C/D Ratio, ISNT rule.",
                        "Visual Field (Perimetry)": "Focus on: Reliability, GHT, MD, PSD, Defect pattern.",
                        "Corneal Topography": "Focus on: K-max, Pachymetry, Elevations.",
                        "Fluorescein Angiography (FFA)": "Focus on: Phases, Leakage, Ischemia.",
                        "OCT Angiography (OCTA)": "Focus on: Vascular density, FAZ, Neovascularization.",
                        "Ultrasound B-Scan": "Focus on: Retinal attachment, Vitreous echoes, Mass."
                    }

                    try:
                        encoded_image = encode_image(image_file)
                        reference_text = load_reference_text()
                        
                        user_prompt = f"MODALITY: {modality}\nCONTEXT: {MODALITY_INSTRUCTIONS[modality]}\nREF: {reference_text}"

                        messages = [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                            ]}
                        ]

                        response = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=messages,
                            temperature=0.1
                        )
                        
                        st.session_state['analysis_result'] = response.choices[0].message.content
                        
                    except Exception as e:
                        st.error(f"Analysis Error: {e}")
    else:
        st.info("Please accept the disclaimer to proceed.")

# =========================================================
# 7. DISPLAY RESULTS
# =========================================================
if 'analysis_result' in st.session_state:
    st.divider()
    st.success("Analysis Complete")
    st.markdown("### 📋 Clinical Report")
    st.markdown(st.session_state['analysis_result'])
    st.warning("Verify all findings clinically.")

# =========================================================
# 8. FEEDBACK FORM (Embedded)
# =========================================================
st.markdown("---") 
st.markdown("### 📩 App Feedback")
st.caption("Found a bug or have a suggestion? Send it directly to Dr. Masood Alam Shah.")

google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScbkQQZcFIquditVQdGTHUFCyZu3nXoLzl5DZzM8zpe49GweA/viewform?embedded=true"

components.iframe(google_form_url, height=800, scrolling=True)
