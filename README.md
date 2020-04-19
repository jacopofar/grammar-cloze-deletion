# grammar-cloze-deletion
Produce Anki cloze deletion cards focused on grammar from Tatoeba dumps

This scripts generate Anki cloze deletion cards by retrieving sentence pairs from languages you know and a (target) langauge you are studying and whose grammar you want to consolidate.

It does not work yet on target languages Chinese, Japanese and any lanuage not using spaces to separater tokens.

It's very very experimental and probably you should not use it if you don't know what you are doing :)

## Instructions

Python 3.6 or later is needed, no extra libraries.

Get the sentences and links file from the Tatoeba download page, extract them in the work folder, then issue the command `python3 generate.py eng,ita deu` (or whatever languages you want).

## TODO
- [ ] Add tokenization for CJK
- [ ] Add lemmatization to generate cards from inflected forms
- [ ] Export Tatoeba metadata to keep a reference to original sentences
