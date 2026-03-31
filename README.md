# 🏥 Hospital Patient Autofill

An AI-powered hospital patient intake automation system that eliminates manual form filling.

## 🚀 Live Demo

[Click here to try the app]
https://patient-autofill.streamlit.app/

## 🔍 The Problem

When a patient arrives at a hospital — especially in critical condition — staff waste precious minutes filling the same information across multiple forms manually.

## ✅ The Solution

This system lets staff type or speak patient details once in natural language. The AI extracts structured information and auto-fills a professional admission PDF instantly.

## ⚙️ Features

- 🧠 LLM-powered information extraction from messy natural language input
- 🎤 Voice input support via OpenAI Whisper
- 📄 Auto-generated professional hospital admission PDF
- 🗃️ Patient records stored in SQLite database
- 🌐 Clean two-column web UI built with Streamlit

## 🛠️ Tech Stack

- Python
- Groq API (Llama 3.3-70b)
- OpenAI Whisper
- Streamlit
- ReportLab
- SQLite

## 🏃 How to Run Locally

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set your Groq API key: `$env:GROQ_API_KEY="your_key"`
4. Run: `streamlit run app.py`

## ⚠️ Note

This project uses synthetic/dummy patient data only. Not intended for real clinical use.
