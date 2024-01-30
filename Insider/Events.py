import requests
import json
from datetime import datetime

event_data = []
city = 'mumbai'
event_type = 'physical'

api_url = f"https://api.insider.in/home?city={city}&eventType={event_type}&filterBy=go-out&norm=1&select=lite&typeFilter={event_type}"

# Make the GET request
response = requests.get(api_url)

if response.status_code == 200:

    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('list', {}).get('masterList', {}).values()
    for event in data:

        min_show_start_time_timestamp = event.get('min_show_start_time')
        max_show_end_time_timestamp = event.get('max_show_end_time')

        # Convert timestamps to human-readable format
        start_time = datetime.fromtimestamp(min_show_start_time_timestamp).strftime('%Y-%m-%d')
        end_time = datetime.fromtimestamp(max_show_end_time_timestamp).strftime('%Y-%m-%d')


            # Append the extracted data to the list
        e_data = {
            'eventId': event.get('_id'),
            'start_time': start_time,
            'end_time': end_time,
            'name': event.get('name'),
            'type': event.get('type')
        }
        event_data.append(e_data)
    # Save the extracted data to a new JSON file
    with open('Event_Data.json', 'w') as json_file:
        json.dump(event_data, json_file, indent=2)
    
else:
    print(f"Error: {response.status_code}")
