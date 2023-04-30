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
# SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
# os.environ['SERPAPI_API_KEY'] = SERPER_API_KEY

# location = st.selectbox(
#     label='What is your location?',
#     options=('Brussels, Belgium', 'Antwerp, Belgium', 'Ghent, Belgium', 'Liège, Belgium',
#      'Leuven, Belgium', 'Namur, Belgium', 'Kortrijk, Belgium', 'Oostende, Belgium'))

# st.write('You selected:', location)

chat = ChatOpenAI(temperature=.9, openai_api_key=OPENAI_API_KEY)

st.title("🍕🎉 Slice Of Adventure")
st.text('Get inspired for fun things to do with your family')

with st.form("my_form"):
    st.text('First, tell us a bit about your family')
    
    st.header("Family composition")

    family_composition = st.text_area('How many family members are there, and what are their ages?', 
    ''' We are three people. I\'m a man of 41, my wife is 36. We have a daughter of 2,5 years old. ''')

    st.header("Interests and passions")
    col1, col2, col3 = st.columns(3)
    with col1:
        family_interests_art =  st.checkbox(":art: Art & Culture")
        family_interests_home = st.checkbox(":house: Stay at home")
        family_interests_entertainment = st.checkbox(":popcorn: Entertainment")
    with col2:
        family_interests_photography = st.checkbox(":camera_with_flash: Photography")
        family_interests_nature = st.checkbox(":deciduous_tree: Nature")
        family_interests_history = st.checkbox(":scroll: History")
    with col3:
        family_interests_sports = st.checkbox(":soccer: Sports")
        family_interests_fooddrink = st.checkbox(":ramen: Food & Drink")
        family_interests_hiddenplaces = st.checkbox(":triangular_flag_on_post: Hidden places")
    
    # Define a list of the selected checkbox labels
    selected_interests = []

    # Check each checkbox variable and add the label to the list if it's selected
    if family_interests_art:
        selected_interests.append("Art & Culture")
    if family_interests_home:
        selected_interests.append("Staying at home")
    if family_interests_entertainment:
        selected_interests.append("Entertainment")
    if family_interests_photography:
        selected_interests.append("Photography")
    if family_interests_nature:
        selected_interests.append("Nature")
    if family_interests_history:
        selected_interests.append("History")
    if family_interests_sports:
        selected_interests.append("Sports and being active")
    if family_interests_fooddrink:
        selected_interests.append("Eating and drinking")
    if family_interests_hiddenplaces:
        selected_interests.append("Discovering hidden places")

    family_selected_interests = ", ".join(selected_interests)

    st.divider()

    submitted = st.form_submit_button("Get suggestions")

    if submitted:

        family_location = "Brussels, Belgium (postal code 1000)"

        profile_template = """
        We live in: {family_location}

        This is how many family members there are, and their ages: {family_composition} 

        Our family loves the following types of activies: {family_selected_interests}
        Make sure to focus on these types with your suggestions.

        We prefer these types of activities: {family_activity_focus} 

        Please suggest activities that we can do next weekend.

        Start your response with a concise summary of our interests to show that you tailored your results.
        """
        prompt = PromptTemplate(
            template = profile_template,
            input_variables = ["family_location", "family_composition", "family_selected_interests"],
        )

        final_prompt = prompt.format(family_location=family_location, family_composition=family_composition, family_selected_interests=family_selected_interests)

        print (f"Final prompt: {final_prompt}")

        INITIAL_CHAT_MODEL = [
            SystemMessage(content="Act as a parent that is highly skilled in organising engaging past time activities for the family. You excell at finding and suggesting a wide range of family activities. You're great at finding both special activities to go do with the family but also in finding fun and creative ways to turn a mundane day in the house into a fun experience. "),
            HumanMessage(content="Your task is to help me plan a diverse calendar with activities for my family. Make sure to include all ranges of activies. For example, it can be everyday activities at home with the family, or also special activities or events in the neigborhood. You could also include parents-only night out (with babysit?). Mix it up."),
            AIMessage(content="Tell me more about your family so I can provide suggestions tailored your needs and preferences."),
            HumanMessage(content=final_prompt),
            AIMessage(content="Great! I'll give you a list of suggestions for the next weekend, taking into account that today is {today_human}. Each suggestion is structured in Markdown. I'll give four suggestions per day."),
        ]

        ai_message = chat(INITIAL_CHAT_MODEL)
        st.markdown(ai_message.content)
