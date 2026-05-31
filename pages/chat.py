import streamlit as st
from openai import OpenAI

st.title("Chat")

if "api_key" not in st.session_state or not st.session_state["api_key"]:
    st.markdown("API KEY를 입력하세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.button("Clear"):
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("메시지를 입력하세요.")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    client = OpenAI(api_key=st.session_state["api_key"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=st.session_state["messages"]
    )
    reply = response.output_text

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
