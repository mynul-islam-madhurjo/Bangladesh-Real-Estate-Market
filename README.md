# Real Estate Market Analysis - Bangladesh

## Problem Statement
The objective of this project was to collect and analyze real estate data for various cities and regions in Bangladesh from [Bproperty](https://www.bproperty.com/en/bangladesh/properties-for-rent/). <br/> 
After scraping and cleaning approximately 100k+ raw data points, I narrowed it down to 4421 unique property listings.

You can visit the public dashboard [here](https://public.tableau.com/app/profile/mynul.islam/viz/BangladeshRealEstateMarket/Dashboard1?publish=yes). 

## Findings and Observations from the [Dashboard](https://public.tableau.com/app/profile/mynul.islam/viz/BangladeshRealEstateMarket/Dashboard1?publish=yes)
Based on the analysis of the cleaned dataset, several key observations were made:

1. **Price Disparity between Dhaka and Chittagong:**
   - Dhaka exhibits significantly higher average property prices compared to Chittagong. 

2. **Price Variation by Property Type:**
   - In Dhaka, there's a substantial price difference between residences and apartments. Apartments in Chittagong are half the price of residences.

3. **Expensive Regions and Cities:**
   - In Dhaka, Gulshan emerges as the most expensive area. Other expensive areas include Baridhara, Uttara, Mirpur, and Bashundhara.
   - Khulshi stands out as the most expensive place in Chittagong.

## Build From Sources and Run the Selenium Scraper
1. Clone the repo
```bash
git clone https://github.com/mynul-islam-madhurjo/Bangladesh-Real-Estate-Market
```
2. Intialize and activate virtual environment
```bash
virtualenv --no-site-packages  venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Download Chrome WebDrive from https://chromedriver.chromium.org/downloads 
5. Run the scraper
```bash
python selenium_scraper/scraper.py --chromedriver_path <path_to_chromedriver>
```
6. You will get a file named `property_details.csv` containing all the required fields.

## Conclusion
The analysis sheds light on the significant price differences between different regions and property types in Bangladesh, particularly Dhaka and Chittagong. These insights can be valuable for real estate professionals, investors, and individuals interested in property markets in Bangladesh.

