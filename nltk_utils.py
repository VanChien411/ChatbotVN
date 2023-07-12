import spacy
import numpy as np

# Load the spacy model
nlp = spacy.load("xx_ent_wiki_sm")

def tokenize(sentence):
    """
    Split sentence into array of words/tokens
    """
    doc = nlp(sentence)
    return [token.text for token in doc]

def stem(word):
    """
    Stemming = find the root form of the word
    """
    # Return the lowercase word as it is without stemming
    return word.lower()

def bag_of_words(tokenized_sentence, words):
    """
    Return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    """

    # Initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag
