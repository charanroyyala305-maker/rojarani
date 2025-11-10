import streamlit as st
import json
import time
from ollama import Client

# 🔹 Initialize model
MODEL = "tinydolphin"
client = Client()

# 🔹 App title
st.title("💊 MedGuide - Your Digital Health Companion")
st.write("Ask about your symptoms, diseases, or any health-related questions 👇")

# 🔹 Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello 👋, I'm MedGuide — your digital health assistant. How can I help you today?"}
    ]

# 🔹 Display previous chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🗣 *You:* {msg['content']}")
    else:
        st.markdown(f"💬 *MedGuide:* {msg['content']}")

# 🔹 Input box for new question
user_input = st.text_input("Type your symptom, disease, or question here:")

# 🔹 Handle Ask button click
if st.button("Ask MedGuide"):
    if user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("MedGuide is preparing your full health information..."):
            # Send chat history for context
            response = client.chat(model=MODEL, messages=st.session_state.messages)

            # Get AI's reply
            ai_reply = response['message']['content']

            # Add AI response to chat
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # Re-run to show new messages
        st.rerun()
    else:
        st.warning("Please type something before asking MedGuide.")

# 🔹 Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared ✅. How can I assist you now?"}
    ]
    st.rerun()