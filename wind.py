import sys
import os
import re
import json
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox, 
                             QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QFont

# ==========================================================
# СЛОВАРЬ ПЕРЕВОДОВ ИНТЕРФЕЙСА (ЛОКАЛИЗАЦИЯ)
# ==========================================================
TRANSLATIONS = {
    'ru': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Парсинг и создание базы",
        'ph_input': "Выберите новый input.txt...",
        'btn_open': "Открыть",
        'ph_old': "Выберите old.txt (ваш перевод)...",
        'ph_old_orig': "Выберите старый orig.txt (для сравнения)...",
        'cb_first_run': "Режим первого запуска (Создать ТОЛЬКО чистый orig.txt)",
        'title_integration': "Интеграция перевода",
        'ph_target': "Куда вставлять? (выберите data.json)...",
        'ph_trans': "Что вставлять? (файл с переводами)...",
        'btn_integrate': "Интегрировать перевод в файл",
        'err_title': "Ошибка",
        'succ_title': "Успех",
        'err_json_title': "Ошибка JSON",
        'err_json_syntax_title': "Синтаксическая ошибка JSON",
        'err_save_title': "Ошибка сохранения",
        'msg_err_input': "Пожалуйста, выберите новый входной файл (input).",
        'msg_err_three_files': "Пожалуйста, выберите все три файла (input, old и старый orig) перед запуском или включите 'Режим первого запуска'.",
        'msg_succ_orig': "Чистый файл orig.txt успешно создан!",
        'msg_err_invalid_json': "Один из файлов имеет неверный формат JSON:\n{0}",
        'msg_err_two_files_int': "Пожалуйста, выберите оба файла (целевой data.json и файл с переводами).",
        'msg_err_corrupted_json': "Один из файлов повреждён или не является правильным JSON.\nПроверьте, не забыли ли вы запятые или кавычки.\nДетали: {0}",
        'msg_err_read': "Не удалось прочитать файлы:\n{0}",
        'msg_succ_integrate': "Интеграция завершена!\n\nОбновлено / добавлено строк: {0}",
        'msg_err_save': "Не удалось сохранить файл:\n{0}",
        'fd_input': "Выберите входной файл (input.txt)",
        'fd_old': "Выберите файл старого перевода (old.txt)",
        'fd_old_orig': "Выберите старый orig.txt",
        'fd_target': "Выберите целевой файл (например, data.json)",
        'fd_trans': "Выберите файл с переводами"
    },
    'en': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Parsing and database creation",
        'ph_input': "Select new input.txt...",
        'btn_open': "Open",
        'ph_old': "Select old.txt (your translation)...",
        'ph_old_orig': "Select old orig.txt (for comparison)...",
        'cb_first_run': "First run mode (Create ONLY clean orig.txt)",
        'title_integration': "Translation Integration",
        'ph_target': "Where to insert? (select data.json)...",
        'ph_trans': "What to insert? (translation file)...",
        'btn_integrate': "Integrate translation into file",
        'err_title': "Error",
        'succ_title': "Success",
        'err_json_title': "JSON Error",
        'err_json_syntax_title': "JSON Syntax Error",
        'err_save_title': "Save Error",
        'msg_err_input': "Please select a new input file (input).",
        'msg_err_three_files': "Please select all three files (input, old, and old orig) before running, or enable 'First run mode'.",
        'msg_succ_orig': "Clean orig.txt file created successfully!",
        'msg_err_invalid_json': "One of the files has an invalid JSON format:\n{0}",
        'msg_err_two_files_int': "Please select both files (target data.json and translation file).",
        'msg_err_corrupted_json': "One of the files is corrupted or not valid JSON.\nCheck for missing commas or quotes.\nDetails: {0}",
        'msg_err_read': "Failed to read files:\n{0}",
        'msg_succ_integrate': "Integration completed!\n\nUpdated / added lines: {0}",
        'msg_err_save': "Failed to save file:\n{0}",
        'fd_input': "Select input file (input.txt)",
        'fd_old': "Select old translation file (old.txt)",
        'fd_old_orig': "Select old orig.txt",
        'fd_target': "Select target file (e.g., data.json)",
        'fd_trans': "Select translations file"
    },
    'de': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Parsing und Datenbankerstellung",
        'ph_input': "Wählen Sie eine neue input.txt...",
        'btn_open': "Öffnen",
        'ph_old': "Wählen Sie old.txt (Ihre Übersetzung)...",
        'ph_old_orig': "Wählen Sie die alte orig.txt (zum Vergleich)...",
        'cb_first_run': "Erster Startmodus (NUR saubere orig.txt erstellen)",
        'title_integration': "Übersetzungsintegration",
        'ph_target': "Wo einfügen? (data.json auswählen)...",
        'ph_trans': "Was einfügen? (Übersetzungsdatei)...",
        'btn_integrate': "Übersetzung in Datei integrieren",
        'err_title': "Fehler",
        'succ_title': "Erfolg",
        'err_json_title': "JSON-Fehler",
        'err_json_syntax_title': "JSON-Syntaxfehler",
        'err_save_title': "Speicherfehler",
        'msg_err_input': "Bitte wählen Sie eine neue Eingabedatei (input).",
        'msg_err_three_files': "Bitte wählen Sie alle drei Dateien aus, bevor Sie fortfahren, oder aktivieren Sie den 'Ersten Startmodus'.",
        'msg_succ_orig': "Saubere orig.txt erfolgreich erstellt!",
        'msg_err_invalid_json': "Eine der Dateien hat ein ungültiges JSON-Format:\n{0}",
        'msg_err_two_files_int': "Bitte wählen Sie beide Dateien aus (Ziel-data.json und Übersetzungsdatei).",
        'msg_err_corrupted_json': "Eine der Dateien ist beschädigt oder kein gültiges JSON.\nDetails: {0}",
        'msg_err_read': "Dateien konnten nicht gelesen werden:\n{0}",
        'msg_succ_integrate': "Integration abgeschlossen!\n\nAktualisierte / hinzugefügte Zeilen: {0}",
        'msg_err_save': "Datei konnte nicht gespeichert werden:\n{0}",
        'fd_input': "Eingabedatei auswählen (input.txt)",
        'fd_old': "Alte Übersetzungsdatei auswählen (old.txt)",
        'fd_old_orig': "Alte orig.txt auswählen",
        'fd_target': "Zieldatei auswählen (z.B. data.json)",
        'fd_trans': "Übersetzungsdatei auswählen"
    },
    'fr': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Analyse et création de base de données",
        'ph_input': "Sélectionnez un nouveau input.txt...",
        'btn_open': "Ouvrir",
        'ph_old': "Sélectionnez old.txt (votre traduction)...",
        'ph_old_orig': "Sélectionnez l'ancien orig.txt (pour comparaison)...",
        'cb_first_run': "Mode premier démarrage (Créer UNIQUEMENT un orig.txt propre)",
        'title_integration': "Intégration de la traduction",
        'ph_target': "Où insérer ? (sélectionnez data.json)...",
        'ph_trans': "Quoi insérer ? (fichier de traduction)...",
        'btn_integrate': "Intégrer la traduction dans le fichier",
        'err_title': "Erreur",
        'succ_title': "Succès",
        'err_json_title': "Erreur JSON",
        'err_json_syntax_title': "Erreur de syntaxe JSON",
        'err_save_title': "Erreur de sauvegarde",
        'msg_err_input': "Veuillez sélectionner un nouveau fichier d'entrée (input).",
        'msg_err_three_files': "Veuillez sélectionner les trois fichiers avant de lancer, ou activer le 'Mode premier démarrage'.",
        'msg_succ_orig': "Fichier orig.txt propre créé avec succès !",
        'msg_err_invalid_json': "L'un des fichiers a un format JSON invalide :\n{0}",
        'msg_err_two_files_int': "Veuillez sélectionner les deux fichiers (data.json cible et fichier de traduction).",
        'msg_err_corrupted_json': "L'un des fichiers est corrompu ou n'est pas un JSON valide.\nDétails : {0}",
        'msg_err_read': "Impossible de lire les fichiers :\n{0}",
        'msg_succ_integrate': "Intégration terminée !\n\nLignes mises à jour / ajoutées : {0}",
        'msg_err_save': "Impossible d'enregistrer le fichier :\n{0}",
        'fd_input': "Sélectionnez le fichier d'entrée (input.txt)",
        'fd_old': "Sélectionnez l'ancien fichier de traduction (old.txt)",
        'fd_old_orig': "Sélectionnez l'ancien orig.txt",
        'fd_target': "Sélectionnez le fichier cible (ex: data.json)",
        'fd_trans': "Sélectionnez le fichier de traduction"
    },
    'es': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Análisis y creación de base de datos",
        'ph_input': "Seleccione un nuevo input.txt...",
        'btn_open': "Abrir",
        'ph_old': "Seleccione old.txt (su traducción)...",
        'ph_old_orig': "Seleccione el orig.txt antiguo (para comparación)...",
        'cb_first_run': "Modo de primer inicio (Crear SOLO orig.txt limpio)",
        'title_integration': "Integración de traducción",
        'ph_target': "¿Dónde insertar? (seleccione data.json)...",
        'ph_trans': "¿Qué insertar? (archivo de traducción)...",
        'btn_integrate': "Integrar traducción en el archivo",
        'err_title': "Error",
        'succ_title': "Éxito",
        'err_json_title': "Error de JSON",
        'err_json_syntax_title': "Error de sintaxis JSON",
        'err_save_title': "Error al guardar",
        'msg_err_input': "Seleccione un nuevo archivo de entrada (input).",
        'msg_err_three_files': "Seleccione los tres archivos antes de ejecutar o active el 'Modo de primer inicio'.",
        'msg_succ_orig': "¡Archivo orig.txt limpio creado con éxito!",
        'msg_err_invalid_json': "Uno de los archivos tiene un formato JSON no válido:\n{0}",
        'msg_err_two_files_int': "Seleccione ambos archivos (data.json de destino y archivo de traducción).",
        'msg_err_corrupted_json': "Uno de los archivos está dañado o no es un JSON válido.\nDetalles: {0}",
        'msg_err_read': "No se pudieron leer los archivos:\n{0}",
        'msg_succ_integrate': "¡Integración completada!\n\nLíneas actualizadas / añadidas: {0}",
        'msg_err_save': "No se pudo guardar el archivo:\n{0}",
        'fd_input': "Seleccione el archivo de entrada (input.txt)",
        'fd_old': "Seleccione el archivo de traducción antiguo (old.txt)",
        'fd_old_orig': "Seleccione el antiguo orig.txt",
        'fd_target': "Seleccione el archivo de destino (ej. data.json)",
        'fd_trans': "Seleccione el archivo de traducciones"
    },
    'it': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "Analisi e creazione database",
        'ph_input': "Seleziona un nuovo input.txt...",
        'btn_open': "Apri",
        'ph_old': "Seleziona old.txt (la tua traduzione)...",
        'ph_old_orig': "Seleziona il vecchio orig.txt (per confronto)...",
        'cb_first_run': "Modalità primo avvio (Crea SOLO orig.txt pulito)",
        'title_integration': "Integrazione della traduzione",
        'ph_target': "Dove inserire? (seleziona data.json)...",
        'ph_trans': "Cosa inserire? (file di traduzione)...",
        'btn_integrate': "Integra la traduzione nel file",
        'err_title': "Errore",
        'succ_title': "Successo",
        'err_json_title': "Errore JSON",
        'err_json_syntax_title': "Errore di sintassi JSON",
        'err_save_title': "Errore di salvataggio",
        'msg_err_input': "Seleziona un nuovo file di input (input).",
        'msg_err_three_files': "Seleziona tutti e tre i file prima di procedere, o attiva la 'Modalità primo avvio'.",
        'msg_succ_orig': "File orig.txt pulito creato con successo!",
        'msg_err_invalid_json': "Uno dei file ha un formato JSON non valido:\n{0}",
        'msg_err_two_files_int': "Seleziona entrambi i file (data.json di destinazione e file di traduzione).",
        'msg_err_corrupted_json': "Uno dei file è danneggiato o non è un JSON valido.\nDettagli: {0}",
        'msg_err_read': "Impossibile leggere i file:\n{0}",
        'msg_succ_integrate': "Integrazione completata!\n\nRighe aggiornate / aggiunte: {0}",
        'msg_err_save': "Impossibile salvare il file:\n{0}",
        'fd_input': "Seleziona file di input (input.txt)",
        'fd_old': "Seleziona il vecchio file di traduzione (old.txt)",
        'fd_old_orig': "Seleziona il vecchio orig.txt",
        'fd_target': "Seleziona file di destinazione (es. data.json)",
        'fd_trans': "Seleziona file di traduzione"
    },
    'ko': {
        'window_title': "EasyTranslateCraftopia",
        'title_parsing': "파싱 및 데이터베이스 생성",
        'ph_input': "새 input.txt 선택...",
        'btn_open': "열기",
        'ph_old': "old.txt 선택 (번역본)...",
        'ph_old_orig': "이전 orig.txt 선택 (비교용)...",
        'cb_first_run': "첫 실행 모드 (깨끗한 orig.txt만 생성)",
        'title_integration': "번역 통합",
        'ph_target': "어디에 삽입하시겠습니까? (data.json 선택)...",
        'ph_trans': "무엇을 삽입하시겠습니까? (번역 파일)...",
        'btn_integrate': "파일에 번역 통합",
        'err_title': "오류",
        'succ_title': "성공",
        'err_json_title': "JSON 오류",
        'err_json_syntax_title': "JSON 구문 오류",
        'err_save_title': "저장 오류",
        'msg_err_input': "새 입력 파일(input)을 선택해주세요.",
        'msg_err_three_files': "시작하기 전에 3개의 파일(input, old, 이전 orig)을 모두 선택하거나 '첫 실행 모드'를 활성화하세요.",
        'msg_succ_orig': "깨끗한 orig.txt 파일이 성공적으로 생성되었습니다!",
        'msg_err_invalid_json': "파일 중 하나의 JSON 형식이 잘못되었습니다:\n{0}",
        'msg_err_two_files_int': "대상 data.json과 번역 파일을 모두 선택해주세요.",
        'msg_err_corrupted_json': "파일 중 하나가 손상되었거나 올바른 JSON이 아닙니다.\n자세한 정보: {0}",
        'msg_err_read': "파일을 읽을 수 없습니다:\n{0}",
        'msg_succ_integrate': "통합 완료!\n\n업데이트 / 추가된 줄: {0}",
        'msg_err_save': "파일을 저장할 수 없습니다:\n{0}",
        'fd_input': "입력 파일 선택 (input.txt)",
        'fd_old': "이전 번역 파일 선택 (old.txt)",
        'fd_old_orig': "이전 orig.txt 선택",
        'fd_target': "대상 파일 선택 (예: data.json)",
        'fd_trans': "번역 파일 선택"
    }
}
# ==========================================================

