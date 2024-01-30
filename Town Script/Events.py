import requests
import json
from datetime import datetime

event_data = []
size = 10
distance = 50
page_no = 1


api_url = f"https://www.townscript.com/listings/event/radar?lat=13.0826802&lng=80.2707184&radarDistance={distance}&page={page_no}&size={size}"

body = {

    "minScore": 1
}
# Make the GET request
response = requests.post(api_url, json = body)

if response.status_code == 200:

    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('data', {}).get('data', [])

    for event in data:

        # Convert timestamps to the desired format
        start_time = datetime.fromisoformat(event.get('startTime')).strftime("%Y-%m-%d")
        end_time = datetime.fromisoformat(event.get('endTime')).strftime("%Y-%m-%d")

        e_data = {
            'Id': event.get('id'),
            'eventID': event.get('eventId'),
            'startTime': start_time,
            'endTime': end_time,
            'name': event.get('displayName'),
            'city': event.get('city')
        }
        event_data.append(e_data)
    # Save the extracted data to a new JSON file
    with open('Event_Data.json', 'w') as json_file:
        json.dump(event_data, json_file, indent=2)
    
else:
    print(f"Error: {response.status_code}")
