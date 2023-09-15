import tkinter as tk
import re
import chardet
import json
import os
import subprocess
import codecs

index = 0

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("200x400")
        self.master.resizable(True, True)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        self.text = tk.Label(self, text="Hello", font=("Helvetica", 24))
        self.text.pack(pady=50)
        self.eng_button = tk.Button(self, text="Eng", command=self.load_eng)
        self.eng_button.pack(fill=tk.X, pady=10)
        self.jp_button = tk.Button(self, text="Jp", command=self.load_jp)
        self.jp_button.pack(fill=tk.X, pady=10)
        self.ch_button = tk.Button(self, text="Cn", command=self.load_cn)
        self.ch_button.pack(fill=tk.X, pady=10)
        self.ch_button = tk.Button(self, text="Tw", command=self.load_TW)
        self.ch_button.pack(fill=tk.X, pady=10)
        



    def load_eng(self):
        global index
        index = 0
        self.load_lang()

    def load_jp(self):
        global index
        index = 1
        self.load_lang()
     
    def load_cn(self):
        global index
        index = 2
        self.load_lang()
     
    def load_TW(self):
        global index
        index = 3
        self.load_lang()
     
        
    def load_lang(self):
        with open("input.txt", "r", encoding="utf-8") as file:
            data = file.read()
        # Удаляем строку "0 TermData mTerms"
        data = data.replace("0 TermData mTerms\n", "")
        # Удаляем символ новой строки после символа "]"
        data = data.replace("]\n", "]")
        # Удаляем 7 пробелов подряд
        data = data.replace("       ", "")
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(data)
        with open("input.txt", "r", encoding="utf-8") as file:
            data = file.read()
        # Удаляем строку "0 TermData mTerms"
        data = data.replace("0 TermData mTerms\n", "")
        # Удаляем символ новой строки после символа "]"
        data = data.replace("]\n", "]")
        # Удаляем 7 пробелов подряд
        data = data.replace("       ", "")
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(data)
        input_file = 'output.txt'
        output_file = 'output2.txt'
        term_regex = re.compile(r'Term = "(.+?)"')
        language_regex = re.compile(rf'\[{index}\]1 string Languages = "((?:<.*?>|\s|[^"]*(?:"[^"]*"[^"]*)*[^"]*)+)"')
        terms = {}
        with open(input_file, 'r', encoding='utf-8') as f_input:
            for line in f_input:
                term_match = term_regex.search(line)
                if term_match:
                    term_name = term_match.group(1)
                    terms[term_name] = None
                else:
                    language_match = language_regex.search(line)
                    if language_match:
                        english_translation = language_match.group(1)
                        if term_name and not terms[term_name]:
                            terms[term_name] = english_translation
        with open(output_file, 'w', encoding='utf-8') as f_output:
            for term in sorted(terms.keys()):
                english_translation = terms[term]
                if english_translation:
                    f_output.write(f'    "{term}": "{english_translation}",\n')
        with open('output2.txt', 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()
        with open('output2.txt', 'w', encoding='utf-8') as output_file:
            for line in lines:
                start_index = 0
                while True:
                    start_index = line.find('<', start_index)
                    if start_index == -1:
                        break
                    end_index = line.find('>', start_index)
                    if end_index == -1:
                        break
                    content = line[start_index:end_index+1]
                    content = content.replace('"', r'\"')
                    line = line[:start_index] + content + line[end_index+1:]
                    start_index = end_index
                output_file.write(line)







        def process_line(line, last_line=False):
            
            parts = line.split(': "', 1)
            if len(parts) == 2:
                key = parts[0]
                value = parts[1].rsplit('",', 1)[0]
                
                # Игнорируем обработку, если в значении встречается \"
                if '\\"' in value:
                    return line
                
                # Обработка значения, как и ранее
                value = value.replace('"', '\\"')
                return f'{key}: "{value}",' if not last_line else f'{key}: "{value}"'
            
            return line

        input_filename = 'output2.txt'
        output_filename = 'output2.txt'

        with open(input_filename, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

        # Добавляем { в начало и } на новую строку в конце
        processed_lines = ['{'] + [process_line(line) for line in lines] + ['}']

        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(processed_lines))




        def fix_json_file(input_file, output_file):
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    try:
                        json_data = json.loads(content)
                    except json.JSONDecodeError:
                        content = '{' + content + '}'
                        json_data = json.loads(content)
                    
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        json.dump(json_data, out_f, indent=4, ensure_ascii=False)

                    print("Файл успешно исправлен и сохранен.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")



        # Пример вызова функции
        fix_json_file('output2.txt', 'output2.txt')

        def fix_json2_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if lines:
                joined_lines = ''.join(lines)
                # Ищем последнюю запятую перед фигурной скобкой и удаляем её
                updated_content = joined_lines.rsplit(',', 1)[0] + '\n}'

                # Удаление пустых строк
                updated_content = '\n'.join([line for line in updated_content.split('\n') if line.strip()])

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

        # Пример использования
        fix_json2_file('output2.txt')

            
        # Остальшой код остается неизменным
        with open('output2.txt', encoding='utf-8') as f1, open('old.txt', encoding='utf-8') as f2:
            file1_data = json.load(f1)
            file2_data = json.load(f2)
        for key in file1_data:
            if key in file2_data:
                file1_data[key] = file2_data[key]
            else:
                file1_data[key] = file1_data[key] + " ^"
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(file1_data, f, ensure_ascii=False, indent=2)
        os.remove("output.txt")
        filename = 'data.json'
        subprocess.Popen(['notepad.exe', filename])
        old_name = 'output2.txt'
        new_name = 'orig.txt'
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(old_name, new_name)


root = tk.Tk()
root.title("EasyTranslateCraftopia")
app = Application(master=root)
app.mainloop()
