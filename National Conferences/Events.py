import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def get_formatted_date(date):
    return date.strftime('%Y-%m-%d')

def split_date_and_location(date_and_location):
    parts = date_and_location.split('/')
    date_part = parts[0].strip()
    location_part = parts[1].strip()
    return {'date': date_part, 'location': location_part}

event_data = []
place = 'New%20Delhi'
start_date = datetime(2024, 1, 31)
end_date = datetime(2024, 12, 31)

current_date = start_date

while current_date <= end_date:
    formatted_date = get_formatted_date(current_date)
    api_url = f"https://nationalconferences.org/conference.php?dt={formatted_date}&place={place}"

    response = requests.get(api_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        with open('Row_Data.html', 'w', encoding='utf-8') as html_file:
            html_file.write(response.text)

        events = soup.find_all('div', class_='psdt')

        for event in events:
            date_and_location = event.find('h3').text.strip()
            split_data = split_date_and_location(date_and_location)

            topic_div = event.find_next_sibling('div', class_='pstopic')
            topic_name = topic_div.find('p').text.strip()

            event_data.append({
                'topic_name': topic_name,
                'date': split_data['date'],
                'location': split_data['location']
                
            })

    current_date += timedelta(days=1)

# Save data to JSON file
with open('Event_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(event_data, json_file, ensure_ascii=False, indent=2)
