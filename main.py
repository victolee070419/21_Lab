import streamlit as st
import base64
from openai import OpenAI
 
@st.cache_data
def get_llm_response(api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text
 
@st.cache_data
def generate_image(api_key, image_prompt):
    client = OpenAI(api_key=api_key)
    img = client.images.generate(model="gpt-image-1-mini", prompt=image_prompt)
    image_bytes = base64.b64decode(img.data[0].b64_json)
    return image_bytes
 
st.title("OpenAI GPT model")
 
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""
 
api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state["api_key"])
if api_key:
    st.session_state["api_key"] = api_key
    client = OpenAI(api_key=api_key)
else:
    st.markdown("API KEY를 입력하세요.")
 
prompt = st.text_area("User prompt")
 
if st.button("Ask!", disabled=(len(prompt)==0)):
    st.write(get_llm_response(st.session_state["api_key"], prompt))
 
image_prompt = st.text_area("Image prompt")
 
if st.button("Generate!", disabled=(len(image_prompt)==0)):
    st.image(generate_image(st.session_state["api_key"], image_prompt))