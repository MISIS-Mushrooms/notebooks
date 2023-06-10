import shutil
import pandas as pd
from tqdm import tqdm
import json
from PIL import Image

pref = '/home/digitaljay/projects/lct2023'

groups = pd.read_csv('groups.csv')
with open('translations.json', 'r') as f:
    translations = json.load(f)

for level in tqdm(set(groups['направление 3'])):
    level_by_front = level.replace('/', '_')
    level_in_dict = level.replace('ОНЛАЙН ', '').strip()
    translation = translations[level_in_dict]
    saved = 0
    for num in range(0, 50):
        try:
            img_src = f'{pref}/imgs/{translation}/{num}.png'
            img_dst = f'{pref}/hobby_images/{level_by_front}.png'
            with Image.open(img_src) as im:
                width, height = im.size
            if height/width > 1.2:
                shutil.copyfile(img_src, img_dst)
                saved = 1
                break
        except Exception as e:
            print(level_by_front)
            print(e)
    if not saved:
        for num in range(0, 50):
            try:
                img_src = f'{pref}/imgs/{translation}/{num}.png'
                img_dst = f'{pref}/hobby_images/{level_by_front}.png'
                with Image.open(img_src) as im:
                    width, height = im.size
                if height / width > 1:
                    shutil.copyfile(img_src, img_dst)
                    saved = 1
                    break
            except Exception as e:
                print(level_by_front)
                print(e)
    if not saved:
        img_src = f'{pref}/imgs/{translation}/0.png'
        img_dst = f'{pref}/hobby_images/{level_by_front}.png'
        shutil.copyfile(img_src, img_dst)
