import requests
import datetime
from utils import loadJson

# Test Description
    # a. Build the url and fetch data fom endpoint using python's requests library - make a GET call to retrieve data

# A. Parse the following form input provided: Obtain endpoint, token and timestamp from input
userInput = loadJson()
url = userInput[0]
unix_timestamp = userInput[1]
my_token = userInput[2]

# B. process day, hours and minutes from input timestamp (Convert unix to UTC format and parse required data)
date_time_day = datetime.datetime.fromtimestamp(int(unix_timestamp))
hour = date_time_day.strftime("%H")
minutes = date_time_day.strftime("%M")
day = date_time_day.strftime("%A")

# C. Create a dictionary mapping to map days of week with the position in week: egs: Sunday --> 0, Monday --> 1 etc
    # Creating a map for lookup sic=nce with the format used above, day results a string name denoting day of week(Monday etc)
    # For any input timestamp given, get the day of week and obtain the position in week for api call to return data correctly

days = {'Sunday' : 0, 'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 'Friday' : 5, 'Saturday' : 6}

# D. Function to obtain data from api
    # Pass in the token obtained along with day, hour and minutes
def get_data_from_api(token, hour, minutes, day):
    
    # enclose within try block --> request MAY not always be successful
    try:
        # pass in the params to the url to request data 
        url = "https://api.filtered.ai/q/foodtruck?hour={}&minutes={}&dayOrder={}".format(hour, minutes, days[day])

        # for api call to give a 200 status code(successful, authorization header is required of type basic)
        api_response = requests.get(url, headers={'Authorization': 'Basic %s' %token})
        
        if api_response == 200:
            data = api_response.json()
            # if no matches there is an empty response given --> {'data': []} 
            return data

        else:
            # print(api_response)
            return 'N/A'

    # If endpoint hits an error, print "N/A" (without quote)
    except requests.exceptions.RequestException as error:
        response = 'N/A'
        return response

# call the above module

api_data = get_data_from_api(my_token, hour, minutes, day)
print(api_data)

if not api_data == 'N/A':
    if len(api_data) > 1:
        # match of foodtrucks for input timestamp found
        len_of_entries = len(api_data['data'])

        # api_data consists of dictionaries with len_of_entries matches, go over index and get foodtruck name and location
        for idx in range(0, len_of_entries):
            
            food_truck_name = api_data['data'][idx]['Applicant']
            food_truck_location = api_data['data'][idx]['locationid']
            print(food_truck_name, food_truck_location, sep=', ')

    else:
        # no matches are found for the input timestamp we entered, call returns : {'data': []} 
        print('N/A')

    
