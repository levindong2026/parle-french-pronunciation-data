"""Search the teaching CSV by spelling or by exact IPA label."""

import argparse
import csv
import json
import unicodedata
from pathlib import Path


def spelling_key(value):
    return unicodedata.normalize("NFC", value.strip().casefold())


def ipa_key(value):
    return unicodedata.normalize("NFC", value.strip())


def load_indexes(path):
    by_spelling = {}
    by_ipa = {}
    with Path(path).open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            label = ipa_key(row["ipa"])
            if label in by_ipa:
                raise ValueError(f"Duplicate IPA label after NFC normalization: {label}")
            by_ipa[label] = row

            spellings = (spelling_key(part) for part in row["spellings"].split("|"))
            for spelling in dict.fromkeys(spellings):
                by_spelling.setdefault(spelling, []).append(row)
    return by_spelling, by_ipa


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("mode", choices=("spelling", "ipa"))
    parser.add_argument("query", help="For IPA, use the slash-delimited label from the CSV")
    args = parser.parse_args()

    by_spelling, by_ipa = load_indexes(args.csv)
    if args.mode == "spelling":
        rows = by_spelling.get(spelling_key(args.query), [])
    else:
        row = by_ipa.get(ipa_key(args.query))
        rows = [] if row is None else [row]
    print(json.dumps([row["ipa"] for row in rows], ensure_ascii=False))


if __name__ == "__main__":
    main()
