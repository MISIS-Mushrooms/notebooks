import json
with open("translations.json", 'r') as f:
    d = json.load(f)

print(d)