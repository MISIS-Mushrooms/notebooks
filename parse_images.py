import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
from googletrans import Translator
import pandas as pd
from tqdm import tqdm
import json


class UnsplashParser():
    def __init__(self):
        self.translator = Translator()
        self.parsed = {}

    def retried_response(self, url):
        response = requests.get(url)
        while response.status_code != 200:
            print(response.status_code)
            time.sleep(20)
            response = requests.get(url)
        return response

    def translate_query(self, search_for: str):
        if search_for == 'ОФП':
            return "Sport"
        translation = self.translator.translate(search_for).text
        for_url = [i if i.isalpha() else ' ' for i in translation]
        for_url = ''.join(for_url).strip()
        return for_url.replace(' ', '-')

    def get_picture_links(self, search_for: str):
        url = f'https://unsplash.com/s/photos/{search_for}?orientation=portrait'
        print(url)
        response = self.retried_response(url)
        soup = BeautifulSoup(response.text, "html.parser")
        pictures_soups = soup.findAll('div', class_='MorZF')[:50]
        pictures_links = [pic_soup.find('img')['src'] for pic_soup in pictures_soups]
        return pictures_links

    def download_picture(self, picture_url: str, picture_name: str = 'test'):
        response = self.retried_response(picture_url)
        img = Image.open(BytesIO(response.content))
        img.save(f"imgs/{picture_name}")

    def mkdir(self, search_for):
        import os
        try:
            os.mkdir(f'imgs/{search_for}')
            return 1
        except OSError:
            return 0

    def parse(self, rus_query: str):
        search_for = self.translate_query(rus_query)
        self.parsed[rus_query] = search_for
        with open('translations.json', 'w') as f:
            json.dump(self.parsed, f)
        print(search_for)
        if self.mkdir(search_for):
            pictures_links = self.get_picture_links(search_for)
            for i, link in enumerate(pictures_links):
                self.download_picture(link, f'{search_for}/{i}.png')


parser = UnsplashParser()
groups = pd.read_csv('groups.csv')

for level in tqdm(set(groups['направление 3'])):
    level = level.replace('ОНЛАЙН ', '').strip()
    if level not in parser.parsed:
        parser.parse(level)
