import json


def read_multi_json(filepath):
    """Read a file containing multiple concatenated JSON objects."""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(content):
        while idx < len(content) and content[idx] in ' \t\n\r':
            idx += 1
        if idx >= len(content):
            break
        obj, end_idx = decoder.raw_decode(content, idx)
        records.append(obj)
        idx = end_idx
    return records


if __name__ == "__main__":
    filepath = r"K:\share\0.TBSMMHS\Customer Behaviour Analysis\00_CB Model Inventory\Model ID_15057 Black Knight LPS\US Construction Loan\TAL_JSON_Input.txt"
    records = read_multi_json(filepath)
    print(f"Loaded {len(records)} JSON records.")
