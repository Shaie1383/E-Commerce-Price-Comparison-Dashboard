import json
import os
from bs4 import BeautifulSoup

def scrape_amazon(mock_file_path):
    # Read the local HTML file
    with open(mock_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    products = []

    product_divs = soup.find_all("div", class_="product")
    for div in product_divs:
        name = div.find("span", class_="product-name").get_text(strip=True)
        price_text = div.find("div", class_="product-price").get_text(strip=True).replace('₹', '').replace(',', '')
        price = float(price_text)
        availability = div.find("div", class_="product-availability").get_text(strip=True)

        # Print to confirm product data is being fetched
        print(name, price, availability)  # This will print the values inside the loop

        products.append({
            "id": None,
            "name": name,
            "price": price,
            "stock_status": availability,
            "platform": "Amazon"
        })

    return products

def save_to_json(products):
    # Debugging statement
    print(f"Saving {len(products)} products to JSON...")  # This confirms how many products are being saved

    if os.path.exists('products.json'):
        with open('products.json', 'r') as json_file:
            data = json.load(json_file)
    else:
        data = {"products": []}

    data["products"].extend(products)

    with open('products.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
if __name__ == "__main__":
    mock_html_path = '../mock_sites/amazon_product1.html'  # Adjust the path if needed
    scraped_products = scrape_amazon(mock_html_path)
    save_to_json(scraped_products)
