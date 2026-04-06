# EasyTranslateCraftopia
![GitHub all releases](https://img.shields.io/github/downloads/asidsx/EasyTranslateCraftopia/total)

<p align="center">

<img width="502" height="782" alt="image" src="https://github.com/user-attachments/assets/4899e737-c35c-4773-b6a0-c9a41fcbf370" />

</p>

---

## ⚡ Глобальное обновление / Global Update / 大規模アップデート (PyQt6)

## Russian:
Программа была полностью переписана на **PyQt6**! 
Теперь у неё есть полноценный графический интерфейс. Вам больше не нужно переименовывать файлы и класть их строго в одну папку — теперь любой файл можно выбрать через диалоговое окно «Открыть».
**Новые функции:**
- Интерфейс программы автоматически переводится на язык вашей системы (RU, EN, DE, FR, ES, IT, KO).
- **Режим первого запуска**: простое создание чистой базы (`orig.txt`) из нового дампа.
- **Умное отслеживание изменений**: программа автоматически находит новые и измененные разработчиками строки и выносит их в отдельный файл `changes.json` для удобного перевода.
- **Интеграция перевода**: отдельный модуль внизу программы позволяет в 1 клик перенести переведенные строки в основной файл `data.json`.

*(P.S. Напоминание с прошлого обновления: используйте только новую версию UABEAvalonia V7 для извлечения текста).*

## English:
The program has been completely rewritten in **PyQt6**!
It now has a full-fledged graphical interface. You no longer need to rename files or put them strictly in one folder — you can select any file via the "Open" dialog.
**New features:**
- The program interface automatically translates to your system language (RU, EN, DE, FR, ES, IT, KO).
- **First Run Mode**: Easily create a clean base (`orig.txt`) from a new dump.
- **Smart Change Tracking**: The program automatically finds strings that were added or modified by the developers and places them in a separate `changes.json` file for easy translation.
- **Translation Integration**: A dedicated module at the bottom of the program allows you to merge translated strings into your main `data.json` file with 1 click.

*(P.S. Reminder from the last update: use only the new version of UABEAvalonia V7 to extract text).*

## Japanese:
プログラムは **PyQt6** で完全に書き直されました！
本格的なGUI（グラフィカルインターフェース）を搭載し、ファイル名の変更や同じフォルダーへの配置が不要になりました。「開く」ダイアログから任意のファイルを選択できます。
**新機能:**
- プログラムのインターフェースは、システムの言語（RU、EN、DE、FR、ES、IT、KO）に自動的に翻訳されます。
- **初回起動モード**: 新しいダンプからクリーンなベース（`orig.txt`）を簡単に作成します。
- **スマートな変更追跡**: 開発者によって追加または変更された文字列を自動的に見つけ、翻訳しやすいように別の `changes.json` ファイルに抽出します。
- **翻訳の統合**: プログラム下部の専用モジュールを使用すると、ワンクリックで翻訳された文字列をメインの `data.json` ファイルにマージできます。

*(追記: 前回のアップデートからの注意事項ですが、テキストの抽出には必ず新しいバージョンの UABEAvalonia V7 を使用してください)。*

---

## 🇷🇺 Инструкция по использованию

**Ссылка на проект по переводу:** <a href="https://github.com/BudgieY/AdditionalLanguagesForCraftopia">AdditionalLanguagesForCraftopia</a>

1. Используйте программу <a href="https://github.com/nesrak1/UABEA/releases/tag/v7">UABEAvalonia</a> (версия V7) для создания текстового дамп-файла `I2Languages`. (Назовем его `input.txt`).
2. **Шаг 1: Если вы переводите с нуля (или нужна новая база):**
   - Запустите `wind.exe`.
   - В первом поле выберите ваш свежий `input.txt`.
   - Поставьте галочку **«Режим первого запуска»** и нажмите кнопку нужного языка (Eng, Jp и т.д.).
   - Программа извлечет текст и создаст файл `orig.txt`. Обязательно сохраните его для будущих обновлений!
3. **Шаг 2: Если вышло обновление игры (Сравнение и слияние):**
   - Уберите галочку первого запуска.
   - Выберите новый `input.txt`.
   - Выберите `old.txt` (ваш старый готовый перевод).
   - Выберите старый `orig.txt` (оригинальный текст до обновления игры).
   - Нажмите кнопку языка. Программа создаст 2 файла:
     - `data.json` — объединенный файл (где старые строки переведены, а новые остаются на языке оригинала).
     - `changes.json` — файл, содержащий **только** новые или измененные разработчиками строки.
4. **Шаг 3: Интеграция перевода:**
   - Откройте `changes.json`, переведите нужные строки и сохраните файл.
   - В нижнем блоке программы («Интеграция перевода») выберите ваш основной `data.json` в поле «Куда вставлять?».
   - Выберите ваш переведенный `changes.json` в поле «Что вставлять?».
   - Нажмите **«Интегрировать перевод»**. Программа сама найдет нужные строки и заменит их на переведенные!

---

## 🇬🇧 Instructions

**Project Translation Link:** <a href="https://github.com/BudgieY/AdditionalLanguagesForCraftopia">AdditionalLanguagesForCraftopia</a>

1. Use the <a href="https://github.com/nesrak1/UABEA/releases/tag/v7">UABEAvalonia</a> program (V7 release) to create a text dump file of `I2Languages`. (Let's call it `input.txt`).
2. **Step 1: If you are starting from scratch (or need a new base):**
   - Run `wind.exe`.
   - In the first field, select your fresh `input.txt`.
   - Check the **"First run mode"** box and click the language button you want to extract (Eng, Jp, etc.).
   - The program will extract the text and create an `orig.txt` file. Keep this file safe for future updates!
3. **Step 2: When a game update is released (Compare & Merge):**
   - Uncheck the "First run mode" box.
   - Select the new `input.txt`.
   - Select `old.txt` (your previous completed translation).
   - Select the old `orig.txt` (the original text before the game update).
   - Click the language button. The program will generate 2 files:
     - `data.json` — the merged file (where old strings are translated, and new ones are kept in their original language).
     - `changes.json` — a file containing **only** the new strings or strings changed by the developers.
4. **Step 3: Translation Integration:**
   - Open `changes.json`, translate the strings, and save the file.
   - In the bottom block of the program ("Translation Integration"), select your main `data.json` in the "Where to insert?" field.
   - Select your translated `changes.json` in the "What to insert?" field.
   - Click **"Integrate translation"**. The program will automatically find the corresponding keys and replace them with your translation!

---

## 🇯🇵 使い方（日本語）

**プロジェクト翻訳リンク:** <a href="https://github.com/BudgieY/AdditionalLanguagesForCraftopia">AdditionalLanguagesForCraftopia</a>

1. <a href="https://github.com/nesrak1/UABEA/releases/tag/v7">UABEAvalonia</a> プログラム（V7リリース）を使用して、`I2Languages` のテキストダンプファイルを作成します。（ここでは `input.txt` と呼びます）。
2. **ステップ 1: ゼロから始める場合（または新しいベースが必要な場合）:**
   - `wind.exe` を実行します。
   - 最初のフィールドで、新しい `input.txt` を選択します。
   - **「初回起動モード (First run mode)」** のチェックボックスをオンにし、抽出したい言語のボタン（Eng、Jp など）をクリックします。
   - プログラムがテキストを抽出し、`orig.txt` ファイルを作成します。このファイルは今後のアップデートのために大切に保管してください！
3. **ステップ 2: ゲームのアップデートがリリースされた場合（比較とマージ）:**
   - 「初回起動モード」のチェックを外します。
   - 新しい `input.txt` を選択します。
   - `old.txt`（以前の完成した翻訳ファイル）を選択します。
   - 古い `orig.txt`（アップデート前の元のテキスト）を選択します。
   - 言語ボタンをクリックします。プログラムは以下の2つのファイルを作成します：
     - `data.json` — 統合されたファイル（古い文字列は翻訳され、新しい文字列は元の言語のままになります）。
     - `changes.json` — 開発者によって追加・変更された **新しい文字列のみ** を含むファイル。
4. **ステップ 3: 翻訳の統合:**
   - `changes.json` を開き、文字列を翻訳して、保存します。
   - プログラムの下部（「翻訳の統合」ブロック）で、「どこに挿入しますか？ (Where to insert?)」にメインの `data.json` を選択します。
   - 「何を挿入しますか？ (What to insert?)」に翻訳済みの `changes.json` を選択します。
   - **「翻訳を統合する (Integrate translation)」** をクリックします。プログラムが自動的に該当するキーを見つけ、翻訳済みのテキストに置き換えます！
