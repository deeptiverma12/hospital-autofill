from groq import Groq
import json

client = Groq()
def extract_patient_info(raw_text):
  prompt =f"""
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
        messages=[{"role": "user", "content":prompt}]
    )
    
  raw_output = response.choices[0].message.content
  raw_output = raw_output.strip().strip("```json").strip("```").strip()
  patient_data = json.loads(raw_output)
  return patient_data
raw_input = input("Enter patient details: ")
result = extract_patient_info(raw_input)
print("\nExtracted Info:")
print(json.dumps(result, indent=2))