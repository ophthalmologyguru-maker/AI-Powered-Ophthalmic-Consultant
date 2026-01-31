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

/* 7. Share Button Styling */
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
    st.error("Missing Secrets. Please check Streamlit Settings.")
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# 4. MAIN INTERFACE (HEADER)
# =========================================================
st.title("👁️ Masood Alam Shah Eye Diagnostics 🇵🇰")
st.markdown("<div style='text-align: center; color: grey; margin-bottom: 5px;'>AI-Powered Ophthalmic Assistant</div>", unsafe_allow_html=True)

# SHARE BUTTON (Prominent)
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

                    # SYSTEM PROMPT (Fixed spacing to avoid errors)
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
# 6. DISPLAY RESULTS
# =========================================================
if 'analysis_result' in st.session_state:
    st.divider()
    st.success("Analysis Complete")
    st.markdown("### 📋 Clinical Report")
    st.markdown(st.session_state['analysis_result'])
    st.warning("Verify all findings clinically.")

# =========================================================
# 7. FEEDBACK SECTION
# =========================================================
def send_feedback_email(user_feedback):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = "masoodeye16@gmail.com"
        msg['Subject'] = "New Feedback: Eye Diagnostics App"
        body = f"User Feedback:\n\n{user_feedback}"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        text = msg.as_string()
        server.sendmail(email_user, "masoodeye16@gmail.com", text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

st.divider()
st.markdown("### 📩 App Feedback")
st.caption("Found a bug or have a suggestion? Send it directly to Dr. Masood Alam Shah.")

with st.form("feedback_form"):
    feedback_text = st.text_area("Your message here:")
    submit_feedback = st.form_submit_button("Send Feedback")

    if submit_feedback:
        if feedback_text:
            with st.spinner("Sending email..."):
                success = send_feedback_email(feedback_text)
                if success:
                    st.success("Feedback sent successfully to masoodeye16@gmail.com!")
                    st.balloons() 
                    st.markdown("**Thank you for your valuable feedback! It helps us improve.**")
        else:
            st.warning("Please write some text before sending.")
