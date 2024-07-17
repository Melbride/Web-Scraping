import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import streamlit as st

URL = 'https://www.jumia.co.ke/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

categories = [
    "/mlp-jumia-official-stores/",
    "/phones-tablets/",
    "/electronics/",
    "/home-office-appliances/",
    "/health-beauty/",
    "/home-office/",
    "/category-fashion-by-jumia/",
    "/computing/",
    "/groceries/",
    "/baby-products/",
    "/sporting-goods/",
    "/automobile/",
    "/video-games/",
    "/patio-lawn-garden/",
    "/books-movies-music/",
    "/industrial-scientific/",
    "/toys-games/"
]

def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('article', class_='prd _fb col c-prd')
    product_list = []

    for product in products:
        name = product.find('h3', class_='name').text.strip()
        price = product.find('div', class_='prc').text.strip()
        discount = product.find('div', class_='bdg _dsct _sm')
        discount_text = discount.text.strip() if discount else 'No discount'

        product_list.append({
            'Name': name,
            'Price': price,
            'Discount': discount_text
        })
    
    return product_list

def scrape_all_products(categories, timeout_seconds=60):
    start_time = time.time()
    all_products = []

    for category in categories:
        page = 1
        while True:
            category_url = URL + category + f"?page={page}#catalog-listing"
            print(f"Scraping {category_url}")
            products = scrape_page(category_url)
            if not products:
                break
            all_products.extend(products)
            page += 1
            
            # Check elapsed time and stop after timeout_seconds
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout_seconds:
                print(f"Timeout of {timeout_seconds} seconds reached. Stopping.")
                return all_products

            # Displaying the DataFrame to show ongoing updates
            df = pd.DataFrame(all_products)
            print(f"DataFrame updated with {len(all_products)} products")
            print(df.head())

            time.sleep(1)  # Delay to control the output frequency

    return all_products

try:
    # Scraping all products from specified categories with a timeout
    all_products = scrape_all_products(categories, timeout_seconds=60)

    # Saving scraped data to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('jumia_discount_products2.csv', index=False)

    print("Scraping and CSV export complete.")
    # Print the first few rows of the DataFrame to verify
    print(df.head())

except Exception as e:
    print(f"An error occurred: {e}")

# Streamlit app code---view the products under localhost using streamlit
def main():
    st.title("Jumia Discount Products")
    
    # Reading the DataFrame
    df = pd.read_csv('jumia_discount_products2.csv')

    # Handling 'No discount' and convert Discount column to integers
    df['Discount'] = df['Discount'].astype(str)
    df['Discount'] = df['Discount'].str.replace('No discount', '0').str.replace('%', '').astype(int)
    
    st.dataframe(df)
    
    discount_filter = st.slider('Discount Percentage', 0, 100, 50)
    filtered_df = df[df['Discount'] >= discount_filter]
    
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
