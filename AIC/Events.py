import requests
from bs4 import BeautifulSoup
import json

event_data = []
page_no = 10

for page_no in range(1, page_no + 1):
    api_url = f"https://www.allinternationalconference.com/country/india-conference/{page_no}"

    response = requests.get(api_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')


        event_elements = soup.find_all(class_='confer-featur-top')

        for event in event_elements:

            date_element = event.find('h5')
            date = date_element.find_next('span').text.strip() if date_element else None

            location_element = event.find('span', itemprop='areaServed')
            location = location_element.text if location_element else None

            event_id_element = event.find('h6')
            event_id = event_id_element.text.split(': ')[1] if event_id_element else None

            event_name_element = event.find('span', itemprop='name')
            event_name = event_name_element.text if event_name_element else None

            # Store the extracted data in a dictionary
            event_info = {
                'date': date,
                'location': location,
                'eventId': event_id,
                'eventName': event_name
            }

            # Append the dictionary to the list
            event_data.append(event_info)
        
        print(f"Page {page_no} data extracted.")
        # page_no += 1
    else:
        print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")
        break


# Save the extracted data to a JSON file
with open('Event_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(event_data, json_file, ensure_ascii=False, indent=2)

print("All data extracted!")