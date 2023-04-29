import streamlit as st
import openai
from langchain.chat_models import ChatOpenAI

from prompts import INITIAL_CHAT_MODEL

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

chat = ChatOpenAI(temperature=.7, openai_api_key=OPENAI_API_KEY)
ai_message = chat(INITIAL_CHAT_MODEL)

st.title("SliceOfAdventure")
st.markdown(ai_message.content)

if st.button('It works!'):
    st.balloons()
