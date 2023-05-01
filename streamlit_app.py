import streamlit as st
import requests
import openai
import pycountry
from datetime import datetime
from dictor import dictor
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.agents import initialize_agent

import folium
from streamlit_folium import st_folium, folium_static
from utils import get_location, get_country_code, get_cities, get_next_weekday, SATURDAY_DOW, SUNDAY_DOW, select_weather_prediction_by_date, get_forecast

from langchain.prompts import PromptTemplate
from time import strftime
today_dt: datetime = datetime.today()
today_human = strftime("%a, %d %b %Y")

next_sat :datetime = get_next_weekday(startdate=today_dt, weekday=SATURDAY_DOW)
next_sat_human :str = next_sat.strftime('%A %d %b %Y')
next_sun :datetime = get_next_weekday(startdate=today_dt, weekday=SUNDAY_DOW)
next_sun_human : str = next_sun.strftime('%A %d %b %Y')

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
# SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
# os.environ['SERPAPI_API_KEY'] = SERPER_API_KEY
OPENWEATHERMAP_API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
GMAPS_API_KEY=st.secrets["GMAPS_API_KEY"]

# m = folium.Map(location=my_country_latlon, width=750, height=500, zoom_start=3, control_scale=True)

weather = OpenWeatherMapAPIWrapper()

chat = ChatOpenAI(temperature=.9, openai_api_key=OPENAI_API_KEY)

st.title("💡🎉 Weekend wonders")
st.subheader('Find fun things to do with your family next weekend')

st.header(":world_map: Country")

all_countries = [c.name.capitalize() for c in pycountry.countries]
my_country = st.selectbox(label="Which country?", options=all_countries)

