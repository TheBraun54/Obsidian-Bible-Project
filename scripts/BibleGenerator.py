import os
import csv
from collections import defaultdict

# === CONFIG ===

# Paths for different translations
translations_paths = {
    "NET": "./Data/English/net.csv",                 # NET (2005) translation
    "WEB": "./Data/English/web.csv",                 # WEB (2000/2002) translation
    "KJV": "./Data/English/kjv.csv",                 # KJV (1611) translation
    #"ASV": "./Data/English/asv.csv",                # ASV (1901) translation
    #"BISHOPS": "./Data/English/bishops.csv",        # BISHOPS (1568) translation
    "GENEVA": "./Data/English/geneva.csv",           # GENEVA (1560) translation
    #"COVERDALE": "./Data/English/coverdale.csv",    # COVERDALE (1535) translation
    #"TYNDALE": "./Data/English/tyndale.csv",        # TYNDALE (1525-1536) translation
    "TR": "./Data/Greek/tr.csv",                     # TEXTUS RECEPTUS translation (GREEK NEW TESTAMENT)
}

# Absolute paths for translations
translations_paths = {
    key: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', path))
    for key, path in translations_paths.items()
}

output_folder = "../Bible"

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

# Dictionary of a dicationary defining number of chapters and verses per file
books_chapters_verses = {
    "Genesis": {1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32, 11: 32, 12: 20, 13: 18, 14: 24, 15: 21, 16: 16, 17: 27, 18: 33, 19: 38, 20: 18, 21: 34, 22: 24, 23: 20, 24: 67, 25: 34, 26: 35, 27: 46, 28: 22, 29: 35, 30: 43, 31: 55, 32: 32, 33: 20, 34: 31, 35: 29, 36: 43, 37: 36, 38: 30, 39: 23, 40: 23, 41: 57, 42: 38, 43: 34, 44: 34, 45: 28, 46: 34, 47: 31, 48: 22, 49: 33, 50: 26},
    "Exodus": {1: 22, 2: 25, 3: 22, 4: 31, 5: 23, 6: 30, 7: 25, 8: 32, 9: 35, 10: 29, 11: 10, 12: 51, 13: 22, 14: 31, 15: 27, 16: 36, 17: 16, 18: 27, 19: 25, 20: 26, 21: 36, 22: 31, 23: 9, 24: 18, 25: 40, 26: 37, 27: 21, 28: 43, 29: 46, 30: 38, 31: 18, 32: 35, 33: 23, 34: 35, 35: 35, 36: 38, 37: 29, 38: 31, 39: 43, 40: 38},
    "Leviticus": {1: 17, 2: 16, 3: 17, 4: 35, 5: 19, 6: 30, 7: 38, 8: 36, 9: 24, 10: 20, 11: 47, 12: 8, 13: 59, 14: 57, 15: 33, 16: 34, 17: 16, 18: 30, 19: 37, 20: 27, 21: 24, 22: 33, 23: 44, 24: 23, 25: 55, 26: 46, 27: 34},
    "Numbers": {1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36, 11: 35, 12: 16, 13: 33, 14: 45, 15: 41, 16: 50, 17: 13, 18: 32, 19: 22, 20: 29, 21: 35, 22: 41, 23: 30, 24: 25, 25: 18, 26: 65, 27: 23, 28: 31, 29: 40, 30: 16, 31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13},
    "Deuteronomy": {1: 46, 2: 37, 3: 29, 4: 49, 5: 33, 6: 25, 7: 26, 8: 20, 9: 29, 10: 22, 11: 32, 12: 32, 13: 19, 14: 29, 15: 23, 16: 22, 17: 20, 18: 22, 19: 21, 20: 20, 21: 23, 22: 30, 23: 25, 24: 22, 25: 19, 26: 19, 27: 26, 28: 68, 29: 29, 30: 20, 31: 30, 32: 52, 33: 29, 34: 12},
    "Joshua": {1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35, 9: 27, 10: 43, 11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10, 17: 18, 18: 28, 19: 51, 20: 9, 21: 45, 22: 34, 23: 16, 24: 33},
    "Judges": {1: 36, 2: 23, 3: 31, 4: 24, 5: 31, 6: 40, 7: 25, 8: 35, 9: 57, 10: 18, 11: 40, 12: 15, 13: 25, 14: 20, 15: 20, 16: 31, 17: 13, 18: 31, 19: 30, 20: 48, 21: 25},
    "Ruth": {1: 22, 2: 23, 3: 18, 4: 22},
    "1 Samuel": {1: 28, 2: 36, 3: 21, 4: 22, 5: 12, 6: 21, 7: 17, 8: 22, 9: 27, 10: 27, 11: 15, 12: 25, 13: 23, 14: 52, 15: 35, 16: 23, 17: 58, 18: 30, 19: 24, 20: 42, 21: 16, 22: 23, 23: 29, 24: 23, 25: 44, 26: 25, 27: 12, 28: 25, 29: 11, 30: 31, 31: 13},
    "2 Samuel": {1: 27, 2: 32, 3: 39, 4: 12, 5: 25, 6: 23, 7: 29, 8: 18, 9: 13, 10: 19, 11: 27, 12: 31, 13: 39, 14: 33, 15: 37, 16: 23, 17: 29, 18: 33, 19: 43, 20: 26, 21: 22, 22: 51, 23: 39, 24: 25},
    "1 Kings": {1: 53, 2: 46, 3: 28, 4: 34, 5: 18, 6: 38, 7: 51, 8: 66, 9: 28, 10: 29, 11: 43, 12: 33, 13: 34, 14: 31, 15: 34, 16: 34, 17: 24, 18: 46, 19: 21, 20: 43, 21: 29, 22: 54},
    "2 Kings": {1: 18, 2: 25, 3: 27, 4: 44, 5: 27, 6: 33, 7: 20, 8: 29, 9: 37, 10: 36, 11: 21, 12: 21, 13: 25, 14: 29, 15: 38, 16: 20, 17: 41, 18: 37, 19: 37, 20: 21, 21: 26, 22: 53, 23: 37, 24: 20, 25: 30},
    "1 Chronicles": {1: 54, 2: 55, 3: 24, 4: 43, 5: 26, 6: 81, 7: 40, 8: 40, 9: 44, 10: 14, 11: 47, 12: 40, 13: 14, 14: 17, 15: 29, 16: 43, 17: 27, 18: 17, 19: 19, 20: 8, 21: 30, 22: 19, 23: 32, 24: 31, 25: 31, 26: 32, 27: 34, 28: 21, 29: 30},
    "2 Chronicles": {1: 17, 2: 18, 3: 17, 4: 22, 5: 14, 6: 42, 7: 22, 8: 18, 9: 31, 10: 19, 11: 23, 12: 16, 13: 23, 14: 15, 15: 19, 16: 14, 17: 19, 18: 34, 19: 11, 20: 37, 21: 20, 22: 12, 23: 21, 24: 27, 25: 28, 26: 23, 27: 9, 28: 27, 29: 36, 30: 27, 31: 21, 32: 33, 33: 25, 34: 33, 35: 27, 36: 23},
    "Ezra": {1: 11, 2: 70, 3: 13, 4: 24, 5: 17, 6: 22, 7: 28, 8: 36, 9: 15, 10: 44},
    "Nehemiah": {1: 11, 2: 20, 3: 32, 4: 23, 5: 19, 6: 19, 7: 73, 8: 18, 9: 38, 10: 39, 11: 36, 12: 47, 13: 31},
    "Esther": {1: 22, 2: 23, 3: 15, 4: 17, 5: 14, 6: 14, 7: 10, 8: 17, 9: 32, 10: 3},
    "Job": {1: 22, 2: 13, 3: 26, 4: 21, 5: 27, 6: 30, 7: 22, 8: 22, 9: 35, 10: 22, 11: 20, 12: 25, 13: 28, 14: 22, 15: 35, 16: 22, 17: 16, 18: 22, 19: 29, 20: 29, 21: 34, 22: 30, 23: 17, 24: 25, 25: 6, 26: 14, 27: 23, 28: 28, 29: 25, 30: 31, 31: 40, 32: 22, 33: 33, 34: 37, 35: 16, 36: 33, 37: 24, 38: 41, 39: 30, 40: 24, 41: 34, 42: 17},
    "Psalms": {1: 6, 2: 12, 3: 9, 4: 8, 5: 12, 6: 10, 7: 17, 8: 9, 9: 20, 10: 18, 11: 7, 12: 8, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9, 21: 13, 22: 31, 23: 6, 24: 10, 25: 22, 26: 12, 27: 14, 28: 9, 29: 11, 30: 12, 31: 24, 32: 11, 33: 22, 34: 23, 35: 28, 36: 12, 37: 40, 38: 22, 39: 13, 40: 18, 41: 14, 42: 11, 43: 5, 44: 26, 45: 17, 46: 11, 47: 9, 48: 15, 49: 20, 50: 23, 51: 19, 52: 9, 53: 6, 54: 7, 55: 23, 56: 13, 57: 11, 58: 11, 59: 17, 60: 12, 61: 8, 62: 12, 63: 11, 64: 10, 65: 13, 66: 20, 67: 7, 68: 35, 69: 36, 70: 5, 71: 24, 72: 20, 73: 28, 74: 23, 75: 10, 76: 12, 77: 20, 78: 72, 79: 13, 80: 19, 81: 16, 82: 8, 83: 18, 84: 12, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17, 91: 16, 92: 15, 93: 5, 94: 23, 95: 11, 96: 13, 97: 12, 98: 9, 99: 9, 100: 5, 101: 8, 102: 28, 103: 22, 104: 35, 105: 45, 106: 48, 107: 43, 108: 13, 109: 31, 110: 7, 111: 10, 112: 10, 113: 9, 114: 8, 115: 18, 116: 19, 117: 2, 118: 29, 119: 176, 120: 7, 121: 8, 122: 9, 123: 4, 124: 8, 125: 5, 126: 6, 127: 5, 128: 6, 129: 8, 130: 8, 131: 3, 132: 18, 133: 3, 134: 3, 135: 21, 136: 26, 137: 9, 138: 8, 139: 24, 140: 13, 141: 10, 142: 7, 143: 12, 144: 15, 145: 21, 146: 10, 147: 20, 148: 14, 149: 9, 150: 6},
    "Proverbs": {1: 33, 2: 22, 3: 35, 4: 27, 5: 23, 6: 35, 7: 27, 8: 36, 9: 18, 10: 32, 11: 31, 12: 28, 13: 25, 14: 35, 15: 33, 16: 33, 17: 28, 18: 24, 19: 29, 20: 30, 21: 31, 22: 29, 23: 35, 24: 34, 25: 28, 26: 28, 27: 27, 28: 28, 29: 27, 30: 33, 31: 31},
    "Ecclesiastes": {1: 18, 2: 26, 3: 22, 4: 16, 5: 20, 6: 12, 7: 29, 8: 17, 9: 18, 10: 20, 11: 10, 12: 14},
    "Song of Solomon": {1: 17, 2: 17, 3: 11, 4: 16, 5: 16, 6: 13, 7: 13, 8: 14},
    "Isaiah": {1: 31, 2: 22, 3: 26, 4: 6, 5: 30, 6: 13, 7: 25, 8: 22, 9: 21, 10: 34, 11: 16, 12: 6, 13: 22, 14: 32, 15: 9, 16: 14, 17: 14, 18: 7, 19: 25, 20: 6, 21: 17, 22: 25, 23: 18, 24: 23, 25: 12, 26: 21, 27: 13, 28: 29, 29: 24, 30: 33, 31: 9, 32: 20, 33: 24, 34: 17, 35: 10, 36: 22, 37: 38, 38: 22, 39: 8, 40: 31, 41: 29, 42: 25, 43: 28, 44: 28, 45: 25, 46: 13, 47: 15, 48: 22, 49: 26, 50: 11, 51: 23, 52: 15, 53: 12, 54: 17, 55: 13, 56: 12, 57: 21, 58: 14, 59: 21, 60: 22, 61: 11, 62: 12, 63: 19, 64: 12, 65: 25, 66: 24, 67: 14, 68: 22, 69: 38, 70: 9, 71: 24, 72: 20, 73: 28, 74: 23, 75: 7, 76: 12, 77: 20, 78: 72, 79: 13, 80: 19, 81: 16, 82: 8, 83: 18, 84: 12, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17, 91: 16, 92: 15, 93: 5, 94: 23, 95: 11, 96: 13, 97: 12, 98: 9, 99: 9, 100: 5, 101: 8, 102: 28, 103: 22, 104: 35, 105: 45, 106: 48, 107: 43, 108: 13, 109: 31, 110: 7, 111: 10, 112: 10, 113: 9, 114: 8, 115: 18, 116: 19, 117: 2, 118: 29, 119: 176, 120: 7, 121: 8, 122: 9, 123: 4, 124: 8, 125: 5, 126: 6, 127: 5, 128: 6, 129: 8, 130: 8, 131: 3, 132: 18, 133: 3, 134: 3, 135: 21, 136: 26, 137: 9, 138: 8, 139: 24, 140: 13, 141: 10, 142: 7, 143: 12, 144: 15, 145: 21, 146: 10, 147: 20, 148: 14, 149: 9, 150: 6},
    "Jeremiah": {1: 19, 2: 37, 3: 25, 4: 31, 5: 31, 6: 30, 7: 34, 8: 22, 9: 26, 10: 25, 11: 23, 12: 17, 13: 27, 14: 22, 15: 21, 16: 21, 17: 27, 18: 23, 19: 15, 20: 18, 21: 14, 22: 30, 23: 40, 24: 10, 25: 38, 26: 24, 27: 22, 28: 17, 29: 32, 30: 24, 31: 40, 32: 44, 33: 26, 34: 22, 35: 19, 36: 32, 37: 21, 38: 28, 39: 18, 40: 16, 41: 18, 42: 22, 43: 13, 44: 30, 45: 5, 46: 28, 47: 7, 48: 47, 49: 39, 50: 46, 51: 64, 52: 34},
    "Lamentations": {1: 22, 2: 22, 3: 66, 4: 22, 5: 22},
    "Ezekiel": {1: 28, 2: 10, 3: 27, 4: 17, 5: 17, 6: 14, 7: 27, 8: 18, 9: 11, 10: 22, 11: 25, 12: 28, 13: 23, 14: 23, 15: 8, 16: 63, 17: 24, 18: 32, 19: 14, 20: 49, 21: 32, 22: 31, 23: 49, 24: 27, 25: 17, 26: 21, 27: 36, 28: 26, 29: 21, 30: 26, 31: 18, 32: 32, 33: 33, 34: 31, 35: 15, 36: 38, 37: 28, 38: 23, 39: 29, 40: 49, 41: 26, 42: 20, 43: 27, 44: 31, 45: 25, 46: 24, 47: 23, 48: 35},
    "Daniel": {1: 21, 2: 49, 3: 30, 4: 37, 5: 31, 6: 28, 7: 28, 8: 27, 9: 27, 10: 21, 11: 45, 12: 13},
    "Hosea": {1: 11, 2: 23, 3: 5, 4: 19, 5: 15, 6: 11, 7: 16, 8: 14, 9: 17, 10: 15, 11: 12, 12: 14, 13: 16, 14: 9},
    "Joel": {1: 20, 2: 32, 3: 21},
    "Amos": {1: 15, 2: 16, 3: 15, 4: 13, 5: 27, 6: 14, 7: 17, 8: 14, 9: 15},
    "Obadiah": {1: 21},
    "Jonah": {1: 17, 2: 10, 3: 10, 4: 11},
    "Micah": {1: 16, 2: 13, 3: 12, 4: 13, 5: 15, 6: 16, 7: 20},
    "Nahum": {1: 15, 2: 13, 3: 19},
    "Habakkuk": {1: 17, 2: 20, 3: 19},
    "Zephaniah": {1: 18, 2: 15, 3: 20},
    "Haggai": {1: 15, 2: 23},
    "Zechariah": {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21},
    "Malachi": {1: 14, 2: 17, 3: 18, 4: 6},
    "Matthew": {1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29, 8: 34, 9: 38, 10: 42, 11: 30, 12: 50, 13: 58, 14: 36, 15: 39, 16: 28, 17: 27, 18: 35, 19: 30, 20: 34, 21: 46, 22: 46, 23: 39, 24: 51, 25: 46, 26: 75, 27: 66, 28: 20},
    "Mark": {1: 45, 2: 28, 3: 35, 4: 41, 5: 43, 6: 56, 7: 37, 8: 38, 9: 50, 10: 52, 11: 33, 12: 44, 13: 37, 14: 72, 15: 47, 16: 20},
    "Luke": {1: 80, 2: 52, 3: 38, 4: 44, 5: 39, 6: 49, 7: 50, 8: 56, 9: 62, 10: 42, 11: 54, 12: 59, 13: 35, 14: 35, 15: 32, 16: 31, 17: 37, 18: 43, 19: 48, 20: 47, 21: 38, 22: 71, 23: 56, 24: 53},
    "John": {1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59, 9: 41, 10: 42, 11: 57, 12: 50, 13: 38, 14: 31, 15: 27, 16: 33, 17: 26, 18: 40, 19: 42, 20: 31, 21: 25},
    "Acts": {1: 26, 2: 47, 3: 26, 4: 37, 5: 42, 6: 15, 7: 60, 8: 40, 9: 43, 10: 48, 11: 30, 12: 25, 13: 52, 14: 28, 15: 41, 16: 40, 17: 34, 18: 28, 19: 41, 20: 38, 21: 40, 22: 30, 23: 35, 24: 27, 25: 12, 26: 32, 27: 44, 28: 31},
    "Romans": {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39, 9: 33, 10: 21, 11: 36, 12: 21, 13: 14, 14: 23, 15: 33, 16: 27},
    "1 Corinthians": {1: 31, 2: 16, 3: 23, 4: 21, 5: 13, 6: 20, 7: 40, 8: 13, 9: 27, 10: 33, 11: 34, 12: 31, 13: 13, 14: 40, 15: 58, 16: 24},
    "2 Corinthians": {1: 24, 2: 17, 3: 18, 4: 18, 5: 21, 6: 18, 7: 16, 8: 24, 9: 15, 10: 18, 11: 33, 12: 21, 13: 14},
    "Galatians": {1: 24, 2: 21, 3: 29, 4: 31, 5: 26, 6: 18},
    "Ephesians": {1: 23, 2: 22, 3: 21, 4: 32, 5: 33, 6: 24},
    "Philippians": {1: 30, 2: 30, 3: 21, 4: 23},
    "Colossians": {1: 29, 2: 23, 3: 25, 4: 18},
    "1 Thessalonians": {1: 10, 2: 20, 3: 13, 4: 18, 5: 28},
    "2 Thessalonians": {1: 12, 2: 17, 3: 18},
    "1 Timothy": {1: 20, 2: 15, 3: 16, 4: 16, 5: 25, 6: 21},
    "2 Timothy": {1: 18, 2: 26, 3: 17, 4: 22},
    "Titus": {1: 16, 2: 15, 3: 15},
    "Philemon": {1: 25},
    "Hebrews": {1: 14, 2: 18, 3: 19, 4: 16, 5: 14, 6: 20, 7: 28, 8: 13, 9: 28, 10: 39, 11: 40, 12: 29, 13: 25},
    "James": {1: 27, 2: 26, 3: 18, 4: 17, 5: 20},
    "1 Peter": {1: 25, 2: 25, 3: 22, 4: 19, 5: 14},
    "2 Peter": {1: 21, 2: 22, 3: 18},
    "1 John": {1: 10, 2: 29, 3: 24, 4: 21, 5: 21},
    "2 John": {1: 13},
    "3 John": {1: 14},
    "Jude": {1: 25},
    "Revelation": {1: 20, 2: 29, 3: 22, 4: 11, 5: 14, 6: 17, 7: 17, 8: 13, 9: 21, 10: 11, 11: 19, 12: 17, 13: 18, 14: 20, 15: 8, 16: 21, 17: 18, 18: 24, 19: 21, 20: 15, 21: 27, 22: 21}
}


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# Dictionary to store verses by book, chapter, and verse
chapters = defaultdict(lambda: defaultdict(list))

