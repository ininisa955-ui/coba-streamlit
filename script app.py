import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("❌ Tidak menemukan API key. Pastikan file .env berisi: OPENROUTER_API_KEY=sk-or-v1-xxxxx")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

st.title("🤖 Chatbot AI Interaktif")
st.write("Selamat datang di Chatbot AI menggunakan *OpenRouter* 🚀")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik pesanmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except OpenAIError as e:
        st.error(f"Terjadi kesalahan saat mengakses API: {e}")
