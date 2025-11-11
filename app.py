import streamlit as st
from chatbot_chain import get_instructions

st.set_page_config(page_title="Rojarani Chatbot 💊", page_icon="💬")

st.title("💬 Rojarani Medical Chatbot")
st.write("Describe your symptoms and I’ll suggest possible conditions and medicines.")

user_input = st.text_input("🩺 Enter your symptom:")

if st.button("Get Advice"):
    if user_input.strip():
        response = get_instructions(user_input)
        st.markdown(response)
    else:
        st.warning("Please enter your symptom.")
