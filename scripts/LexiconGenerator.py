import csv
import os

# Paths
csv_path = "./data/strongs.csv"
csv_path = os.path.join(os.path.dirname(__file__), '..', csv_path)
csv_path = os.path.abspath(csv_path)

output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Lexicon'))

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Read the CSV and process
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        number = row.get('number', '').strip()
        if not number:
            continue  # Skip entries without number

        # Format markdown content
        content = f"""# Lexicon Entry {number}

**Lemma**: {row.get('lemma', '').strip()}

**Transliteration (xlit)**: {row.get('xlit', '').strip()}

**Pronunciation**: {row.get('pronounce', '').strip()}

**Description**:
{row.get('description', '').strip()}
"""

        # Write markdown file
        file_path = os.path.join(output_folder, f"{number}.md")
        with open(file_path, 'w', encoding='utf-8') as mdfile:
            mdfile.write(content)

print(f"✅ Markdown files created in the '{output_folder}' folder.")
