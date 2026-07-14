import json


def load_json(path):

    with open(path, "r", encoding="utf8") as f:

        return json.load(f)


def clean_text(value):

    if value is None:

        return ""

    return str(value).strip()


def is_blank(value):

    if value is None:

        return True

    return str(value).strip() == ""