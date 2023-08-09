import json

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

with open('old.txt', encoding='utf-8') as f:
    old_data = json.load(f)

error_data = []

for key, value in data.items():
    if key in old_data and old_data[key] != value:
        error_data.append({key: value})

with open('compare.txt', 'w', encoding='utf-8') as f:
    json.dump(error_data, f, indent=4, ensure_ascii=False)