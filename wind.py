import tkinter as tk
import re
import json
import os
import subprocess

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
        self.tw_button = tk.Button(self, text="Tw", command=self.load_tw)
        self.tw_button.pack(fill=tk.X, pady=10)

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

    def load_tw(self):
        global index
        index = 3
        self.load_lang()

    def load_lang(self):
        with open("input.txt", "r", encoding="utf-8") as file:
            data = file.read()
        data = data.replace("0 TermData mTerms\n", "")
        data = data.replace("]\n", "]")
        data = data.replace("       ", "")
        
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(data)
        
        input_file = 'output.txt'
        output_file = 'output2.txt'
        term_regex = re.compile(r'1 string Term = "(.+?)"')
        language_regex = re.compile(rf'\[{index}\]\s*1 string data = "(.*)"')

        terms = {}
        current_term = None
        
        with open(input_file, 'r', encoding='utf-8') as f_input:
            for line in f_input:
                term_match = term_regex.search(line)
                if term_match:
                    current_term = term_match.group(1)
                    terms[current_term] = None
                else:
                    language_match = language_regex.search(line)
                    if language_match and current_term:
                        translation = language_match.group(1)
                        translation = translation.replace('"', r'\"')
                        terms[current_term] = translation

        with open(output_file, 'w', encoding='utf-8') as f_output:
            for term, translation in sorted(terms.items()):
                if translation:
                    f_output.write(f'    "{term}": "{translation}",\n')

        def fix_json_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if len(lines) > 0:
                if lines[0][0] != '{':
                    lines.insert(0, '{\n')
                if lines[-1][-2:] == ',\n':
                    lines[-1] = lines[-1][:-2] + '\n'
                elif lines[-1][-1] == '\n':
                    lines[-1] = lines[-1][:-1]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                if lines[-1][-1] != '}':
                    f.write('}\n')

        fix_json_file('output2.txt')

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