with st.form("my_form"):

    my_country_latlon = get_location(my_country)

    try:
        my_country_lat = my_country_latlon[0]
        my_country_lon = my_country_latlon[1]
    except Exception:
        my_country_lat = 40.7127281
        my_country_lon = -74.0060152

    st.header(":classical_building: City")

    my_country_code = get_country_code(lat=my_country_lat, lon=my_country_lon)
    my_cities = get_cities(country_code=my_country_code)
    my_cities_capitalized = [city.capitalize() for city in my_cities]

    location = st.selectbox(label='Which city?', options=my_cities_capitalized)
    
    # Profile
    st.header(":family: Who are you?")

    family_composition = st.text_area('How many family members are there, and what are their ages?', 
    ''' We are three people. I\'m a man of 41, my wife is 36. We have a daughter of 2,5 years old. ''', 50)

    # Interests
    st.header(":thinking_face: What do you feel like doing?")
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
    
    selected_interests = []

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

    # Originality
    st.header(":gift: Can we surprise you?")
    family_openness = st.select_slider("How original can the suggestions be?", options=("Stick strictly to my selections", "I'm also open to new things.", "Go bonkers!"))

    if family_openness == "I'm also open to new things." :
        family_openness = "I'm also open to new things. Suggest a balanced mix of activities based on the things I love, and also mix in a few other types of activities"
    
    if family_openness == "Go bonkers!" :
        family_openness = "Get creative with your answers. Suggest wildly different types of acitivities and you can go over the top with the ideas. The activities can be elaborate and out of the ordinary."

    st.divider()

    submitted = st.form_submit_button("Get suggestions")

    if submitted:

        with st.spinner(f'Looking for good times in {location}, {my_country_code.upper()} on {next_sat_human} and {next_sun_human} ...'):

            my_city_latlon = get_location(f"{location},{my_country_code}")
            my_city_lat = my_city_latlon[0]
            my_city_lon = my_city_latlon[1]

            exclude_parts = "minutely,hourly,alerts"
            weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={my_city_lat}&lon={my_city_lon}&appid={OPENWEATHERMAP_API_KEY}&exclude={exclude_parts}&units=metric"
            weather_data = requests.get(weather_url).json()
            # st.write(weather_data)

            weather_data_sat = select_weather_prediction_by_date(weather_data.get("daily"), next_sat)
            weather_data_sun = select_weather_prediction_by_date(weather_data.get("daily"), next_sun)

            # st.write(weather_data_sat)
            # st.write(weather_data_sun)

            weather_forecast_sat = get_forecast(weather_data_sat)
            weather_forecast_sun = get_forecast(weather_data_sun)

            weather_icon_sat = dictor(weather_data_sat, "weather.0.icon")
            weather_icon_url_sat = f"http://openweathermap.org/img/w/{weather_icon_sat}.png"
            weather_icon_sun = dictor(weather_data_sun, "weather.0.icon")
            weather_icon_url_sun = f"http://openweathermap.org/img/w/{weather_icon_sun}.png"

            family_location = f"{location}, {my_country_code.upper()}"

            profile_template = """
            We live in: {family_location}

            This is how many family members there are, and their ages: {family_composition} 

            Our family loves the following types of activies: {family_selected_interests}
            
            I shared this overview of the types of activities that we love. And would like you to treat this suggestions in this way: {family_openness}.

            Now please suggest activities that we can do next weekend.

            The weather forecast for {next_sat_human}: {weather_forecast_sat}
            The weather forecast for {next_sun_human}: {weather_forecast_sun}

            Please take this weather forecast into account when making your suggestions.

            Start your response with a concise summary of our interests to show that you tailored your results.
            Also add one weather emoji per day, the temperature and how to dress accordingly.
            """
            prompt = PromptTemplate(
                template = profile_template,
                input_variables = ["family_location",
                                   "family_composition",
                                   "family_selected_interests",
                                   "family_openness",
                                   "weather_forecast_sat",
                                   "weather_forecast_sun",
                                   "next_sat_human",
                                   "next_sun_human"],
            )

            final_prompt = prompt.format(
                family_location=family_location,
                family_composition=family_composition,
                family_selected_interests=family_selected_interests,
                family_openness=family_openness,
                weather_forecast_sat=weather_forecast_sat,
                weather_forecast_sun=weather_forecast_sun,
                next_sat_human=next_sat_human,
                next_sun_human=next_sun_human)

            print (f"Final prompt: {final_prompt}")
            print (f"family_openness: {family_openness}")

            # st_data = st_folium(m, width=700)

            INITIAL_CHAT_MODEL = [
                SystemMessage(content="Act as a parent that is highly skilled in organising engaging past time activities for the family. You excell at finding and suggesting a wide range of family activities. You're great at finding both special activities to go do with the family but also in finding fun and creative ways to turn a mundane day in the house into a fun experience. "),
                HumanMessage(content="Your task is to help me plan a diverse calendar with activities for my family. Make sure to include all ranges of activies. For example, it can be everyday activities at home with the family, or also special activities or events in the neigborhood. You could also include parents-only night out (with babysit?). Mix it up. Know that we are locals, so please do not suggest typical touristic destinations."),
                AIMessage(content="Tell me more about your family so I can provide suggestions tailored your needs and preferences."),
                HumanMessage(content=final_prompt),
                AIMessage(content=f"Great! I'll give you a list of suggestions formatted in json for the next weekend {next_sat_human} and {next_sun_human}. I'll also return four suggestions per day (day of the week in words only). Every suggestion should contain the descriptions of the activities (description), the names of the places (place_name), the url associated with those places.")
            ]

            ai_message = chat(INITIAL_CHAT_MODEL)
            llm_result_str = ai_message.content

            # Clean the content (it can have text before or after the json)
            if llm_result_str[0] != '{':
                llm_result_str = llm_result_str[llm_result_str.find('{'):]
            if llm_result_str[-1] != '}':
                llm_result_str = llm_result_str[:-len(llm_result_str)+llm_result_str.rindex('}')+1]

            # transform the output to json
            import ast
            llm_result_dict = ast.literal_eval(llm_result_str)

            st.title("Suggestions for next weekend")
            
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
                st.header(day)

                if day == 'Saturday' and weather_icon_url_sat:
                    col1, col2 = st.columns([1,10])
                    with col1:
                        st.image(weather_icon_url_sat)
                    with col2:
                        st.markdown(f"#### {weather_forecast_sat}")
                elif day == 'Sunday' and weather_icon_url_sun:
                    col1, col2 = st.columns([1,10])
                    with col1:
                        st.image(weather_icon_url_sun)
                    with col2:
                        st.markdown(f"#### {weather_forecast_sun}")

                day_int = 0
                try:
                    day_int=days_of_week[day]
                except KeyError:
                    pass
                for act in activities:
                    hours = find_location_hours(act['place_name'], GMAPS_API_KEY)
                    if hours:
                        for h in hours:
                            activities_with_hours[act['place_name']] = act['place_name']
                            open = h['open']
                            if str(open['day']) == str(day_int):
                                if open['time'] == '0000':
                                    activities_with_hours[act['place_name']] += " (Always Open)"
                                else:
                                    activities_with_hours[act['place_name']] += " (Open time: %s" % open['time']
                            if 'close' in h:
                                close = h['close']
                                if close['day'] == day_int:
                                    activities_with_hours[act['place_name']] += " - %s)" % close['time']
                        st.markdown("* " + act['description'].replace(act['place_name'],activities_with_hours[act['place_name']]))
                    else:
                        st.markdown("* " + act['description'])
