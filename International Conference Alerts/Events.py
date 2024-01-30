import requests
from bs4 import BeautifulSoup
import json

headers = {
    "X-Requested-With": "XMLHttpRequest"
}

api_url = "https://internationalconferencealerts.com/pagination/searchfresult/fetch_data?country=India&topic=Medicine&subtopic=null&month=february&page=1"

# Make the GET request
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element with the class "t-scroll"
    t_scroll_element = soup.find('div', class_='t-scroll')

    if t_scroll_element:
        # Extract h3, h5, h6, and location data within the "t-scroll" element
        h3_data = [h3.text.strip() for h3 in t_scroll_element.find_all('h3')]
        h5_data = [h5.text.strip() for h5 in t_scroll_element.find_all('h5')]
        h6_data = [h6.text.strip() for h6 in t_scroll_element.find_all('h6')]
        location_data = [loc.text.strip() for loc in t_scroll_element.find_all('div', class_='c-loc')]

        # Create a list of dictionaries with the extracted data
        event_data = []
        for h3_text, h5_text, h6_text, location_text in zip(h3_data, h5_data, h6_data, location_data):
            # Format the date strings
            event_day_month = f"{h6_text}-{h5_text}"

            e_data = {
                'eventName': h3_text,
                'eventDate': event_day_month,
                'eventLocation': location_text
            }
            event_data.append(e_data)

        # Save the extracted data to a JSON file
        with open('Event_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(event_data, json_file, indent=2)

        print("Data extracted!")
    else:
        print("No element with class 't-scroll' found in the HTML.")
else:
    print(f"Error: {response.status_code}")
