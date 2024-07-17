import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib
import streamlit as st


URL = 'https://www.jumia.co.ke/'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
response = requests.get(URL)
#r = requests.get('https://www.jumia.co.ke/phones-tablets/')

soup = BeautifulSoup(response.content, 'html.parser')

#soup1

#soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

#soup2

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


#productlist = soup2.find_all('div', class_='itm')

#productlist

#for item in productlist:
    #for link in item.find_all('a', href=True):
        #productlinks.append(URL + link['href'])
#print(len(productlinks))

#for category in categories:
    #page = 1
    #while True:
        #category_url = URL + category + f"?page={page}#catalog-listing"
        #r = requests.get(category_url)
        #soup = BeautifulSoup(content, 'html.parser')
        #productlist = soup.find_all('div', class_='itm')
        #if not productlist:
            #break
        #for item in productlist:
            #link = item.find('a', href=True)
            #if link:
                #productlinks.append(URL + link['href'])
        #page += 1

#print(len(productlinks))
#print(productlinks)

#testlink = 'https://www.jumia.co.ke//fashion-womens-casual-flat-loafer-walking-shoes-platform-brogue-shoes-for-girls-women-177745929.html'
#r = requests.get(testlink, headers=headers)
#soup = BeautifulSoup(r.content, 'html.parser')

#product_name = soup.find('h3', class_='name').text.strip()
#print(product_name)

import time
def scrape_all_products(categories, timeout_seconds=300):
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
    # Scraping all products from specified categories with a 10-second timeout
    all_products = scrape_all_products(categories, timeout_seconds=300)

    # Saving scraped data to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('jumia_discount_products2.csv', index=False)

    print("Scraping and CSV export complete.")
    print(df.head())  # Print the first few rows of the DataFrame to verify

except Exception as e:
    print(f"An error occurred: {e}")

df

df.isnull().sum()

df['Name'].dtypes

df['Price'].dtypes

st.title("Jumia Discount Products")
st.dataframe(df)

df['Discount'] = df['Discount'].astype(str)

df['Discount'] = df['Discount'].str.replace('No discount', '0').str.replace('%', '').astype(int)

st.title("Jumia Discount Products")
st.dataframe(df)

discount_filter = st.slider('Discount Percentage', 0, 100, 50)
filtered_df = df[df['Discount'] >= discount_filter]

st.dataframe(filtered_df)





