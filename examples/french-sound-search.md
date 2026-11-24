# Searching French sound data without losing accents

Search by spelling when the query is written French, and by IPA label when the query is a sound symbol. Keep those indexes separate. This example uses Python's standard library and the 35-row teaching CSV included in this repository.

## Reproduce two search errors

Decomposing text and removing every combining mark is sometimes used for broad text search. Here it gives two real collisions:

| Original IPA label | Result after removing combining marks | Example words distinguished by the CSV |
| --- | --- | --- |
| `/ɛ̃/` | `/ɛ/` | `vin` and `mère` |
| `/ɔ̃/` | `/ɔ/` | `bon` and `porte` |

Both results already belong to separate entries. The combining tilde carries nasalization. Removing it from `/ɑ̃/` gives `/ɑ/`, which has no row in this particular inventory. The same shortcut would also collapse the spellings `ou` and `où`. Only `ou` is listed as a spelling for `/w/` in this file.

## Use canonical normalization for exact lookup

1. Read the UTF-8 file with `csv.DictReader`. Split the `spellings` field on the pipe character and ignore its surrounding spaces.
2. For written queries, case-fold and normalize to NFC. An `é` entered as U+00E9 and an `e` followed by U+0301 now reach the same row. Accents remain meaningful.
3. For IPA queries, use NFC with the chart’s slash delimiters. Keep case, combining marks and IPA symbols intact. Use the normalized key for lookup and keep the original row for display.
4. Keep every matching row for a spelling. De-duplicate repeated spellings inside each row so a row appears once per result.

[Unicode Standard Annex #15](https://www.unicode.org/reports/tr15/) explains canonical equivalence and normalization forms.

From the repository root, run the [lookup example](search_french_sounds.py):

```console
$ python3 examples/search_french_sounds.py french-sound-chart.csv spelling 'é'
["/e/"]
$ python3 examples/search_french_sounds.py french-sound-chart.csv spelling 'ou'
["/u/", "/w/"]
$ python3 examples/search_french_sounds.py french-sound-chart.csv spelling 'où'
["/u/"]
$ python3 examples/search_french_sounds.py french-sound-chart.csv ipa '/ɔ̃/'
["/ɔ̃/"]
```

Each spelling result is a list of rows that explicitly include that spelling. The lookup does not predict how to pronounce an arbitrary word. If an interface also needs accent-insensitive suggestions, keep them in a separate spelling index and label them as suggestions.

Run `python3 -m unittest discover -s tests` to verify both IPA collisions, the decomposed acute accent, the two spellings and duplicate handling against the bundled CSV.

## Data and attribution

Parle French Sound Chart CSV, Tingnova Inc., [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See the [live chart’s guide to the CSV fields](https://getparle.app/french-sound-chart/#reading-the-csv) and the [archived CSV](https://doi.org/10.5281/zenodo.21932586). This example uses written data only. See the chart’s recording credits for separate audio terms.
