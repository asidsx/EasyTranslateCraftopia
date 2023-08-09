# Открываем файлы для чтения и записи
with open('data.json', 'r', encoding='utf-8') as data_file, \
     open('old.txt', 'r', encoding='utf-8') as old_file, \
     open('error.txt', 'w', encoding='utf-8') as error_file:
    
    # Читаем все строки из data.txt в список
    data_lines = data_file.readlines()
    # Читаем строки из old.txt в список
    old_lines = old_file.readlines()
    # Удаляем переводы строк из каждой строки
    old_lines = [line.strip() for line in old_lines]

    # Создаем пустой список для строк, которые не найдены в old.txt
    not_found = []

    # Ищем каждую строку в old.txt и удаляем ее из data_lines, если она найдена
    for line in data_lines:
        if line.strip() in old_lines:
            continue
        not_found.append(line)

    # Записываем строки, которые не найдены в old.txt, в error.txt
    error_file.writelines(not_found)

    # Перезаписываем data.txt с оставшимися строками
    data_file.seek(0)
    data_file.truncate()
    data_file.writelines(not_found)