# Read from all translation files
translations = {key: defaultdict(dict) for key in translations_paths}

# Function to clean the "¶ " character from the verse text
def clean_text(text):
    return text.replace("¶ ", "")

for translation, path in translations_paths.items():
    with open(path, newline='', encoding='utf-8') as file:
        for _ in range(5):  # Skip first 5 lines before the header
            next(file)
        reader = csv.DictReader(file)
        for row in reader:
            book = row['Book Name']
            chapter = int(row['Chapter'])
            verse = int(row['Verse'])
            text = row['Text'].strip()

            # Clean the text to remove "¶ " character
            cleaned_text = clean_text(text)

            # Store the translation text by book, chapter, and verse
            translations[translation][(book, chapter, verse)] = cleaned_text

            # Populate chapters with translation texts for all translations
            chapters[(book, chapter)][translation].append(f"{verse}: {cleaned_text}")

# Now create individual verse files and chapter files, where each translation is listed under its header
for translation, path in translations_paths.items():
    print(translation)
    for (book, chapter, verse), text in translations[translation].items():

        # Build the verse file path
        book_code = BOOK_CODES.get(book)
        verse_id = f"{book_code}{str(chapter).zfill(2)}{str(verse).zfill(2)}"
        book_num = str(list(BOOK_CODES.keys()).index(book) + 1).zfill(2)  # Create book number
        book_folder = f"{book_num} - {book}"
        chapter_folder = f"{book} {chapter}"
        verse_file = f"{book} {chapter}.{verse}.md"
        tag = "NT" if book in NT_BOOKS else "OT"

        book_chap_vers = f"{book} {chapter}:{verse}"

        folder_path = os.path.join(output_folder, book_folder, chapter_folder)
        ensure_dir(folder_path)

        verse_path = os.path.join(folder_path, verse_file)
        with open(verse_path, 'w', encoding='utf-8') as vf:
            vf.write(f'---\n')
            vf.write(f'book: "{book}"\n')
            vf.write(f'chapter: "{chapter}"\n')
            vf.write(f'verse: "{verse}"\n')
            vf.write(f'reference: "{book} {chapter}:{verse}"\n')
            vf.write(f'testament: "{tag}"\n')
            vf.write(f'verse_id: "{verse_id}"\n')
            vf.write(f'tags: ["bible/verse"]\n')
            vf.write(f'topics: []\n')
            vf.write(f'themes: []\n')
            vf.write(f'elaborated: false\n')
            vf.write(f'carded: false\n')
            vf.write(f'memorized: false\n')
            vf.write(f'---\n\n')

            vf.write(f"# {book_chap_vers}\n\n")

            # Write out the texts for all translations (no year in verse files)
            for trans in translations.keys():
                trans_name = trans.split()[0]  # Remove year from the translation name
                lower_trans_name = trans_name.lower()
                if lower_trans_name == "tr" and tag == "OT":
                    continue
                vf.write(f"###### {trans_name}\n")
                vf.write(f"{book_chap_vers}\n")
                vf.write(translations[trans].get((book, chapter, verse), "") + "\n\n")

            vf.write("---\n")
            vf.write("# Notes\n\n")

