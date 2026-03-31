from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime
import random

def generate_filled_pdf(patient_data, output_path="patient_form.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFillColorRGB(0.1, 0.4, 0.7)
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 45, "City General Hospital")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 65, "Patient Admission Form")
    c.drawString(50, height - 82, "Emergency & Outpatient Department")
    patient_id = f"PID-{random.randint(10000, 99999)}"
    date_str = datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 50, height - 45, f"Patient ID: {patient_id}")
    c.drawRightString(width - 50, height - 62, f"Date: {date_str}")

    c.setFillColor(colors.black)

    # Section: Patient Information
    y = height - 130
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.1, 0.4, 0.7)
    c.drawString(50, y, "PATIENT INFORMATION")
    c.setFillColor(colors.black)
    c.line(50, y - 5, width - 50, y - 5)

    y -= 30
    fields = [
        ("Full Name", patient_data.get("name")),
        ("Age", patient_data.get("age")),
        ("Presenting Symptoms", patient_data.get("symptoms")),
        ("Medical History", patient_data.get("medical_history")),
        ("Known Allergies", patient_data.get("allergies")),
        ("Emergency Contact", patient_data.get("emergency_contact")),
    ]

    for label, value in fields:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"{label}:")
        c.setFont("Helvetica", 11)
        c.drawString(220, y, str(value) if value else "Not mentioned")
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(50, y - 8, width - 50, y - 8)
        y -= 35

    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.1, 0.4, 0.7)
    c.drawString(50, y, "DECLARATION")
    c.setFillColor(colors.black)
    c.line(50, y - 5, width - 50, y - 5)

    y -= 25
    c.setFont("Helvetica", 10)
    declaration = (
        "I hereby confirm that the information provided above is accurate to the best of my knowledge. "
        "I consent to the necessary medical examination and treatment."
    )
    c.drawString(50, y, declaration[:80])
    c.drawString(50, y - 15, declaration[80:])

    y -= 60
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Patient / Guardian Signature:")
    c.line(250, y, 420, y)

    c.drawString(50, y - 35, "Doctor Signature:")
    c.line(250, y - 35, 420, y - 35)

    c.drawString(50, y - 70, "Staff ID:")
    c.line(250, y - 70, 420, y - 70)

    c.setFillColorRGB(0.1, 0.4, 0.7)
    c.rect(0, 0, width, 30, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 9)
    c.drawString(50, 10, "City General Hospital | Emergency Dept | This is a system-generated form")
    c.drawRightString(width - 50, 10, f"{patient_id}")

    c.save()
    return output_path