import streamlit as st
import requests
import os
import time
import base64

# --- Load API key and URLs ---

DIFY_API_KEY = st.secrets["DIFY_API_KEY"]
DIFY_CHAT_URL = st.secrets["DIFY_CHAT_URL"]
DIFY_FEEDBACK_URL_TEMPLATE = st.secrets["DIFY_FEEDBACK_URL_TEMPLATE"]

# --- Load Logo Image ---
logo_path = "logo.png"
with open(logo_path, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
logo_data_url = f"data:image/png;base64,{logo_base64}"

# --- Page Config ---
st.set_page_config(page_title="Festivo AI", page_icon=logo_path, layout="wide")

# --- Custom CSS ---
st.markdown(f"""
    <style>
        [data-testid="stSidebar"] {{
            background-color: #202020;
        }}
        .sidebar-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .new-chat-btn {{
            border: 1px solid #ff4b4b;
            color: white;
            background-color: transparent;
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-weight: bold;
            width: 100%;
        }}
        .new-chat-btn:hover {{
            background-color: #ff4b4b20;
        }}
        .stChatMessage.user {{
            text-align: right;
            background-color: #23262e;
            padding: 12px;
            border-radius: 16px;
            margin: 10px 0;
            color: white;
            font-size: 16px;
        }}
        .stChatMessage.assistant {{
            text-align: left;
            background-color: #1e1e1e;
            padding: 12px;
            border-radius: 16px;
            margin: 10px 0;
            color: white;
            font-size: 16px;
        }}
        .stTextInput>div>div>input {{
            background-color: #111;
            color: white;
        }}
        header {{
            background-color: #0e1117;
            padding: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.5rem;
        }}
        header:before {{
            content: "";
            display: inline-block;
            width: 50px;
            height: 50px;
            background-image: url("{logo_data_url}");
            background-size: cover;
        }}
        .block-container {{
            max-width: 900px;
            margin: 0 auto;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Layout ---
with st.sidebar:
    st.markdown("### 💬 Chat History")
    if st.button("+ New Chat", key="new_chat", help="Start a new conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_message_id = None
        st.session_state.starter_input = None
        st.rerun()

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_message_id" not in st.session_state:
    st.session_state.last_message_id = None

# --- Title ---
st.markdown("## Festivo AI – Explore Festivals Around the World")
st.markdown("Ask me about any festival, holiday, or observance day! 🌍")

# --- Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# --- Conversation Starter ---
if not st.session_state.chat_history:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
            🎉 Hi there! Welcome to **Festivo AI** – your guide to festivals, global holidays, and important observance days around the world. 🌍

            You can ask me about:
            • Festivals like Diwali, Pongal, or Christmas 👫  
            • Special days like Mother’s Day, Environment Day, or Children’s Day 🌱  
            • National and International observances from any country 🌐

            Go ahead and ask — What would you like to explore today? 💬
        """)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is the history of Christmas?"):
                st.session_state.starter_input = "What is the history of Christmas?"
        with col2:
            if st.button("What is the story behind Holi?"):
                st.session_state.starter_input = "What is the story behind Holi?"
        with col3:
            if st.button("Tell me about International Yoga Day."):
                st.session_state.starter_input = "Tell me about International Yoga Day."
else:
    st.session_state.starter_input = None

# --- Chat Input ---
user_input = st.chat_input("Type your special day question here...") or st.session_state.get("starter_input", "")

if user_input:
    st.session_state.starter_input = None
    st.chat_message("user", avatar="👤").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": user_input,
        "response_mode": "blocking",
        "user": "festivo-user-001",
        "conversation_id": ""
    }

    with st.spinner("🤔💬 Thinking..."):
        response = requests.post(DIFY_CHAT_URL, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer returned.")
            message_id = data.get("id")
            st.session_state.last_message_id = message_id

            response_box = st.chat_message("assistant", avatar="🤖").empty()
            displayed_text = ""
            for char in answer:
                displayed_text += char
                response_box.markdown(displayed_text + "▌")
                time.sleep(0.015)
            response_box.markdown(displayed_text)

            st.session_state.chat_history.append({"role": "assistant", "content": answer})

            # --- Feedback Section ---
            with st.expander("💬 Give Feedback on this Response"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Like", key=f"like_{message_id}"):
                        send_feedback(message_id, "like")
                        st.success("👍 Feedback received!")
                with col2:
                    if st.button("👎 Dislike", key=f"dislike_{message_id}"):
                        send_feedback(message_id, "dislike")
                        st.warning("👎 We'll use your feedback to improve.")

                feedback_comment = st.text_input("Optional comment:", key=f"comment_input_{message_id}")
                if st.button("Submit Comment", key=f"comment_submit_{message_id}"):
                    if feedback_comment.strip():
                        send_feedback(message_id, "like", content=feedback_comment)
                        st.success("📝 Comment submitted!")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")


# --- Feedback API ---
def send_feedback(message_id, rating, content=None):
    url = DIFY_FEEDBACK_URL_TEMPLATE.format(message_id=message_id)
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"rating": rating}
    if content:
        payload["content"] = content
    requests.post(url, json=payload, headers=headers)
