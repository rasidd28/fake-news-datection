import streamlit as st
import requests

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
WEBHOOK_URL = "https://rahulllllllllllllllll.app.n8n.cloud/webhook-test/8d91510a-69e7-4380-9653-120ccac05906

st.set_page_config(
    page_title="Conversational AI Assistant",
    page_icon="💬",
    layout="centered"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# UI HEADER
# -------------------------------------------------
st.title("💬 Conversational AI Assistant")
st.caption("Friendly • Helpful • Natural conversation")

# -------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------------------------
    # SEND TO n8n
    # -------------------------------------------------
    payload = {
        "message": user_input,
        "conversation": st.session_state.messages
    }

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    WEBHOOK_URL,
                    json=payload,
                    timeout=90
                )

            result = response.json()

            assistant_reply = result.get(
                "reply",
                "Sorry, I couldn’t generate a response right now."
            )

    except Exception as e:
        assistant_reply = f"⚠️ Something went wrong. Please try again."

    # -------------------------------------------------
    # DISPLAY ASSISTANT MESSAGE
    # -------------------------------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
