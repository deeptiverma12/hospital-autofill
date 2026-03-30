from pdf_generator import generate_filled_pdf
import os
import streamlit as st
from groq import Groq
import json

client = Groq()

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


st.title("Hospital Patient Autofill")
st.write("Enter patient details in any format. The system will extract structured information automatically.")

raw_input = st.text_area("Patient Details", height=150)

if st.button("Extract Info"):
    if raw_input:
        with st.spinner("Extracting..."):
            result = extract_patient_info(raw_input)
        
        st.success("Done!")
        pdf_path = generate_filled_pdf(result)
        with open(pdf_path, "rb") as f:
           st.download_button(
           label="Download Filled PDF",
           data=f,
           file_name="patient_form.pdf",
           mime="application/pdf"
    )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Name", result.get("name") or "Not mentioned")
            st.metric("Age", result.get("age") or "Not mentioned")
            st.metric("Allergies", result.get("allergies") or "Not mentioned")
        
        with col2:
            st.metric("Symptoms", result.get("symptoms") or "Not mentioned")
            st.metric("Medical History", result.get("medical_history") or "Not mentioned")
            st.metric("Emergency Contact", result.get("emergency_contact") or "Not mentioned")
    else:
        st.warning("Please enter patient details first.")