import pandas as pd
import re

df = pd.read_csv('train.csv')
df.fillna('', inplace=True)

import string

TRAIN_COMBINED = []

total_conflicts = 0

def find_match(raw_words, target_words, ignore_truncated=True):
    
    low = 0
    high = 0
    pattern_index = 0
    found = False
            
    while high < len(raw_words):

        word = raw_words[high]

        if pattern_index == len(target_words):
            found = True
            break
            
        elif not ignore_truncated and (target_words[pattern_index].startswith(word) or target_words[pattern_index].startswith(word[:-1])):
            high += 1
            pattern_index += 1

        elif target_words[pattern_index] == word or target_words[pattern_index] == word[:-1]:
            high += 1
            pattern_index += 1

        else:
            low += 1
            high = low
            pattern_index = 0
            
    if pattern_index == len(target_words):
        found = True

    if found:
        vector = [1 if i >= low and i < high else 0 for i in range(len(raw_words))]
    else:
        vector = [0 for i in range(len(raw_words))]
        
    return vector

for index, row in df.iterrows():
    raw_address = row['raw_address']
    poi, street = row['POI/street'].split('/')
    
    combined_entities = []
    
    first_entity = None
    
    if poi:
        
        m = re.search(re.escape(poi), raw_address)
        
        if m:
            low, high = m.start(), m.end()
        
        else:
            
            vector = find_match(raw_address.split(), poi.split(), False)

            curr_idx = 0
            low = None
            high = None

            for i in range(len(vector)):
                if vector[i] == 1 and low == None:
                    low = curr_idx
                elif vector[i] == 0 and low != None and high == None:
                    high = curr_idx - 1
                    break

                curr_idx += len(raw_address.split()[i]) + 1

            if low != None and high == None:
                high = len(raw_address)

        if low != None and high != None:

            while raw_address[high - 1] in string.punctuation:
                high -= 1

            first_entity = (low, high, "POI")
            combined_entities.append((low, high, "POI"))
            
    if street:
        
        m = re.search(re.escape(street), raw_address)
        
        if m:
            low, high = m.start(), m.end()
        
        else:
        
            vector = find_match(raw_address.split(), street.split(), False)

            curr_idx = 0
            low = None
            high = None

            for i in range(len(vector)):
                if vector[i] == 1 and low == None:
                    low = curr_idx
                elif vector[i] == 0 and low != None and high == None:
                    high = curr_idx - 1
                    break

                curr_idx += len(raw_address.split()[i]) + 1

            if low != None and high == None:
                high = len(raw_address)
        
        if low != None and high != None:
            
            while raw_address[high - 1] in string.punctuation:
                high -= 1
            
            if first_entity and (
                # Starting index overlaps with POI tag
                low >= first_entity[0] and low <= first_entity[1] or 
                
                # Ending index overlaps with POI tag
                high >= first_entity[0] and high <= first_entity[1] or
                
                # POI tag is a subset of SRT tag
                low < first_entity[0] and high > first_entity[1]
            ):
                # Conflicting tags
                total_conflicts += 1
            
            else:
                combined_entities.append((low, high, "SRT"))
    
    combined_spacy_entry = (raw_address, {"entities": combined_entities})
    TRAIN_COMBINED.append(combined_spacy_entry)

print(f"{total_conflicts} total conflicts.")
print(TRAIN_COMBINED[:10])

import spacy
import random
import logging
logging.captureWarnings(True)

print("Preparing...")

nlp = spacy.blank("id") # Indonesian
ner = nlp.create_pipe("ner")
nlp.add_pipe(ner)
ner.add_label("POI")
ner.add_label("SRT")

from spacy.util import minibatch, compounding
from spacy.util import decaying

print("Training...")

# Start the training
nlp.begin_training()

dropout = decaying(0.6, 0.2, 1e-4)

# Loop for 20 iterations
for itn in range(20):
    
    # Shuffle the training data
    random.shuffle(TRAIN_COMBINED)
    losses = {}
    
    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(TRAIN_COMBINED, size=compounding(4.0, 32.0, 1.001)):
        texts = [text for text, entities in batch]
        annotations = [entities for text, entities in batch]
        
        # Update the model
        nlp.update(texts, annotations, losses=losses, drop=next(dropout))
        
    print(f"Epoch: {itn}\tLosses: {str(losses)}")
    
nlp.to_disk("combined.model")