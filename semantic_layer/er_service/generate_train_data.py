import csv
import random
import json
import os
import re
from typing import List, Dict, Tuple
from gliner.data_processing.tokenizer import WhitespaceTokenSplitter

# Paths relative to project root
ENTITIES_CSV = "data/semantic_input/entities/mfi_entities.csv"
POSITIVE_TEMPLATES = "data/semantic_input/entities/example_sentences.txt"
NEGATIVE_SENTENCES = "data/semantic_input/entities/negative_sentences.txt"
OUTPUT_DIR = "data/semantic_input/entities/train"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dataset.json")

LIMIT = 10000
NEGATIVE_RATIO = 0.1 

def load_entities(path: str) -> List[str]:
    entities = []
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return []
    with open(path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if 'NAME' in row:
                name = row['NAME'].strip()
                if name:
                    entities.append(name)
    return list(set(entities))

def load_lines(path: str) -> List[str]:
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return []
    with open(path, mode='r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def get_token_span(tokens_with_offsets: List[Tuple[str, int, int]], char_start: int, char_end: int) -> Tuple[int, int]:
    """Find token indices for a character-level span."""
    start_token_idx = -1
    end_token_idx = -1
    
    for i, (token, s, e) in enumerate(tokens_with_offsets):
        # If the token overlaps with the character span
        if s == char_start:
            start_token_idx = i
        if e == char_end:
            end_token_idx = i
            
    return start_token_idx, end_token_idx

def generate_data():
    entities = load_entities(ENTITIES_CSV)
    pos_templates = load_lines(POSITIVE_TEMPLATES)
    neg_sentences = load_lines(NEGATIVE_SENTENCES)
    
    if not entities or not pos_templates:
        print("Error: No entities or positive templates found.")
        return

    num_neg_available = len(neg_sentences)
    num_pos_possible = len(entities) * len(pos_templates)
    num_pos = min(num_pos_possible, int(num_neg_available * 9), int(LIMIT * 0.9))
    num_neg = int(num_pos / 9)
    
    print(f"Entities: {len(entities)}")
    print(f"Positive templates: {len(pos_templates)}")
    print(f"Negative sentences: {len(neg_sentences)}")
    print(f"Target: {num_pos} pos, {num_neg} neg.")

    splitter = WhitespaceTokenSplitter()
    dataset = []

    # Positive samples
    all_pos_combos = []
    for template in pos_templates:
        for entity in entities:
            all_pos_combos.append((template, entity))
    
    random.shuffle(all_pos_combos)
    selected_pos = all_pos_combos[:num_pos]

    for template, entity in selected_pos:
        # 1. Replace placeholder and keep track of char offsets
        start_char_idx = template.find("{entity}")
        if start_char_idx == -1:
            continue
            
        text = template.replace("{entity}", entity)
        end_char_idx = start_char_idx + len(entity)
        
        # 2. Tokenize the full text
        tokens_with_offsets = list(splitter(text))
        token_list = [t[0] for t in tokens_with_offsets]
        
        # 3. Find token span
        # Note: If entity name is multiple words, it might be split into multiple tokens.
        # We need to find the start token index and end token index.
        # Sometimes tokenization might not align perfectly with char offsets if there's no whitespace.
        # But WhitespaceTokenSplitter uses \S so it should be okay.
        
        # More robust token span finding:
        start_token = -1
        end_token = -1
        for i, (t, s, e) in enumerate(tokens_with_offsets):
            if s <= start_char_idx < e:
                start_token = i
            if s < end_char_idx <= e:
                end_token = i
        
        if start_token != -1 and end_token != -1:
            dataset.append({
                "tokenized_text": token_list,
                "ner": [[start_token, end_token, "bank"]]
            })

    # Negative samples
    random.shuffle(neg_sentences)
    selected_neg = neg_sentences[:num_neg]
    
    for text in selected_neg:
        tokens_with_offsets = list(splitter(text))
        token_list = [t[0] for t in tokens_with_offsets]
        dataset.append({
            "tokenized_text": token_list,
            "ner": []
        })

    random.shuffle(dataset)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {len(dataset)} samples.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
