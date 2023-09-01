import json


def preprocess_possible_json(text: str) -> dict:
    """Preprocess a json written according to MD convention"""
    start_1 = "```json\n"
    start_2 = "```\n"
    start_3 = "```"

    initial = None

    if start_1 in text:
        initial = text.index(start_1) + len(start_1)
    elif start_2 in text:
        initial = text.index(start_2) + len(start_2)
    elif start_3 in text:
        initial = text.index(start_3) + len(start_3)

    end_1 = "\n```"
    end_2 = "```"

    final = None

    if end_1 in text:
        final = text.index(end_1, initial if initial else 0)
    elif end_2 in text:
        final = text.index(end_2, initial if initial else 0)

    json_text = text[initial if initial else 0 : final if final else len(text)]

    return json.loads(json_text)
