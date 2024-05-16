import pandas as pd
from bs4 import BeautifulSoup
import requests
import uuid

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
}

data = []

for page_number in range(1, 20):
    url = f"https://www.bkmkitap.com/edebiyat-kitaplari?pg={page_number}"
    page = requests.get(url, headers=headers).text  # connect to the website
    soup = BeautifulSoup(page, "html.parser")
    product_items = soup.find_all("div", class_="col col-3 col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease")
    print(f"Scraping page {page_number}...")

    # Iterate over each product on the current page
    for i in product_items:
        # Create a dictionary to store the scraped data for each product
        product_data = {}

        product_data['Unique ID'] = str(uuid.uuid4())

        # Extracting book name
        product_data['Book Name'] = i.find("a", class_="fl col-12 text-description detailLink").text.strip()

        # Extracting publisher
        product_data['Publisher'] = i.find("a", class_="col col-12 text-title mt").text.strip()

        # Extracting author
        product_data['Author'] = i.find("a", class_="fl col-12 text-title").text.strip()

        # Extracting discounted price
        try:
            product_data['Discounted Price'] = i.find("div", class_="text-line discountedPrice").text.strip().split("\n")[0].strip()
        except AttributeError:
            product_data['Discounted Price'] = None
        try:
             # Extracting discount percentage
            product_data['Discount Percentage'] = i.find("div", class_="text-line discountedPrice").find("span").text.strip()[1:4]
            print(i.find("div", class_="text-line discountedPrice").find("span").text.strip()[1:3])
        except AttributeError:
            product_data['Discount Percentage'] = None

        new_price = i.find("div", class_="currentPrice").text.strip().split("\n")[0].strip()
        product_data['New Price'] = new_price.replace('TL', '')

        img_url = i.find("img", class_="stImage")["data-src"]
        product_data['Image URL'] = img_url

        # Append the dictionary to the list
        data.append(product_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('scraped_data.csv', index=False)

print("Data saved to 'scraped_data.csv'")