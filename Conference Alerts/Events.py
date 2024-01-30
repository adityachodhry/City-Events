import requests
from bs4 import BeautifulSoup
import json

event_data = []
limit_events = 200
api_url = f"https://www.conferencealerts.in/advance_search/?limit_events_p={limit_events}"

body = {
    "limit_events_p": limit_events
}
# Make the GET request
response = requests.post(api_url, json = body)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    with open('Row_Data.html', 'w', encoding='utf-8') as html_file:
        html_file.write(response.text)
    
    events = soup.find_all('td', class_='listing-detal col-md-7')

    for event in events:

        event_name = event.find('a', class_='conflist').text.strip()
        location = event.find_next('td', class_='listing-place col-md-3').text.strip()
        date_element = event.find_next('td', class_='col-md-2 listing-date')
        date = date_element.h6.text.strip() if date_element and date_element.h6 else "Date not available"

        event_details = {
            'name': event_name,
            'date': date,
            'location': location
        }
        event_data.append(event_details)

    with open('Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(event_data, json_file, indent=2)

    print("Data Extracted!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")