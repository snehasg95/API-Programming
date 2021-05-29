import requests
import datetime
from collections import OrderedDict
from utils import loadJson

# Test Description
    # a. Build the url and fetch data fom endpoint using python's requests library - make a GET call to retrieve data

#  Create a dictionary mapping to map days of week with the position in week: egs: Sunday --> 0, Monday --> 1 etc
    # Creating a map for lookup sic=nce with the format used above, day results a string name denoting day of week(Monday etc)
    # For any input timestamp given, get the day of week and obtain the position in week for api call to return data correctly

days = {'Sunday' : 0, 'Monday' : 1, 'Tuesday' : 2, 'Wednesday' : 3, 'Thursday' : 4, 'Friday' : 5, 'Saturday' : 6}

# D. Function to obtain data from api
    # Pass in the token obtained along with day, hour and minutes
def get_data_from_api(token, hour, minutes, day):
    
    # enclose within try block --> request MAY not always be successful
    try:
        # pass in the params to the url to request data 
        url = 'https://api.filtered.ai/q/foodtruck?hour={}&minutes={}&dayOrder={}'.format(hour, minutes, days[day])

        # for api call to give a 200 status code(successful, authorization header is required of type basic)

        api_response = requests.get(url, headers={'Authorization': 'Basic %s' %token})
        if api_response.status_code == 200:
            data = api_response.json()
    
            # if no matches there is an empty response given --> {'data': []} 
            return data

        else:
            return 'N/A'

    # If endpoint hits an error, print "N/A" (without quote)
    except requests.exceptions.RequestException as error:
        return 'N/A'


def convert_time_start(time):
    if time == '12AM':
        time_24 = 0
    
    else:
        if time[-2:] == 'AM':
            time_24 = int(time[:-2])

        elif time == '12PM':
            time_24 = 12

        else:
            time_24 = int(time[:-2]) + 12
    
    return time_24


def convert_time_end(time):
    if time == '12AM':
        time_24 = 24
    
    else:
        if time[-2:] == 'AM':
            time_24 = int(time[:-2])

        else:
            time_24 = int(time[:-2]) + 12
    return time_24


def sort_food_truck(api_data, current_time):

    available_food_trucks = []

    if not api_data == 'N/A':
        len_of_entries = len(api_data['data'])

        if len_of_entries > 1:
            
            # match of foodtrucks for input timestamp found

            # api_data consists of dictionaries with len_of_entries matches, go over index and get foodtruck name and location
            for idx in range(0, len_of_entries):
                start_time = api_data['data'][idx]['starttime']
                end_time = api_data['data'][idx]['endtime']
                
                start_time_24hr = convert_time_start(start_time)
                end_time_24hr = convert_time_end(end_time)
                
                # compare if AM or PM
                # current_time = hour_conversion(hour)
                if start_time_24hr <= int(current_time) < end_time_24hr:
                    available_food_trucks.append((api_data['data'][idx]['Applicant'], api_data['data'][idx]['locationid']))
            
            # for food_truck_name, food_truck_location in sorted(d.items()):
            available_food_trucks.sort()
            return available_food_trucks

        else:
            # no matches are found for the input timestamp we entered, call returns : {'data': []} 
            return 'N/A'

    else:
        return 'N/A'



### Testing ##

# A. Parse the following form input provided: Obtain endpoint, token and timestamp from input
    # Assumptions:
        # a. 3 inputs will be given, in order to parse at index values

userInput = loadJson()
url = userInput[0]
unix_timestamp = userInput[1]
my_token = userInput[2]

# B. process day, hours and minutes from input timestamp (Convert unix to UTC format and parse required data)
date_time_day = datetime.datetime.fromtimestamp(int(unix_timestamp))
hour = date_time_day.strftime("%H")
minutes = date_time_day.strftime("%M")
day = date_time_day.strftime("%A")

# C. call Modules
api_data = get_data_from_api(my_token, hour, minutes, day)

available_food_trucks = sort_food_truck(api_data, hour)
if available_food_trucks != 'N/A':
    for pair in available_food_trucks:
        food_truck_name = pair[0]
        food_truck_location = pair[1]
        print(food_truck_name, food_truck_location, sep=', ')
else:
    print('N/A')

