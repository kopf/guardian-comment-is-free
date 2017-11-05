import json

import markovify
import spacy

nlp = spacy.load("en")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

REPLACEMENTS = {
    '\u2019': "'",
    " 's": "'s",
    " 'd": "'d",
    " 've": "'ve",
    " .": ".",
    " ,": ",",
    " n't": "n't",
    " 're": "'re",
    " 'm": "'m",
    " !": "!",
    " ?": "?",
    "( ": "(",
    " )": ")"
}

def load_dataset():
    with open('dataset.json', 'r') as f:
        data = json.load(f)
    dataset = ''
    for url, metadata in data.items():
        title = metadata['title']
        for find, replace in REPLACEMENTS.items():
            title = title.replace(find, replace)
        if '|' in title:
            title = title[:title.index('|')]
        title.strip()
        title += '. '
        dataset += title 
    return dataset

def main():
    print("Loading...")
    dataset = load_dataset()
    print("Creating model...")
    model = POSifiedText(dataset)
    print("Done.\n\n")
    for i in range(100):
        # since we do some post-processing which shortens the sentence,
        # 160 should be fine as a hard limit:
        sentence = model.make_short_sentence(max_chars=160)
        for find, replace in REPLACEMENTS.items():
            sentence = sentence.replace(find, replace)
            sentence = sentence.lstrip(" .")
        print(sentence)
        


if __name__ == '__main__':
    main()
