import spacy

nlp = spacy.load("combined.model")

import pandas as pd

df = pd.read_csv('test.csv')

results = {}

for index, row in df.iterrows():
    raw_address, id = row['raw_address'], row['id']
    
    doc = nlp(raw_address)
    
    elements = [(X.text, X.label_) for X in doc.ents]
    poi_elements = [x for x in elements if x[1] == 'POI']
    srt_elements = [x for x in elements if x[1] == 'SRT']
    
    if not poi_elements:
        poi_elements = [('', '')]
    
    if not srt_elements:
        srt_elements = [('', '')]
    
    results[id] = (poi_elements, srt_elements)

with open('submission.csv', 'w') as f:
    f.write("id,POI/street\n")
    for id in range(50000):
        poi = results[id][0][0][0]
        srt = results[id][1][0][0]
        
        f.write(f"{id},\"{poi}/{srt}\"\n")

df = pd.read_csv('submission.csv')

from spacy.scorer import Scorer
from spacy.gold import GoldParse
import logging
import random

logging.captureWarnings(True)

def evaluate(ner_model, examples):
    scorer = Scorer()
    for input_, annot in examples:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot.get('entities'))
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores

# random.shuffle(TRAIN_COMBINED)
# print(evaluate(nlp, TRAIN_COMBINED[:100]))