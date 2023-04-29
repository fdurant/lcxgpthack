import streamlit as st
import pandas as pd
import numpy as np
from langchain.llms import OpenAI

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(temperature=0.9)

prompt = "What would be a good name for a company that bakes Pizzas and Waffles?"

st.title('Basic Streamlit app')

st.write(prompt)

st.write(llm(prompt=prompt))

if st.button('It works!'):
    st.balloons()
