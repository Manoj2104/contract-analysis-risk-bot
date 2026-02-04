from app.modules.ner import get_entities
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sample_path = os.path.join(BASE_DIR, "data", "samples", "sample_contract.txt")

with open(sample_path, "r", encoding="utf-8") as f:
    text = f.read()

entities = get_entities(text)

print("Extracted Entities:")
for key, values in entities.items():
    print(f"{key}: {values}")
