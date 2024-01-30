import requests
from bs4 import BeautifulSoup
import json

event_data = []
page_no = 1
city = 'Delhi'

while True:
    api_url = f"https://www.conferencealerts.in/{city}/page/{page_no}"

    response = requests.get(api_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        events = soup.find_all('td', class_='listing-detal col-md-7')

        if not events:
            # No more data on the page, break out of the loop
            break

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

        print(f"Page {page_no} data extracted.")
        page_no += 1
    else:
        print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")
        break  # Break out of the loop on error

# Store the collected data in a JSON file
with open('Event_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(event_data, json_file, indent=2)

print("All data extracted!")
