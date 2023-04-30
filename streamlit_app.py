import streamlit as st
import os
import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from time import strftime
today_human = strftime("%a, %d %b %Y")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
os.environ['SERPAPI_API_KEY'] = SERPER_API_KEY

location = st.selectbox(
    label='What is your location?',
    options=('Brussels, Belgium', 'Antwerp, Belgium', 'Ghent, Belgium', 'Liège, Belgium',
     'Leuven, Belgium', 'Namur, Belgium', 'Kortrijk, Belgium', 'Oostende, Belgium'))

st.write('You selected:', location)

chat = ChatOpenAI(temperature=.9, openai_api_key=OPENAI_API_KEY)

st.title("🍕🎉 Slice Of Adventure")
st.text('Get inspired for fun things to do with your family')


with st.form("my_form"):
    st.text('First, tell us a bit about your family')
    
    family_composition = st.text_area('How many family members are there, and what are their ages?', 
    ''' We are three people. I\'m a man of 41, my wife is 36. We have a daughter of 2,5 years old. ''')
    
    family_interests = st.text_area('What are the general interests or hobbies of each family member?', 
    ''' We like music, playing, walking around, nature, playgrounds, eating out, inviting friends for dinner. Some culture too. We don't have specific hobbies. ''')

    family_activity_focus = st.text_area('Is there a specific focus for the activities, such as learning, bonding, fitness, or relaxation?', 
    ''' There's no specific focus. But a good balance might be nice. ''')

    submitted = st.form_submit_button("Submit")
    if submitted:

        family_location = "Brussels, Belgium (postal code 1000)"

        # family_composition = "We are three people. I\'m a man of 41, my wife is 36. We have a daughter of 2,5 years old."
        # family_interests = "We like music, playing, walking around, nature, playgrounds, eating out, inviting friends for dinner. Some culture too. We don't have specific hobbies."
        # family_activity_focus = "There's no specific focus. But a good balance might be nice."

        profile_template = """
        We live in: {family_location}

        This is how many family members there are, and their ages: {family_composition} 

        And these are our general interest or hobbies: {family_interests}

        We prefer these types of activities: {family_activity_focus} 

        Please suggest activities that we can do next weekend.
        """
        prompt = PromptTemplate(
            template = profile_template,
            input_variables = ["family_location", "family_composition", "family_interests", "family_activity_focus"],
        )

        final_prompt = prompt.format(family_location=family_location, family_composition=family_composition, family_interests=family_interests, family_activity_focus=family_activity_focus)

        print (f"Final prompt: {final_prompt}")

        INITIAL_CHAT_MODEL = [
            SystemMessage(content="Act as a parent that is highly skilled in organising engaging past time activities for the family. You excell at finding and suggesting a wide range of family activities. You're great at finding both special activities to go do with the family but also in finding fun and creative ways to turn a munday day in the house into a fun experience."),
            HumanMessage(content="Your task is to help me plan a diverse calendar with activities for my family. Make sure to include all ranges of activies. For example, it can be everyday activities at home with the family, or also special activities or events in the neigborhood. Mix it up."),
            AIMessage(content="Tell me more about your family so I can provide suggestions tailored your needs and preferences."),
            HumanMessage(content=final_prompt),
            AIMessage(content="Great! I'll give you a list of suggestions for the next weekend, taking into account that today is {today_human}. Each suggestion is structured in Markdown. I'll give three suggestions per day"),
        ]


        ai_message = chat(INITIAL_CHAT_MODEL)
        st.markdown(ai_message.content)