# Adds navigation to the chapter files
def chapter_navigation(book, chapter, cf, is_top):
    # Retrieve the total chapters dictionary for the given book
    total_chapters = books_chapters_verses.get(book)
    
    if not total_chapters:
        cf.write(f"Book {book} not found.\n")
        return

    # Get the last chapter number (the highest key in the dictionary)
    last_chapter = max(total_chapters.keys())

    # Add navigation to previous chapter, ensuring it is within bounds
    if chapter > 1:
        prev_chapter = chapter - 1
        cf.write(f"[[{book} {prev_chapter}|<-]] ")
    
    # Current chapter navigation link
    cf.write(f" ✞ ")
    
    # Add navigation to next chapter, ensuring it is within bounds
    if is_top:
        if chapter < last_chapter:
            next_chapter = chapter + 1
            cf.write(f"[[{book} {next_chapter}|->]]\n\n")
        else:
            # Check if this is the last chapter of the current book
            next_book_index = list(BOOK_CODES.keys()).index(book) + 1  # Get the next book's index
            if next_book_index < len(BOOK_CODES):
                next_book = list(BOOK_CODES.keys())[next_book_index]  # Get the next book's name
                cf.write(f"[[{next_book} 1|Next Book ->]]\n\n")
            else:
                cf.write(f"\n\n")  # End of the Bible, no next book
    else:
        if chapter < last_chapter:
            next_chapter = chapter + 1
            cf.write(f"[[{book} {next_chapter}|->]]\n\n")
        else:
            # Check if this is the last chapter of the current book
            next_book_index = list(BOOK_CODES.keys()).index(book) + 1  # Get the next book's index
            if next_book_index < len(BOOK_CODES):
                next_book = list(BOOK_CODES.keys())[next_book_index]  # Get the next book's name
                cf.write(f"[[{next_book} 1|Next Book ->]]")

