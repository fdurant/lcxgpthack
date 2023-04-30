import streamlit as st
import os
import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

import folium
from streamlit_folium import st_folium, folium_static
from utils import get_location, get_country_code, get_cities

from time import strftime
today_human = strftime("%a, %d %b %Y")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
os.environ['SERPAPI_API_KEY'] = SERPER_API_KEY

my_country_latlon = get_location()
my_country_lat = my_country_latlon[0]
my_country_lon = my_country_latlon[1]
m = folium.Map(location=my_country_latlon, width=750, height=500, zoom_start=3, control_scale=True)

my_country_code = get_country_code(lat=my_country_lat, lon=my_country_lon)

my_cities = get_cities(country_code=my_country_code)

location = st.selectbox(
    label='What is your location?',
    options=my_cities)

st.write('You selected:', location)

# st_data = st_folium(m, width=700)

INITIAL_CHAT_MODEL = [
    SystemMessage(content="Act as a parent that is highly skilled in organising engaging past time activities for the family."),
    HumanMessage(content="Your task is to help me plan a diverse calendar with activities for my family."),
    AIMessage(content="Tell me more about your family so I can provide suggestions tailored your needs and preferences. First question: How many family members are there, and what are their ages?"),
    HumanMessage(content="We are three. I'm a man of 41, my wife is 36. We have a daughter of 2,5 years old.."),
    AIMessage(content="What are the general interests or hobbies of each family member?"),
    HumanMessage(content="We like music, playing, walking around, nature, playgrounds, eating out, inviting friends for dinner. Some culture too. We don't have specific hobbies."),
    AIMessage(content="How much time do you have available for these activities? Are you looking for daily, weekly, or monthly activities?"),
    HumanMessage(content="We mostly have weekends, and sometimes evenings. But with our toddler, the evenings are often short, and there's not much time for other activities."),
    AIMessage(content="Do you have any budget constraints for the activities?"),
    HumanMessage(content="We have a moderate income, and no specific budget constraints. "),
    AIMessage(content="Is there a specific focus for the activities, such as learning, bonding, fitness, or relaxation?"),
    HumanMessage(content="There's no specific focus. But a good balance might be nice."),
    AIMessage(content="Are there any physical or dietary restrictions within your family that I should be aware of?"),
    HumanMessage(content="We don't have dietary restrictions."),
    AIMessage(content="What is the general climate and geography of your area? Are there any local attractions or resources that you'd like to incorporate into the calendar?"),
    HumanMessage(content=f"We live in {location}. Remember I am a local, not a tourist."),
    AIMessage(content=f"Great! I'll give you a list of suggestions for the next weekend, taking into account that today is {today_human}. Each suggestion is structured in Markdown. I'll give three suggestions per day"),
]

chat = ChatOpenAI(temperature=.7, openai_api_key=OPENAI_API_KEY)
ai_message = chat(INITIAL_CHAT_MODEL)

st.title("SliceOfAdventure")
st.markdown(ai_message.content)

prompt_agent = st.text_area(label="Fixed activity", value=f"Attend a kid friendly cultural event in {location}", label_visibility="hidden")

llm = OpenAI(temperature=0)

search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search"
    )
]

self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
result = self_ask_with_search.run(prompt_agent)

st.write(result)

if st.button('It works!'):
    st.balloons()
