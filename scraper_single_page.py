from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json

# Function to convert lakh to numeric value
def convert_lakh_to_numeric(value):
    if 'Lakh' in value:
        return float(value.replace(' Lakh', '').strip()) * 100000
    return int(value.replace(' Thousand', '').replace(',', '').strip()) * 1000

def main():
    try:
        url = 'https://www.bproperty.com/en/bangladesh/properties-for-rent/'
        webdriver_path = 'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        property_listings = soup.find_all('li', {'role': 'article', 'class': 'ef447dde'})
        # print(property_listings)

        cities = []
        regions = []
        property_types = []
        sizes = []
        num_bedrooms_list = []
        num_bathrooms_list = []
        prices = []
        image_urls = []

        # Loop through property listings
        for listing in property_listings:
            script_tag = listing.find('script', type='application/ld+json')
            if script_tag:
                json_data = json.loads(script_tag.string)

                # Extracting information from the JSON data
                if 'address' in json_data:
                    cities.append(json_data['address']['addressLocality'])
                    regions.append(json_data['address']['addressRegion'])

                if 'geo' in json_data:
                    latitude = json_data['geo']['latitude']
                    longitude = json_data['geo']['longitude']

                property_types.append(json_data['@type'])
                sizes.append(json_data['floorSize']['value'])
                num_bedrooms_list.append(json_data['numberOfRooms']['value'])
                num_bathrooms_list.append(json_data['numberOfBathroomsTotal'])
                image_urls.append(json_data['image'])

                # Extracting the price from the HTML content
                price_element = listing.find('span', class_='_14bafbc4')
                if price_element:
                    price_text = price_element.find_next_sibling('span', class_='f343d9ce').text
                    # Convert price text to a numerical value
                    price = convert_lakh_to_numeric(price_text)
                    prices.append(price)
                else:
                    prices.append(None)  # Append None if price is not found

        # Create a dictionary from the lists
        data = {
            'City': cities,
            'Region': regions,
            'Property Type': property_types,
            'Size(sqft)': sizes,
            'Bedrooms': num_bedrooms_list,
            'Bathrooms': num_bathrooms_list,
            'Price': prices,
            'Image URL': image_urls
        }

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Export the DataFrame to a CSV file
        df.to_csv('property_details.csv', index=False)

    except Exception as e:
        print(f"Error opening URL: {e}")

if __name__ == "__main__":
    main()