# Now create chapter files, where each translation is listed under its header (with the year)
for (book, chapter), translations_in_chapter in chapters.items():
    book_code = BOOK_CODES.get(book)
    book_num = str(list(BOOK_CODES.keys()).index(book) + 1).zfill(2)  # Create book number
    book_folder = f"{book_num} - {book}"
    chapter_folder = f"{book} {chapter}"
    chapter_file = f"{book} {chapter}.md"

    tag = "NT" if book in NT_BOOKS else "OT"

    verse_count = books_chapters_verses[book][chapter]

    folder_path = os.path.join(output_folder, book_folder, chapter_folder)
    ensure_dir(folder_path)

    chapter_path = os.path.join(folder_path, chapter_file)

    # Create chapter file with translations for each chapter
    with open(chapter_path, 'w', encoding='utf-8') as cf:
        cf.write("---\n")
        cf.write(f"book: {book}\n")
        cf.write(f"chapter: {chapter}\n")
        cf.write(f"reference: {book} {chapter}\n")
        cf.write(f"testament: {tag}\n")
        cf.write(f"verse_count: {verse_count}\n")
        cf.write(f"tags: [bible/chapter]\n")
        cf.write(f"people: []\n")
        cf.write(f"locations: [] \n")
        cf.write(f"topics: []\n")
        cf.write(f"themes: []\n")
        cf.write(f"elaborated: false\n")
        cf.write("---\n\n")

        # chapter_navigation(book, chapter, cf, True)

        cf.write(f"# {book} {chapter}\n\n")

        # Write out each translation under its header, including the year in chapter files
        for translation, verses in translations_in_chapter.items():
            # Skip the TR translation if the book number is less than 40
            if translation == "TR" and (list(BOOK_CODES.keys()).index(book) + 1) < 40:
                continue  # Skip if TR translation and book number < 40

            cf.write(f"## {translation}\n")
            for verse_text in verses:
                cf.write(f"{verse_text}\n\n")

        cf.write(f"---\n")
        cf.write(f"# Notes\n\n\n\n")
        
        # chapter_navigation(book, chapter, cf, False)
