import streamlit as st
import requests

# App title
st.set_page_config(page_title="my poooo Chatbot with langchain and blablabla")

if "messages" not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "How may I help you?"}]
if "is_thinking" not in st.session_state:
    st.session_state['is_thinking'] = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(prompt_input):
    inputs = {"input": {"question": prompt_input}}
    #response = requests.post("http://localhost:8000/chatGPT-turbo/invoke", json=inputs)
    response = requests.post("https://3592-173-231-123-226.ngrok-free.app/chatGPT-turbo/invoke", json=inputs)
    return response.json()["output"]["answer"]

# User-provided prompt
if not st.session_state.is_thinking:
    prompt = st.chat_input(placeholder="Type your message here...",disabled=st.session_state.is_thinking)
    if prompt:
        st.session_state.is_thinking = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant" and st.session_state.is_thinking:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(st.session_state.messages[-1]["content"])
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    st.session_state.is_thinking = False
