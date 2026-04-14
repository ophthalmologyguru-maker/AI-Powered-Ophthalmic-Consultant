import streamlit as st
import base64
import streamlit.components.v1 as components 
import anthropic
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
div[role="radiogroup"] > label > div:first-child {
    display: none; 
}

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

div[role="radiogroup"] > label:hover {
    opacity: 0.8;
    transform: scale(1.0);
    cursor: pointer;
}

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

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. API SETUP (CLAUDE)
# =========================================================
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    st.error("Missing Secrets (ANTHROPIC_API_KEY). Please check Streamlit Settings.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# =========================================================
# 4. FUNCTIONS
# =========================================================
def encode_image(file):
    return base64.b64encode(file.getvalue()).decode("utf-8")

def get_media_type(file):
    # Claude needs to know if it's a jpeg or png
    if file.type:
        return file.type
    elif file.name.lower().endswith("png"):
        return "image/png"
    return "image/jpeg"

def load_reference_text(path="REFERNCE.pdf"):
    try:
        reader = PdfReader(path)
        text = ""
        for i, page in enumerate(reader.pages):
            if i > 50: break
            text += page.extract_text() or ""
        return text[:6000] 
    except:
        return ""

# =========================================================
# 5. MAIN INTERFACE (HEADER)
# =========================================================
st.title("👁️ Masood Alam Shah Eye Diagnostics 🇵🇰")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 5px;'>AI-Powered Ophthalmic Assistant</div>", unsafe_allow_html=True)

# SHARE BUTTON
share_link = "https://wa.me/?text=Check%20out%20Dr.%20Masood%20Alam%20Shah%27s%20Eye%20Diagnostics%20App%3A%20https%3A%2F%2Fmasoodalamshah.streamlit.app"
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
            "Ultrasound B-Scan",
            "Electroretinogram (ERG)",
            "Visual Evoked Potential (VEP)",
            "Electrooculogram (EOG)"
        ],
        index=0
    )

# --- RIGHT COLUMN: Upload, Analyze ---
with col2:
    st.write(f"### 2. Upload Scan")
    
    ack = st.checkbox("✅ I acknowledge the disclaimer above.")
    
    if ack:
        uploaded_files = st.file_uploader("📂 Upload from Gallery (Select multiple scans if needed)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            cols = st.columns(len(uploaded_files))
            for i, file in enumerate(uploaded_files):
                cols[i].image(file, caption=f"Scan {i+1}", use_container_width=True)
            
            if st.button("Analyze Scans", type="primary", use_container_width=True):
                with st.spinner("Dr. Masood Alam Shah's AI is analyzing..."):
                    
                    # --- SYSTEM PROMPT ---
                    SYSTEM_PROMPT = """
                    You are an expert Consultant Ophthalmologist.
                    Analyze the ophthalmic scan(s) professionally. 
                    If multiple images are provided, synthesize them into a single comprehensive diagnostic report.
                    STRICT FORMATTING:
                    **PATIENT DATA:** [Name/ID/Age if visible]
                    **SCAN QUALITY:** [Signal, Artifacts]
                    **KEY FINDINGS:** [Bulleted list summarizing findings across all provided images]
                    **QUANTITATIVE ANALYSIS:** [Thickness, Indices, Amplitudes, Latencies]
                    **CLINICAL IMPRESSION:** [Diagnosis MUST be written in **ALL CAPS AND BOLD**, e.g., **DIABETIC MACULAR EDEMA**]
                    **MANAGEMENT SUGGESTIONS:** [Next steps]
                    """
                    
                    MODALITY_INSTRUCTIONS = {
                        "OCT Macula": "Focus on: CSMT, Retinal Layers, Fluid (IRF/SRF), RPE, Choroid.",
                        "OCT ONH (Glaucoma)": "Focus on: RNFL thickness, C/D Ratio, ISNT rule, Disc symmetry.",
                        "Visual Field (Perimetry)": "Focus on: Reliability (Fixation losses, FN/FP), GHT, MD, PSD, Defect Pattern (Arcuate, Nasal step, etc.).",
                        "Corneal Topography": "Focus on: K-max, Pachymetry, Anterior/Posterior Elevation, Astigmatism patterns (Bow-tie, Crab claw).",
                        "Fluorescein Angiography (FFA)": "Focus on: Phases (Arterial, Venous), Hyperfluorescence (Leakage, Pooling, Staining, Window defect), Hypofluorescence (Blocking, Filling defect).",
                        "OCT Angiography (OCTA)": "Focus on: Vascular density, FAZ (Foveal Avascular Zone), Neovascularization, Ischemia.",
                        "Ultrasound B-Scan": "Focus on: Vitreous echoes, Retinal attachment, Mass (Reflectivity), Choroidal thickening.",
                        "Electroretinogram (ERG)": "Focus on: scotopic/photopic responses, a-wave (photoreceptors), b-wave (bipolar/Müller), amplitudes, implicit times.",
                        "Visual Evoked Potential (VEP)": "Focus on: P100 latency, Amplitude, Inter-eye asymmetry, Morphology.",
                        "Electrooculogram (EOG)": "Focus on: Arden Ratio (Light peak / Dark trough). Normal > 1.85."
                    }

                    try:
                        reference_text = load_reference_text()
                        user_prompt = f"MODALITY: {modality}\nCONTEXT: {MODALITY_INSTRUCTIONS.get(modality, 'Analyze standard ophthalmic image.')}\nREF: {reference_text}"

                        # Build the payload for Claude
                        user_content = []
                        
                        # 1. Add all images first
                        for file in uploaded_files:
                            encoded_image = encode_image(file)
                            media_type = get_media_type(file)
                            
                            user_content.append({
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": encoded_image
                                }
                            })
                            
                        # 2. Add the text prompt at the end
                        user_content.append({"type": "text", "text": user_prompt})

                        # Call Claude API
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20240620",
                            max_tokens=1500,
                            temperature=0.1,
                            system=SYSTEM_PROMPT,
                            messages=[
                                {"role": "user", "content": user_content}
                            ]
                        )
                        
                        # --- POST-PROCESSING ---
                        raw_result = response.content[0].text
                        colored_result = raw_result.replace("**CLINICAL IMPRESSION:**", "### :red[**CLINICAL IMPRESSION:**]")
                        
                        st.session_state['analysis_result'] = colored_result
                        
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

google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeItsM5K0MtBon20jwu1Y1biXucGeRFmo9YOlc5VtbBzY0IZw/viewform?embedded=true"

components.iframe(google_form_url, height=800, scrolling=True)
