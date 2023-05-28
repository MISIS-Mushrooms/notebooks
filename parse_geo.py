from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm.auto import tqdm
import pandas as pd
import csv
import folium


groups = pd.read_csv("groups.csv")

groups['Url'] = ['https://www.google.com/maps/search/' + i for i in groups['адрес площадки']]

Url_With_Coordinates = []

option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
option.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome("C:\\chromedriver.exe", options=option)

for url in tqdm(set(groups.Url), leave=False):
    driver.get(url)
    result = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop=image]').get_attribute('content')
    with open('geocoord.txt', 'a') as f:
        f.write(f'{url} -> {result}\n')


driver.close()

with open('Url_With_Coordinates.csv', 'w') as file:
    wr = csv.writer(file)
    wr.writerow(Url_With_Coordinates)