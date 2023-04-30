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
        I'll return a json with 3 suggestion per day.
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
            AIMessage(content="I'll return a json with 3 suggestion per day. Every suggestion should contain the descriptions of the activities, the names of the places, the url associated with those places, without any message after the json.")
        ]


        from pydantic import BaseModel, Field, validator
        from langchain.output_parsers import PydanticOutputParser

        # Define your desired data structure.
        class Activity(BaseModel):
            #day: str = Field(description="day of the week")
            text: str = Field(description="description of the activity")
            #location_name: str = Field(description="named entity of the location")
            
        # Set up a parser + inject instructions into the prompt template.
        parser = PydanticOutputParser(pydantic_object=Activity)

        from langchain.chains import LLMChain, TransformChain
        from langchain.chains import SequentialChain, SimpleSequentialChain

        llm = OpenAI(temperature=.9, openai_api_key=OPENAI_API_KEY)
        llm_chain = LLMChain(
            prompt=prompt,
            llm=llm,
            output_key="json_string",
        )

        def parse_output(inputs: dict) -> dict:
            text = inputs["json_string"]
            return {"result": parser.parse(text)}

        transform_chain = TransformChain(
            input_variables=["json_string"],
            output_variables=["result"],
            transform=parse_output
        )

        chain = SequentialChain(
            input_variables=["family_location", "family_composition", "family_interests", "family_activity_focus"],
            output_variables=["result"],
            chains=[llm_chain, transform_chain],
        )

        #chain = SimpleSequentialChain(chains=[llm_chain, transform_chain], verbose=True)

        a = chain.run(prompt=prompt,family_location=family_location, family_composition=family_composition, family_interests=family_interests, family_activity_focus=family_activity_focus)
        print(a)
        print(type(a))
        st.write(a)
        st.title("Suggestions for next weekend")



        
        #llm_result = { "Saturday": [ { "name": "Visit the Royal Palace of Brussels.", "url": "https://www.monarchie.be/en/visit-palace-brussels", "description": "Take a guided tour of the palace and learn about its history and architecture. You'll get to see the Throne Room, the Mirror Room, and the Goya Room. ", "indoor": True }, { "name": "Visit the Musée Magritte Museum.", "url": "https://www.fine-arts-museum.be/en/museums/musee-magritte-museum", "description": "Explore the surreal art of René Magritte. The museum has an extensive collection of his works, including paintings, drawings, and sculptures.", "indoor": True }, { "name": "Bois de la Cambre", "url": "https://visit.brussels/en/place/Bois-de-la-Cambre", "description": "Take a walk in the beautiful park and enjoy the nature. You can also have a picnic or rent a paddleboat on the lake.", "indoor": False } ], "Sunday": [ { "name": "Visit Mini-Europe.", "url": "https://www.minieurope.com/en/", "description": "Explore Europe's most famous landmarks in miniature form. The park has over 350 models, including the Eiffel Tower, the Atomium, and the Colosseum.", "indoor": True }, { "name": "Explore the Atomium.", "url": "https://www.atomium.be/", "description": "Visit the iconic Atomium, a unique example of mid-century modern architecture. You'll get to see the permanent exhibition, as well as temporary exhibitions.", "indoor": True }, { "name": "Visit Parc de Bruxelles", "url": "https://visit.brussels/en/place/Parc-de-Bruxelles", "description": "Take a walk in the beautiful park, feed the ducks and have a picnic or walk around the Royal Palace of Brussels.", "indoor": False } ] }
        st.write(llm_result_str)
        days_of_week = {'Monday': 1,
                        'Tuesday': 2, 
                        'Wednesday': 3, 
                        'Thursday': 4,
                        'Friday': 5,
                        'Saturday': 6,
                        'Sunday': 0}

        from location_finder import find_location_hours
        activities_with_hours = {}
        for day, activities in llm_result_dict.items():
            st.write(day)
            day_int=days_of_week[day]
            #st.write(activities)
            for act in activities:
                hours = find_location_hours(act['name'])
                st.write(act['name'])
                if hours:
                    for h in hours:
                        #activities_with_hours[]
                        open = h['open']
                        if open['day'] == day_int:
                            if open['time'] == '0000':
                                st.write("Open time: Always")
                            else:
                                st.write("Open time: %s" % open['time'])
                        if 'close' in h:
                            close = h['close']
                            if close['day'] == day_int:
                                st.write("Open time: %s" % close['time'])
                else:
                    st.write("no hours")


        