class Application(QWidget):
    def __init__(self):
        super().__init__()
        
        # Определение языка системы
        # QLocale.system().name() возвращает строку вида "ru_RU", "en_US", "de_DE"
        sys_lang = QLocale.system().name()[:2]
        # Если язык есть в словаре - используем его, если нет - ставим английский ('en')
        self.lang = sys_lang if sys_lang in TRANSLATIONS else 'en'

        if '__file__' in globals():
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.current_dir = os.getcwd()
            
        os.chdir(self.current_dir)
        self.initUI()

    # Метод для получения переведенного текста по ключу
    def t(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    def initUI(self):
        self.setWindowTitle(self.t('window_title'))
        self.resize(500, 750) 

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # ==========================================================
        # БЛОК 1: ПАРСИНГ И ПОИСК ИЗМЕНЕНИЙ
        # ==========================================================
        self.label = QLabel(self.t('title_parsing'))
        self.label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addSpacing(10)

        # --- Выбор основного файла (input.txt) ---
        input_layout = QHBoxLayout()
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText(self.t('ph_input'))
        self.input_entry.setReadOnly(True)
        
        self.input_btn = QPushButton(self.t('btn_open'))
        self.input_btn.clicked.connect(self.browse_input)
        
        input_layout.addWidget(self.input_entry)
        input_layout.addWidget(self.input_btn)
        layout.addLayout(input_layout)

        # --- Выбор файла старого перевода (old.txt) ---
        old_layout = QHBoxLayout()
        self.old_entry = QLineEdit()
        self.old_entry.setPlaceholderText(self.t('ph_old'))
        self.old_entry.setReadOnly(True)
        
        self.old_btn = QPushButton(self.t('btn_open'))
        self.old_btn.clicked.connect(self.browse_old)
        
        old_layout.addWidget(self.old_entry)
        old_layout.addWidget(self.old_btn)
        layout.addLayout(old_layout)

        # --- Выбор старого orig.txt для сравнения изменений ---
        old_orig_layout = QHBoxLayout()
        self.old_orig_entry = QLineEdit()
        self.old_orig_entry.setPlaceholderText(self.t('ph_old_orig'))
        self.old_orig_entry.setReadOnly(True)
        
        self.old_orig_btn = QPushButton(self.t('btn_open'))
        self.old_orig_btn.clicked.connect(self.browse_old_orig)
        
        old_orig_layout.addWidget(self.old_orig_entry)
        old_orig_layout.addWidget(self.old_orig_btn)
        layout.addLayout(old_orig_layout)
        
        layout.addSpacing(10)

        # --- Чекбокс режима создания чистой базы ---
        self.only_orig_cb = QCheckBox(self.t('cb_first_run'))
        self.only_orig_cb.toggled.connect(self.toggle_mode)
        layout.addWidget(self.only_orig_cb)

        layout.addSpacing(10)

        # --- Кнопки языков ---
        lang_layout = QHBoxLayout()
        self.eng_button = QPushButton("Eng")
        self.eng_button.clicked.connect(lambda: self.load_lang(0))
        lang_layout.addWidget(self.eng_button)

        self.jp_button = QPushButton("Jp")
        self.jp_button.clicked.connect(lambda: self.load_lang(1))
        lang_layout.addWidget(self.jp_button)

        self.ch_button = QPushButton("Cn")
        self.ch_button.clicked.connect(lambda: self.load_lang(2))
        lang_layout.addWidget(self.ch_button)

        self.tw_button = QPushButton("Tw")
        self.tw_button.clicked.connect(lambda: self.load_lang(3))
        lang_layout.addWidget(self.tw_button)

        layout.addLayout(lang_layout)
        layout.addSpacing(20)

        # ==========================================================
        # РАЗДЕЛИТЕЛЬНАЯ ЛИНИЯ
        # ==========================================================
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        layout.addSpacing(20)

        # ==========================================================
        # БЛОК 2: ИНТЕГРАЦИЯ ПЕРЕВОДА
        # ==========================================================
        self.label_integrate = QLabel(self.t('title_integration'))
        self.label_integrate.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        self.label_integrate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_integrate)
        layout.addSpacing(10)

        # --- Выбор целевого файла (data.json) ---
        target_layout = QHBoxLayout()
        self.target_entry = QLineEdit()
        self.target_entry.setPlaceholderText(self.t('ph_target'))
        self.target_entry.setReadOnly(True)
        
        self.target_btn = QPushButton(self.t('btn_open'))
        self.target_btn.clicked.connect(self.browse_target)
        
        target_layout.addWidget(self.target_entry)
        target_layout.addWidget(self.target_btn)
        layout.addLayout(target_layout)

        # --- Выбор файла с переведенным куском ---
        trans_layout = QHBoxLayout()
        self.trans_entry = QLineEdit()
        self.trans_entry.setPlaceholderText(self.t('ph_trans'))
        self.trans_entry.setReadOnly(True)
        
        self.trans_btn = QPushButton(self.t('btn_open'))
        self.trans_btn.clicked.connect(self.browse_trans)
        
        trans_layout.addWidget(self.trans_entry)
        trans_layout.addWidget(self.trans_btn)
        layout.addLayout(trans_layout)

        layout.addSpacing(10)

        self.integrate_button = QPushButton(self.t('btn_integrate'))
        self.integrate_button.setMinimumHeight(45)
        self.integrate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px;")
        self.integrate_button.clicked.connect(self.integrate_translation)
        layout.addWidget(self.integrate_button)

        layout.addStretch()
        self.setLayout(layout)

    # ==========================
    # МЕТОДЫ ВЫБОРА ФАЙЛОВ
    # ==========================
    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.t('fd_input'), self.current_dir, "Text Files (*.txt);;All Files (*)")
        if file_path: self.input_entry.setText(file_path)

    def browse_old(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.t('fd_old'), self.current_dir, "Text Files (*.txt);;JSON Files (*.json);;All Files (*)")
        if file_path: self.old_entry.setText(file_path)

    def browse_old_orig(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.t('fd_old_orig'), self.current_dir, "Text Files (*.txt);;JSON Files (*.json);;All Files (*)")
        if file_path: self.old_orig_entry.setText(file_path)

    def browse_target(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.t('fd_target'), self.current_dir, "JSON Files (*.json);;Text Files (*.txt);;All Files (*)")
        if file_path: self.target_entry.setText(file_path)

    def browse_trans(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.t('fd_trans'), self.current_dir, "JSON Files (*.json);;Text Files (*.txt);;All Files (*)")
        if file_path: self.trans_entry.setText(file_path)

    # ==========================
    # ЛОГИКА ПЕРЕКЛЮЧАТЕЛЕЙ
    # ==========================
    def toggle_mode(self, checked):
        self.old_entry.setEnabled(not checked)
        self.old_btn.setEnabled(not checked)
        self.old_orig_entry.setEnabled(not checked)
        self.old_orig_btn.setEnabled(not checked)

    # ==========================
    # ФУНКЦИЯ 1: ПАРСИНГ
    # ==========================
    def load_lang(self, index):
        input_file_path = self.input_entry.text()
        only_orig_mode = self.only_orig_cb.isChecked()

        if not input_file_path:
            QMessageBox.warning(self, self.t('err_title'), self.t('msg_err_input'))
            return

        if not only_orig_mode:
            old_file_path = self.old_entry.text()
            old_orig_file_path = self.old_orig_entry.text()
            if not old_file_path or not old_orig_file_path:
                QMessageBox.warning(self, self.t('err_title'), self.t('msg_err_three_files'))
                return

        with open(input_file_path, "r", encoding="utf-8") as file:
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

        if only_orig_mode:
            if os.path.exists("orig.txt"): os.remove("orig.txt")
            os.rename("output2.txt", "orig.txt")
            if os.path.exists("output.txt"): os.remove("output.txt")
            
            subprocess.Popen(['notepad.exe', 'orig.txt'])
            QMessageBox.information(self, self.t('succ_title'), self.t('msg_succ_orig'))
            return

        try:
            with open('output2.txt', encoding='utf-8') as f1, \
                 open(old_file_path, encoding='utf-8') as f2, \
                 open(old_orig_file_path, encoding='utf-8') as f3:
                
                new_orig_data = json.load(f1)
                old_trans_data = json.load(f2)
                old_orig_data = json.load(f3)

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, self.t('err_json_title'), self.t('msg_err_invalid_json').format(e))
            return
        
        changes_data = {}

        for key, value in new_orig_data.items():
            is_changed_or_new = False
            if key not in old_orig_data:
                is_changed_or_new = True
            elif old_orig_data[key] != value:
                is_changed_or_new = True

            if is_changed_or_new:
                new_orig_data[key] = value
                changes_data[key] = value
            else:
                if key in old_trans_data:
                    new_orig_data[key] = old_trans_data[key]
                else:
                    new_orig_data[key] = value

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(new_orig_data, f, ensure_ascii=False, indent=2)

        with open('changes.json', 'w', encoding='utf-8') as f:
            json.dump(changes_data, f, ensure_ascii=False, indent=2)
        
        os.remove("output.txt")
        old_name = 'output2.txt'
        new_name = 'orig.txt'
        if os.path.exists(new_name): os.remove(new_name)
        os.rename(old_name, new_name)

        subprocess.Popen(['notepad.exe', 'data.json'])
        subprocess.Popen(['notepad.exe', 'changes.json'])

    # ==========================
    # ФУНКЦИЯ 2: ИНТЕГРАЦИЯ 
    # ==========================
    def integrate_translation(self):
        target_path = self.target_entry.text()
        trans_path = self.trans_entry.text()

        if not target_path or not trans_path:
            QMessageBox.warning(self, self.t('err_title'), self.t('msg_err_two_files_int'))
            return

        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
            
            with open(trans_path, 'r', encoding='utf-8') as f:
                trans_data = json.load(f)
                
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, self.t('err_json_syntax_title'), self.t('msg_err_corrupted_json').format(e))
            return
        except Exception as e:
            QMessageBox.critical(self, self.t('err_title'), self.t('msg_err_read').format(e))
            return

        updates_count = 0
        for key, value in trans_data.items():
            if key in target_data:
                target_data[key] = value
                updates_count += 1
            else:
                target_data[key] = value
                updates_count += 1

        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
                
            QMessageBox.information(self, self.t('succ_title'), self.t('msg_succ_integrate').format(updates_count))
            subprocess.Popen(['notepad.exe', target_path])
            
        except Exception as e:
            QMessageBox.critical(self, self.t('err_save_title'), self.t('msg_err_save').format(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
