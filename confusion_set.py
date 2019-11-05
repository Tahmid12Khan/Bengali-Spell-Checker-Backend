from gensim.models import Word2Vec
w2v = Word2Vec.load('word2vec_300_5.model')
from phonetic_encoder import *
bangla_words = set()
letters = []

def read_letters():
    bengali_letters = open('bengali_letters.txt', 'r', encoding='utf-8')
    return [letter.strip() for letter in bengali_letters]

def read_bangla_words():
    bangla_words = open('bangla_words.txt', 'r', encoding='utf-8')
    return set(word.strip() for word in bangla_words)

def candidates(word):
    candidates = set(valid_words for valid_words in get_phonetic_similar_words(word) if valid_words in w2v.wv.vocab)
    return candidates.union(known([word])).union(known(edits1(word))).union(known(edits2(word)))
#    return candidates.union(known([word])).union(known(edits1(word)))
def known(words): 
    return set(w for w in words if w in w2v.wv.vocab)

def known2(words, word):
    print(words)
    return set(w for w in words if w in w2v.wv.vocab and doublemetaphone_encode(word) == doublemetaphone_encode(w))

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

letters = read_letters()
bangla_words = read_bangla_words()
def main():
    letters = read_letters()
    bangla_words = read_bangla_words()
    ww = 'নিপুনের'
    print(known2(edits2(ww), ww))
    candidates('নিপুনের')
    
#
#w = 'পরি'
#print(candidates(w))
#print(len(candidates(w)))
#from phonetic_encoder import doublemetaphone_encode
#
#for word in candidates(w):
#    if doublemetaphone_encode(w) == doublemetaphone_encode(word):
#        print(word)
