# -*- coding: utf-8 -*-
"""PythonWS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EHe2PtJ4H8tgL0xhqbi1GK_4Ol7R5Gvw
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#function to extract product title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'B_NuCI'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

#function to extract price
def get_price(soup):

    try:
        price = soup.find("div", attrs={"class":"_30jeq3 _16Jk6d"}).string.strip()

    except AttributeError:
      price = ""

        #try:
            # If there is some deal price
            #price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        #except:

    return price

#function to extract 
def get_rating(soup):

    try:
        rating = soup.find("div", attrs={"class":"_3LWZlK"}).string.strip()
    
    except AttributeError:
      rating = ""
        #try:
            #rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        #except:
            #rating = ""	

    return rating

if __name__ == '__main__':

    # add your user agent 
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.findAll("a",attrs="_1fQZEK")

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
      

    
    flipkart_df = pd.DataFrame.from_dict(d)
    flipkart_df['title'].replace('', np.nan, inplace=True)
    flipkart_df = amazon_df.dropna(subset=['title'])
    flipkart_df.to_csv("flipkart_data.csv", header=True, index=False)