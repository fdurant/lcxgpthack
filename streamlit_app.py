import streamlit as st
import pandas as pd
import numpy as np
from langchain.llms import OpenAI
import openai

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)

prompt_company_name = "What would be a good name for a hipster restaurant that bakes Pizzas and Waffles?"
answer = llm(prompt=prompt_company_name)

prompt_illustration = f"Front store of an expensive hipster restaurant with signage \"{answer}\""
response = openai.Image.create(
  prompt=prompt_illustration,
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

st.title('Basic Streamlit app')
st.write(prompt_company_name)
st.write(answer)

st.image(image_url, caption=answer, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="small")

if st.button('It works!'):
    st.balloons()
