import pandas as pd
from bs4 import BeautifulSoup
import json
import requests


# Function to convert lakh to numeric value
def convert_lakh_to_numeric(value):
    if 'Lakh' in value:
        return int(float(value.replace(' Lakh', '').strip()) * 100000)
    elif 'Thousand' in value:
        return int(float(value.replace(' Thousand', '').replace(',', '').strip()) * 1000)
    elif '.' in value:  # Check for decimal point
        return int(float(value.replace(',', '').strip()))  # Convert to float, then to int
    else:
        return int(value.replace(',', '').strip()) * 1000


def main():
    try:
        base_url = 'https://www.bproperty.com/en/bangladesh/properties-for-rent/page-'
        page_number = 2  # Start with page 1
        data_list = []  # Store data from all pages

        while True:
            url = base_url + str(page_number) + '/'
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch page {page_number}. Exiting loop.")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            property_listings = soup.find_all('li', {'role': 'article'})

            if not property_listings:
                print(f"No more listings found on page {page_number}. Exiting loop.")
                break

            names = []
            cities = []
            regions = []
            property_types = []
            sizes = []
            num_bedrooms_list = []
            num_bathrooms_list = []
            prices = []
            image_urls = []

            # Loop through property listings on one page
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
                    names.append(json_data['name'])
                    sizes.append(json_data['floorSize']['value'])
                    num_bedrooms_list.append(json_data['numberOfRooms']['value'])
                    num_bathrooms_list.append(json_data['numberOfBathroomsTotal'])
                    # Extracting the image URL from the JSON data
                    image_url = None
                    if 'image' in json_data:
                        image_url = json_data['image']
                    elif 'image' in json_data.get('potentialAction', {}):
                        image_url = json_data['potentialAction']['image']['url']

                    image_urls.append(image_url)

                # Extracting the price from the HTML content
                price_element = listing.find('span', class_='_14bafbc4')
                if price_element:
                    price_text = price_element.find_next_sibling('span', class_='f343d9ce').text
                    # Convert price text to a numerical value
                    price = convert_lakh_to_numeric(price_text)
                    prices.append(price)
                else:
                    prices.append(None)  # Append None if price is not found

                # Store all extracted data in a dictionary
                data = {
                    'Name': names,
                    'City': cities,
                    'Region': regions,
                    'Property Type': property_types,
                    'Size(sqft)': sizes,
                    'Bedrooms': num_bedrooms_list,
                    'Bathrooms': num_bathrooms_list,
                    'Price': prices,
                    'Image URL': image_urls
                }

                # Append data from this page to the list
                data_list.append(data)

            page_number += 1  # Move to the next page

        # Concatenate all the data collected from different pages into a single DataFrame
        if data_list:
            final_data = {key: sum([d.get(key, []) for d in data_list], []) for key in data_list[0].keys()}
            df = pd.DataFrame(final_data)
            df.to_csv('Data/property_details.csv', index=False)
        else:
            print("No data collected. Something went wrong.")

    except Exception as e:
        print(f"Error opening URL: {e}")


if __name__ == "__main__":
    main()
