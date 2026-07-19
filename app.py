import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ===============================
# Load Environment Variables
# ===============================
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ===============================
# Page Configuration
# ===============================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# Custom CSS
# ===============================
st.markdown("""
<style>

.stApp{
    background:#f5f7fb;
}

.block-container{
    padding-top:1rem;
    max-width:900px;
}

h1{
    color:#003366;
    text-align:center;
    font-size:45px;
}

.stCaption{
    text-align:center;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
    margin-bottom:10px;
}

.stButton button{
    background:#003366;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 18px;
    font-weight:bold;
}

.stButton button:hover{
    background:#0056b3;
    color:white;
}

div[data-testid="stChatInput"]{
    border-radius:12px;
}

section[data-testid="stSidebar"]{
    background:#eef3fb;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# Sidebar
# ===============================
with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.write("Powered by OpenRouter API")

    st.divider()

    st.subheader("✨ Features")

    st.markdown("""
- 💬 AI Conversation
- 🧠 Context Memory
- 🔄 Session State
- ⚡ Fast Responses
- 🗑️ Clear Chat
""")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = [
            {
                "role":"system",
                "content":"You are an AI assistant. Your task is to generate helpful responses."
            }
        ]

        st.rerun()

# ===============================
# Session State
# ===============================
if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role":"system",
            "content":"You are an AI assistant. Your task is to generate helpful responses."
        }

    ]

# ===============================
# Welcome Screen
# ===============================
if len(st.session_state.messages) == 1:

    st.title("🤖 AI Assistant")

    st.caption("Chat with an AI powered by OpenRouter")

    st.info("👋 Ask me anything!")

# ===============================
# Display Chat History
# ===============================
for message in st.session_state.messages:

    if message["role"] != "system":

        with st.chat_message(message["role"]):

            st.write(message["content"])

# ===============================
# Chat Input
# ===============================
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display User Message

    with st.chat_message("user"):

        st.write(prompt)

    st.session_state.messages.append(

        {
            "role":"user",
            "content":prompt
        }

    )

    # Generate Response

    with st.spinner("Thinking..."):

        response = client.chat.completions.create(

            model="poolside/laguna-xs-2.1:free",

            messages=st.session_state.messages

        )

        answer = response.choices[0].message.content

    # Display AI Message

    with st.chat_message("assistant"):

        st.write(answer)

    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer
        }

    )