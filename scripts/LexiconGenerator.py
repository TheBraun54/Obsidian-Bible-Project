import os
import csv

# === CONFIG ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# CSV file is assumed to be in ../data/strongs.csv relative to this script
csv_path = os.path.join(script_dir, '..', 'data', 'strongs.csv')
csv_path = os.path.abspath(csv_path)

# Output to ../Lexicon/Greek and ../Lexicon/Hebrew
base_output_folder = os.path.join(script_dir, '..', 'Lexicon')
base_output_folder = os.path.abspath(base_output_folder)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

print(f"Reading CSV from: {csv_path}")
print(f"Base output folder: {base_output_folder}")

# Read the CSV and process
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        number = row.get('number', '').strip()
        if not number:
            continue

        # Detect folder based on prefix
        if number.startswith('H'):
            subfolder = 'Hebrew'
        elif number.startswith('G'):
            subfolder = 'Greek'
        else:
            subfolder = 'Other'

        output_folder = os.path.join(base_output_folder, subfolder)
        ensure_dir(output_folder)

        # File content
        content = f"""# Lexicon Entry {number}

**Lemma**: {row.get('lemma', '').strip()}

**Transliteration (xlit)**: {row.get('xlit', '').strip()}

**Pronunciation**: {row.get('pronounce', '').strip()}

**Description**:
{row.get('description', '').strip()}
"""

        # File path
        file_path = os.path.join(output_folder, f"{number}.md")

        # Write file
        with open(file_path, 'w', encoding='utf-8') as mdfile:
            mdfile.write(content)

        # Debug print
        print(f"✅ Wrote: {file_path}")

print("✅ All done.")
