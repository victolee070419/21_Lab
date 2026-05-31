import streamlit as st
from openai import OpenAI

st.title("ChatPDF")

if "api_key" not in st.session_state or not st.session_state["api_key"]:
    st.markdown("API KEY를 입력하세요.")
    st.stop()

client = OpenAI(api_key=st.session_state["api_key"])

if "pdf_messages" not in st.session_state:
    st.session_state["pdf_messages"] = []
if "vector_store_id" not in st.session_state:
    st.session_state["vector_store_id"] = None
if "file_id" not in st.session_state:
    st.session_state["file_id"] = None

def clear():
    if st.session_state["vector_store_id"]:
        client.vector_stores.delete(st.session_state["vector_store_id"])
    st.session_state["pdf_messages"] = []
    st.session_state["vector_store_id"] = None
    st.session_state["file_id"] = None

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type="pdf")

if uploaded_file and st.session_state["vector_store_id"] is None:
    with st.spinner("파일을 업로드하는 중입니다..."):
        vector_store = client.vector_stores.create(name=uploaded_file.name)
        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=[(uploaded_file.name, uploaded_file.getvalue(), "application/pdf")]
        )
        st.session_state["vector_store_id"] = vector_store.id

if st.session_state["vector_store_id"]:
    st.success("파일이 업로드되었습니다.")
    if st.button("Clear"):
        clear()
        st.rerun()

for message in st.session_state["pdf_messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state["vector_store_id"]:
    prompt = st.chat_input("PDF 내용에 대해 질문하세요.")
    if prompt:
        st.session_state["pdf_messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = client.responses.create(
            model="gpt-5.4-mini",
            input=st.session_state["pdf_messages"],
            tools=[{"type": "file_search", "vector_store_ids": [st.session_state["vector_store_id"]]}]
        )
        reply = response.output_text

        st.session_state["pdf_messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
