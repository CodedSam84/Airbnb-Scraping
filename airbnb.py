# -*- coding: utf-8 -*-
"""
"""

import requests
from bs4 import BeautifulSoup

import pandas as pd

url ="https://www.airbnb.com/s/Malm%C3%B6--Sweden/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Malm%C3%B6%2C%20Sweden&place_id=ChIJ_5HEdKUFU0YR5YhIvd8FqdM&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"

payload = {'api_key': '637931fd146a1e19c817d61d', 'url': url, 'dynamic':'false'}
page = requests.get(url).text

soup = BeautifulSoup(page, "lxml")

df = pd.DataFrame({"title":[], "price":[], "description":[], "rating":[], "link":[]})


while True:
    domain = "https://www.airbnb.com/"
    next_page_path = soup.find("a", {"aria-label":"Next"}).get("href")
    next_page_url = domain + next_page_path
    
    cards = soup.find_all("div", class_="cy5jw6o dir dir-ltr")

    for card in cards:
        try:
            link = card.find("a", class_="ln2bl2p dir dir-ltr").get("href")
            link_url = domain + link
            title = card.find("div", class_="t1jojoys dir dir-ltr").text
            price = card.find("span", class_="a8jt5op dir dir-ltr").text
            description = card.find("span", class_="t6mzqp7 dir dir-ltr").text
            rating = card.find("span", class_="r1dxllyb dir dir-ltr").text
               
            new_df = pd.Series({"title":title, "price":price, "description":description, "rating":rating, "link":link_url})
            convert_to_frame = new_df.to_frame().T
            final_df = pd.concat([df, convert_to_frame], ignore_index=True)
            df = final_df
        except:
            pass
        
    page = requests.get(next_page_url).text
    soup = BeautifulSoup(page, "lxml")
    
df.to_csv("C:/Users/swuma/scrapping/airbnb.xlsx")