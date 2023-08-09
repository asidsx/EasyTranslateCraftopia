import json

def replace_strings(input_file, data_file):
    # Открытие файлов с данными в кодировке UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Замена строк по начальным данным
    for key in input_data:
        for data_key in data:
            if data_key.startswith(key):
                data[data_key] = input_data[key]

    # Запись изменений в файл data.json в кодировке UTF-8
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Пример использования функции
replace_strings('Input.json', 'data.json')