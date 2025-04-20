import os
import csv
import re
from collections import defaultdict

# === CONFIG ===
csv_path = "./data/kjv_strongs.csv"
csv_path = os.path.join(os.path.dirname(__file__), '..', csv_path)
csv_path = os.path.abspath(csv_path)

output_folder = "../Bibles/King-James-Version-Strong"
translation = "King James Version (KJV)"

# New Testament books (for tagging)
NT_BOOKS = {
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John",
    "3 John", "Jude", "Revelation"
}

# Book codes for verse_id
BOOK_CODES = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT", "1 Samuel": "1SA", "2 Samuel": "2SA",
    "1 Kings": "1KI", "2 Kings": "2KI", "1 Chronicles": "1CH", "2 Chronicles": "2CH",
    "Ezra": "EZR", "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA",
    "Proverbs": "PRO", "Ecclesiastes": "ECC", "Song of Solomon": "SNG", "Isaiah": "ISA",
    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN", "Hosea": "HOS",
    "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON", "Micah": "MIC",
    "Nahum": "NAM", "Habakkuk": "HAB", "Zephaniah": "ZEP", "Haggai": "HAG", "Zechariah": "ZEC",
    "Malachi": "MAL", "Matthew": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT",
    "Romans": "ROM", "1 Corinthians": "1CO", "2 Corinthians": "2CO", "Galatians": "GAL",
    "Ephesians": "EPH", "Philippians": "PHP", "Colossians": "COL", "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH", "1 Timothy": "1TI", "2 Timothy": "2TI", "Titus": "TIT",
    "Philemon": "PHM", "Hebrews": "HEB", "James": "JAS", "1 Peter": "1PE", "2 Peter": "2PE",
    "1 John": "1JN", "2 John": "2JN", "3 John": "3JN", "Jude": "JUD", "Revelation": "REV"
}

# Extract Strong's Numbers using regex (looking for text inside [[]])
def extract_strongs(text):
    # Regex to match any Strong's numbers within [[ ]]
    return re.findall(r'\[\[(.*?)\]\]', text)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

chapters = defaultdict(list)

with open(csv_path, newline='', encoding='utf-8') as file:
    for _ in range(5):  # Skip first 5 lines before the header
        next(file)
    reader = csv.DictReader(file)
    for row in reader:
        book = row['Book Name']
        book_num = row['Book Number'].zfill(2)
        chapter = int(row['Chapter'])
        verse = int(row['Verse'])
        text = row['Text'].strip()

        # Extract Strong's Numbers from the verse text
        strongs = extract_strongs(text)  # This will be a list of Strong's numbers
        strongs_tag = ', '.join(strongs) if strongs else '[]'  # If there are no Strong's numbers, it will be empty

        tag = "bible/nt" if book in NT_BOOKS else "bible/ot"

        book_code = BOOK_CODES.get(book)
        verse_id = f"{book_code}{str(chapter).zfill(2)}{str(verse).zfill(2)}"

        book_folder = f"{book_num} - {book}"
        chapter_folder = f"{book} {chapter}"
        verse_file = f"{book} {chapter}.{verse}.md"
        chapter_file = f"{book} {chapter}.md"

        folder_path = os.path.join(output_folder, book_folder, chapter_folder)
        ensure_dir(folder_path)

        # Create verse file
        verse_path = os.path.join(folder_path, verse_file)
        with open(verse_path, 'w', encoding='utf-8') as vf:
            vf.write(f"---\n")
            vf.write(f"book: {book}\n")
            vf.write(f"chapter: {chapter}\n")
            vf.write(f"verse: {verse}\n")
            vf.write(f"reference: {book} {chapter}:{verse}\n")
            vf.write(f"verse_id: {verse_id}\n")
            vf.write(f"translation: {translation}\n")
            vf.write(f"tags: [bible/verse/{tag}]\n")
            vf.write(f"strongs: [{strongs_tag}]\n")  # Include Strong's numbers if available
            vf.write(f"topics: []\n")
            vf.write(f"themes: []\n")
            vf.write(f"people: []\n")
            vf.write(f"places: []\n")
            vf.write(f"notes: >\n  \n")
            vf.write(f"---\n\n")
            vf.write(text + "\n")

        chapters[(book, chapter, book_num)].append((verse, f"![[{book} {chapter}.{verse}]]"))

# Create chapter files (same as your existing logic)
for (book, chapter, book_num), verse_embeds in chapters.items():
    chapter_folder = f"{book} {chapter}"
    chapter_file = f"{book} {chapter}.md"
    book_folder = f"{book_num} - {book}"
    chapter_path = os.path.join(output_folder, book_folder, chapter_folder, chapter_file)

    chapter_number = int(chapter)
    prev_chapter = chapter_number - 1
    next_chapter = chapter_number + 1
    tag = "bible/nt" if book in NT_BOOKS else "bible/ot"

    with open(chapter_path, 'w', encoding='utf-8') as cf:
        cf.write("---\n")
        cf.write(f"book: {book}\n")
        cf.write(f"chapter: {chapter}\n")
        cf.write(f"reference: {book} {chapter}\n")
        cf.write(f"translation: {translation}\n")
        cf.write(f"tags: [bible/chapter/{tag}]\n")
        cf.write(f"topics: []\n")
        cf.write(f"themes: []\n")
        cf.write(f"people: []\n")
        cf.write(f"places: []\n")
        cf.write(f"notes: >\n  \n")
        cf.write("---\n\n")

        if prev_chapter > 0:
            cf.write(f"[[{book} {prev_chapter}|<-]] ")
        cf.write("✞ ")
        cf.write(f"[[{book} {next_chapter}|->]]\n\n")

        cf.write(f"# {book} {chapter}\n\n")
        for _, embed in sorted(verse_embeds):
            cf.write(embed + "\n\n")

        if prev_chapter > 0:
            cf.write(f"[[{book} {prev_chapter}|<-]] ")
        cf.write("✞ ")
        cf.write(f"[[{book} {next_chapter}|->]]\n")

print(f"✅ Markdown files created in the '{output_folder}' folder.")