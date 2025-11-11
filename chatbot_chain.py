import json
import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------- MODEL SELECTION -----------------
MODEL = "llama-3.1-8b-instant"
# ---------------------------------------------------

# Load your diseases and medicine info
with open("patient_instructions.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# Emergency keywords (optional)
EMERGENCY_KEYWORDS = {"chest pain", "shortness of breath", "severe bleeding", "loss of consciousness"}


def get_instructions(symptom_text: str) -> str:
    text = symptom_text.strip().lower()

    # emergency detection
    if any(word in text for word in EMERGENCY_KEYWORDS):
        return "🚨 Emergency: Please seek medical help immediately."

    # match disease
    for disease, info in DATA.items():
        if disease.lower() in text:
            return (
                f"🩺 Disease: {disease}\n"
                f"💊 Medicines: {', '.join(info['medicines'])}\n"
                f"💉 Dosage: {info['dosage']}\n"
                f"📦 Storage: {info['storage']}\n"
                f"📋 Instructions: {info['instructions']}"
            )

    # fallback: use LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content.strip()
