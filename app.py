import streamlit as st
import os
from groq import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("LLM Chat Demo")

# Initialize session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display the chat history
for m in st.session_state.chat:
    st.chat_message(m["role"]).write(m["content"])

# Get user input
prompt = st.chat_input("Ask something")

if prompt:
    # Add user message to chat history
    st.session_state.chat.append({"role": "user", "content": prompt})

    # Make the API call and get a response
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.chat
        )
        reply = res.choices[0].message.content
        st.session_state.chat.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {e}")

    # Automatically re-render the page after a response
    st.experimental_rerun()
