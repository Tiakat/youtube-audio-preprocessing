import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Given a string of unparsed labels, return the number of distinct labels.

    For example:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    # TODO
    if not labels or pd.isna(labels) or labels == "":
        return 0
    return len(labels.split(','))


def convert_id(ID: str) -> str:
    """
    Create a function that takes in a label ID (e.g. "/m/09x0r") and returns the corresponding label name (e.g. "Speech")
    """
    # TODO
    # Load ontology when needed
    try:
        with open("data/ontology.json", "r") as f:
            ontology = json.load(f)
        id_to_name = {item["id"]: item["name"] for item in ontology}
        return id_to_name.get(ID, ID)
    except FileNotFoundError:
        return ID  # Return original ID if file not found


def convert_ids(labels: str) -> str:
    """
    Using get_label_name() create a function that takes the label columns (i.e a string of comma-separated label IDs)
    and returns a string of label names, separated by pipes "|".
    """
    # TODO
    if not labels or pd.isna(labels) or labels == "":
        return ""
    
    ids = labels.split(',')
    names = [convert_id(id.strip()) for id in ids]
    return "|".join(names)


def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Create a function that takes a Series of strings where each string is formatted as above 
    (i.e. "|" separated label names like "Music|Skateboard|Speech") and returns a Series with just
    the values that include `label`.
    """
    # TODO
    return labels[labels.apply(lambda x: label in str(x).split('|') if pd.notna(x) else False)]


def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Create a function that, given a Series as described above, returns the proportion of rows
    with label_1 that also have label_2.
    """
    # TODO
    has_label1 = contains_label(labels, label_1)
    if len(has_label1) == 0:
        return 0.0
    
    has_both = has_label1[has_label1.apply(lambda x: label_2 in str(x).split('|'))]
    return len(has_both) / len(has_label1)


if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))