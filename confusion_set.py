from gensim.models import Word2Vec
import nltk
w2v = Word2Vec.load('word2vec_300_5.model')
from phonetic_encoder import *
bangla_words = set()
extras = set()
remove_letters = []
letters = []
priority = 0.8
def is_sounds_same(word, candidate):
    try:
        return doublemetaphone_encode(word) == doublemetaphone_encode(candidate)
    except:
        return False
def score(similarity, word, candidate):
    ds = nltk.edit_distance(word_cutter(word), word_cutter(candidate))
    if is_sounds_same(word, candidate):
        ds = 0
#        return abs(3 * priority * similarity / (ds + 1));
#    if ds >= 3:
#        ds = 2
#    return abs(priority * similarity / (ds + 1));
    return priority * similarity - (1-priority) * (ds)

def word_cutter(word):
    return word
    _result_word = ''
    for letter in word:
        if letter not in remove_letters:
            _result_word += letter
    return _result_word

def valid_bengali_words_acc_to_dic(word):
    __word = word
    if __word in bangla_words:
        return True
    extra = ''
    while len(__word) != 0:
        extra = __word[-1] + extra
        __word = __word[:-1]
        if __word in bangla_words and extra in extras:
            return True
    return False
def is_true_word(word):
    if word in w2v.wv.vocab and w2v.wv.vocab[word].count > 100:
        return True

    return False
def valid_bengali_words(words):
    return [word for word in words if valid_bengali_words_acc_to_dic(word) == True]
            
def read_letters():
    bengali_letters = open('bengali_letters.txt', 'r', encoding='utf-8')
    return [letter.strip() for letter in bengali_letters]

def read_bangla_words():
    bangla_words = open('bangla_words.txt', 'r', encoding='utf-8')
    return set(word.strip() for word in bangla_words)

def read_extras():
    extras = open('extra.txt', 'r', encoding='utf-8')
    return set(word.strip() for word in extras)

def candidates(word):
    candidates = set(valid_words for valid_words in get_phonetic_similar_words(word) if is_true_word(valid_words) == True)
    return candidates.union(known([word])).union(known(edits1(word))).union(known(edits2(word)))
#    return candidates.union(known([word])).union(known(edits1(word)))
def known(words): 
    return set(w for w in words if is_true_word(w))

def known2(words, word):
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

def read_remove_letters():
    remove_letters = open('remove_letters.txt', 'r', encoding='utf-8')
    return [letter.strip() for letter in remove_letters]
    

letters = read_letters()
bangla_words = read_bangla_words()
extras = read_extras()
remove_letters = read_remove_letters()
def main():
    letters = read_letters()
    bangla_words = read_bangla_words()
    ww = 'নিপুনের'
    print(known2(edits2(ww), ww))
    candidates('নিপুনের')
    
#print(is_true_word('পরিa'))
#print('পারেন' in valid_bengali_words(candidates('পারেন')))
#
#w = 'পরি'
#print(candidates(w))
#print(len(candidates(w)))
#from phonetic_encoder import doublemetaphone_encode
#
#for word in candidates(w):
#    if doublemetaphone_encode(w) == doublemetaphone_encode(word):
#        print(word)
#candidate = 'ভাসা'
#context = ['মুখের', 'ঠিক', 'কর']
#scores = w2v.wv.n_similarity([candidate], context)
#print(scores)