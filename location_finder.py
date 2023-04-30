import requests
import urllib

# Code auto generated from chat gpt

def find_location_hours(text):
    # set up the API endpoint and parameters
    api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    location = text  # replace with the location you want to look up
    api_key = "AIzaSyC_1BBnpRXiR-Alk9_aXfLimwF5JDBpois"   # replace with your Google Places API key
    fields = "place_id"  # specify the fields you want to retrieve

    # construct the request URL
    params = {"input": location, "inputtype": "textquery", "fields": fields, "key": api_key}
    request_url = f"{api_url}?{urllib.parse.urlencode(params)}"

    # make the API request
    response = requests.get(request_url)

    # check if the request was successful
    if response.status_code == 200:
        # parse the response JSON data
        response_data = response.json()

        # extract the place ID from the response data
        place_id = response_data["candidates"][0]["place_id"]

        # construct a new request to retrieve the opening hours data
        api_url = "https://maps.googleapis.com/maps/api/place/details/json"
        fields = "opening_hours"  # specify the fields you want to retrieve
        params = {"placeid": place_id, "fields": fields, "key": api_key}
        request_url = f"{api_url}?{urllib.parse.urlencode(params)}"

        # make the API request
        response = requests.get(request_url)

        # check if the request was successful
        if response.status_code == 200:
            # parse the response JSON data
            response_data = response.json()
            #print(response_data)
            if response_data['result'] != {}:
                # extract the opening hours data
                opening_hours = response_data["result"]["opening_hours"]
                if opening_hours:
                    return opening_hours['periods']
    
    return False
