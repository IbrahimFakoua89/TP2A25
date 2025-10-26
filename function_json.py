from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path
from typing import List


# chatGPT

def save_list_to_json(strings, filepath, indent: int = 2, ensure_ascii: bool = False) -> None:

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", dir=str(path.parent), delete=False, encoding="utf-8") as tf:
        json.dump(strings, tf, ensure_ascii=ensure_ascii, indent=indent)
        tempname = tf.name
    os.replace(tempname, str(path))


def load_list_from_json() -> List[str]:

    path = Path("json_file/functions.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError(f"JSON file {path!s} does not contain a list of strings")
    return data
