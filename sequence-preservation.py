import nltk
import sys
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def process_file(filename):
    with open(filename, 'r') as f:
        text = f.read()

    words = word_tokenize(text)
    pos_tags = nltk.pos_tag(words)

    unique_words = []

    for word, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos)
        if wordnet_pos in {wordnet.NOUN, wordnet.VERB, wordnet.ADJ} and word.isalpha() and len(word) >= 3 and word.encode('ascii', 'ignore').decode() == word and word not in unique_words:
            unique_words.append(word)

    return unique_words

filename = sys.argv[1]
unique_words = process_file(filename)

translator = GoogleTranslator(source='auto', target='russian')

with open('en.txt', 'w') as en_file, open('ru.txt', 'w') as ru_file:
    for word in unique_words:
        en_file.write(word + '\n')
        translation = translator.translate(word)
        ru_file.write(translation + '\n')

print("Done")
