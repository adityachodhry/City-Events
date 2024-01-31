import requests
from bs4 import BeautifulSoup
import json

event_data = []

headers = {
    "Cookie": "ajs_anonymous_id=1550c366-70a5-43f1-b1b3-3f5674539316",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

api_url = "https://theindia100.com/event-calendar/january/"

response = requests.get(api_url, headers=headers)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    with open('Row_Data.html', 'w', encoding='utf-8') as html_file:
        html_file.write(response.text)

    month_elements = soup.find_all(class_='eventblock')

    for month in month_elements :
        month_name = month.find('h3').text.strip()
        print(month_name)

        thumb = month.find_all(class_='thumbnail')

        for thumnail in thumb :
            event_elements = thumnail.find_all(class_='info')
            for event_element in event_elements :
                event_name = event_element.find('h4').text.strip()
                location = event_element.find('span', {'class': 'location'}).text.strip()
                date = thumnail.find('span', {'class': 'datemobile'}).text.strip()
                print(f"{event_name}:{location}:{date}")

                event_info = {
                'month': month_name,
                'date': date, 
                'location': location,
                'eventName': event_name,
                # 'description': description
            }

            event_data.append(event_info)

# Save the extracted data to a JSON file
with open('Event_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(event_data, json_file, ensure_ascii=False, indent=2)

print("All data extracted!")