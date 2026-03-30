from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_filled_pdf(patient_data, output_path="patient_form.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(180, height - 60, "Hospital Admission Form")

    # Line
    c.line(50, height - 75, width - 50, height - 75)

    # Fields
    c.setFont("Helvetica-Bold", 12)
    c.setFont("Helvetica", 12)

    fields = [
        ("Patient Name", patient_data.get("name")),
        ("Age", patient_data.get("age")),
        ("Symptoms", patient_data.get("symptoms")),
        ("Medical History", patient_data.get("medical_history")),
        ("Allergies", patient_data.get("allergies")),
        ("Emergency Contact", patient_data.get("emergency_contact")),
    ]

    y = height - 120
    for label, value in fields:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(200, y, str(value) if value else "Not mentioned")
        y -= 40

    c.save()
    return output_path