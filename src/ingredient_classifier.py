# src/ingredient_classifier.py
import pandas as pd
import re
from difflib import get_close_matches

# load CSV once
df = pd.read_csv("data/ingredient_list.csv")
veg_list = df[df['category'] == 'veg']['ingredient'].astype(str).tolist()
nonveg_list = df[df['category'] == 'nonveg']['ingredient'].astype(str).tolist()

# make regex-safe and sort by length (longest first) to match multi-word items first
def make_word_regex(word):
    return r'\b' + re.escape(word.lower()) + r'\b'

veg_regexes = [re.compile(make_word_regex(w)) for w in sorted(veg_list, key=len, reverse=True)]
nonveg_regexes = [re.compile(make_word_regex(w)) for w in sorted(nonveg_list, key=len, reverse=True)]

def find_matches(text):
    text_l = text.lower()
    found_veg = []
    found_nonveg = []

    # exact / whole-word matches first
    for w, rx in zip(veg_list, veg_regexes):
        if rx.search(text_l):
            found_veg.append(w)
    for w, rx in zip(nonveg_list, nonveg_regexes):
        if rx.search(text_l):
            found_nonveg.append(w)

    # if nothing found, try fuzzy guesses for small OCR typos
    if not (found_veg or found_nonveg):
        words = re.findall(r"[a-zA-Z]+(?: [a-zA-Z]+)?", text_l)
        # try small fuzzy matches to nonveg list first (safer)
        for w in words:
            close = get_close_matches(w, nonveg_list, n=1, cutoff=0.8)
            if close:
                found_nonveg.append(close[0])
            else:
                close2 = get_close_matches(w, veg_list, n=1, cutoff=0.85)
                if close2:
                    found_veg.append(close2[0])

    return list(sorted(set(found_veg))), list(sorted(set(found_nonveg)))

def classify_ingredients(text):
    veg_found, nonveg_found = find_matches(text)
    # simple decision rules
    if nonveg_found:
        label = "❌ Non-Vegetarian"
        reasons = nonveg_found
    elif veg_found:
        label = "✅ Vegetarian"
        reasons = veg_found
    else:
        label = "⚠️ Unclear"
        reasons = []
    # confidence: number of matches
    confidence = len(nonveg_found) + len(veg_found)
    return label, reasons, confidence
