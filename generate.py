from collections import Counter
from csv import reader
from random import randint
from sys import argv

# how often to add an extra cloze
ANOTHER_CLOZE_FACTOR = 50

# how often add a fake cloze that doesn't replace anything
EMPTY_CLOZE_FACTOR = 50

# how many most-common words will be replaced by clozes
WORD_MIN_RANK = 1000

# evil evil words to not cover with the cloze
FORBIDDEN_CLOZE_TOKENS = {'Tom', 'Mary'}


def normalize(text: str, lang: str):
    """Normalize the text.
    This is used to allow comparison of tokens to extract the frequency
    """
    if text[:-1] in '.,?!;':
        text = text[:-1]
    return text.lower()


def tokenize(text: str, lang: str):
    """Split a string into tokens."""
    # TODO actually tokenize according to the language
    return text.split()


def main(src_lang: [str], tgt_lang: str):
    """Produce the cloze deletion cards.

    Parameters
    ----------
    src_lang : [str]
        Source languages, e.g. ['eng', 'ita']
    tgt_lang : str
        Target language, e.g. 'deu'
    """
    sents = reader(open('sentences.csv'), delimiter='\t')
    links = reader(open('links.csv'), delimiter='\t')

    tgt_sents = {}
    src_lang_sents = {}

    word_counter = Counter()

    print(f'Importing {src_lang} to {tgt_lang} sentence pairs')

    for [_id, lang, text] in sents:
        if lang not in src_lang and lang != tgt_lang:
            continue
        if len(text) > 140 or len(text) < 20:
            continue
        if lang in src_lang:
            src_lang_sents[int(_id)] = text
        else:
            tgt_sents[int(_id)] = text
            word_counter.update(tokenize(normalize(text, tgt_lang), tgt_lang))
    print(
        f'Imported {len(src_lang_sents)}/{len(tgt_sents)}'
        ' src_lang/tgt sentences'
    )

    most_common = set(w for w, _ in word_counter.most_common(WORD_MIN_RANK))
    del word_counter

    pairs = []
    for [from_id, to_id] in links:
        from_id = int(from_id)
        to_id = int(to_id)

        if from_id not in src_lang_sents or to_id not in tgt_sents:
            continue
        pairs.append((src_lang_sents[from_id], tgt_sents[to_id]))

    print(f'Found {len(pairs)} sentence pairs')

    out = open('cards.tsv', 'w')
    for s, t in pairs:
        tokens = tokenize(t, tgt_lang)
        cloze_idx = 1
        for _ in range(100):
            to_replace_idx = randint(0, len(tokens) - 1)
            # no cloze of a cloze
            if tokens[to_replace_idx].startswith('{{'):
                continue
            # only the most common words
            if normalize(tokens[to_replace_idx], tgt_lang) not in most_common:
                continue
            # ignore forbidden words
            if tokens[to_replace_idx] in FORBIDDEN_CLOZE_TOKENS:
                continue
            tokens[to_replace_idx] = ''.join([
                '{{c',
                str(cloze_idx),
                '::',
                tokens[to_replace_idx],
                '}}'
            ])
            cloze_idx += 1

            if randint(0, EMPTY_CLOZE_FACTOR) == 0:
                to_insert_idx = randint(0, len(tokens) - 1)
                tokens.insert(
                    to_insert_idx,
                    '{{c' + str(cloze_idx) + '::-}}'
                )
                cloze_idx += 1

            if randint(0, ANOTHER_CLOZE_FACTOR) == 0:
                continue
            break

        if cloze_idx == 1:
            continue
        out.write(s)
        out.write('<br>')
        out.write(' '.join(tokens))
        out.write('\n')

    out.close()


if __name__ == '__main__':
    main(
        argv[1].split(','),
        argv[2]
        )
