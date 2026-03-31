import streamlit as st
from groq import Groq
import json
from pdf_generator import generate_filled_pdf
from database import init_db, save_patient, get_all_patients
try:
    from voice import transcribe_audio
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False
import os

 
st.set_page_config(
    page_title="Hospital Patient Autofill",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #1a66cc;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #1450a3; }
    .info-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .header-text {
        color: #1a66cc;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .subheader-text { color: #555; font-size: 1rem; }
    .field-label { color: #888; font-size: 0.85rem; font-weight: bold; }
    .field-value { color: #222; font-size: 1.1rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

client = Groq()
init_db()

def extract_patient_info(raw_text):
    prompt = f"""
You are a hospital assistant. Extract patient information from the text below.
Return ONLY a JSON object with these fields:
- name
- age
- symptoms
- medical_history
- allergies
- emergency_contact

If any field is not mentioned, set it to null.
Return only the JSON. No explanation. No extra text.

Patient text: {raw_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    raw_output = response.choices[0].message.content
    raw_output = raw_output.strip().strip("```json").strip("```").strip()
    patient_data = json.loads(raw_output)
    return patient_data

st.markdown('<p class="header-text">🏥 Hospital Patient Autofill</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">Enter or speak patient details — the system extracts, saves, and generates a filled admission form instantly.</p>', unsafe_allow_html=True)
st.divider()

# Two column layout
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📝 Patient Input")

    if "patient_text" not in st.session_state:
        st.session_state.patient_text = ""

    raw_input = st.text_area("Type patient details here", height=180, value=st.session_state.patient_text, placeholder="e.g. My name is Ravi, 45 years old, chest pain since morning, diabetic, allergic to penicillin...")

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        extract_clicked = st.button("⚡ Extract Info", use_container_width=True)
    with btn_col2:
     if VOICE_AVAILABLE:
        if st.button("🎤 Speak Instead", use_container_width=True):
            with st.spinner("Listening for 10 seconds..."):
                spoken_text = transcribe_audio()
            st.session_state.patient_text = spoken_text
            st.rerun()
     else:
        st.button("🎤 Voice (Local Only)", disabled=True, use_container_width=True

with col_right:
    st.markdown("### 📋 Extracted Information")

    if extract_clicked and raw_input:
        with st.spinner("Extracting with AI..."):
            result = extract_patient_info(raw_input)
            save_patient(result)
            pdf_path = generate_filled_pdf(result)

        st.success("✅ Patient info extracted and saved!")

        fields = [
            ("👤 Full Name", result.get("name")),
            ("🎂 Age", result.get("age")),
            ("🩺 Symptoms", result.get("symptoms")),
            ("📋 Medical History", result.get("medical_history")),
            ("⚠️ Allergies", result.get("allergies")),
            ("📞 Emergency Contact", result.get("emergency_contact")),
        ]

        for label, value in fields:
            st.markdown(f"""
            <div class="info-card">
                <p class="field-label">{label}</p>
                <p class="field-value">{value if value else "Not mentioned"}</p>
            </div>
            """, unsafe_allow_html=True)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Admission Form",
                data=f,
                file_name="patient_form.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    elif extract_clicked and not raw_input:
        st.warning("Please enter patient details first.")
    else:
        st.info("Extracted patient information will appear here.")

# Patient records
st.divider()
st.markdown("### 🗂️ Patient Records")
patients = get_all_patients()
if patients:
    for p in patients:
        st.markdown(f"""
        <div class="info-card">
            <p class="field-label">ID: {p[0]}</p>
            <p class="field-value">{p[1]} | Age: {p[2]} | Symptoms: {p[3]}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No patients recorded yet.")