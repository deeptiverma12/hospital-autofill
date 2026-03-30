import sqlite3

DB_PATH ="patients.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age TEXT,
            symptoms TEXT,
            medical_history TEXT,
            allergies TEXT,
            emergency_contact TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_patient(patient_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, symptoms, medical_history, allergies, emergency_contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_data.get("name"),
        str(patient_data.get("age")),
        patient_data.get("symptoms"),
        patient_data.get("medical_history"),
        patient_data.get("allergies"),
        patient_data.get("emergency_contact")
    ))
    conn.commit()
    conn.close()

def search_patient(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?", (f"%{name}%",))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "name": row[1],
            "age": row[2],
            "symptoms": row[3],
            "medical_history": row[4],
            "allergies": row[5],
            "emergency_contact": row[6]
        }
    return None

def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, symptoms FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows