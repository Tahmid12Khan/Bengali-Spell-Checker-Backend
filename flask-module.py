
from confusion_set import *
from phonetic_encoder import doublemetaphone_encode, soundex_encode
from flask import Flask, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
import nltk
priority = 0.6

def score(similarity, word, candidate):
    ds = nltk.edit_distance(word, candidate)
    if is_sounds_same(word, candidate):
        ds = 0
    return priority * similarity + (1-priority) * (2 - ds);

def get_valid_context_words(context_words):
    return [valid_word for valid_word in context_words if valid_word in w2v.wv.vocab]

def is_sounds_same(word, candidate):
    try:
        return doublemetaphone_encode(word) == doublemetaphone_encode(candidate)
    except:
        return False

def get_suggestions(word, context_words):
    context_words = get_valid_context_words(context_words)
    suggestions = []
    for candidate in candidates(word):
        suggestions.append((score(w2v.wv.n_similarity([candidate], context_words), word, candidate), candidate))
    suggestions.sort(reverse = True)
    top_five_score = [suggestion[0] for suggestion in suggestions[:5]]

    top_five_suggestions = [suggestion[1] for suggestion in suggestions[:5]]
    print(top_five_score)
    print(top_five_suggestions)
    if word not in top_five_suggestions:
        return top_five_suggestions
    return []

def valid_bengali_letters(char):
    return ord(char) >= 2433 and ord(char) <= 2543

def get_replacement(char):
    if valid_bengali_letters(char):
        return char
    newlines = [10, 2404, 2405, 2551, 9576]
    if ord(char) in newlines:
        return '\n'
    return ' ';

def get_valid_lines(line):
    copy_line = ''
    for letter in line:
        copy_line += get_replacement(letter)
    return copy_line

def test():
    get_suggestions('স্কুলে', ['আমি' , 'যাই'])
    get_suggestions('ইস্কুলে',  ['আমি', ' যাই'] )
    get_suggestions('ইশকুলে', ['আমি',  'যাই'] )
    get_suggestions('পড়ে', ['সে',  'বই' ])
    get_suggestions('পরা', ['বই', 'উচিত'])


def temp(data):
    my_suggestions = get_suggestions(data['word'], data['contexts'])
    response = {}
    response['status'] = 'success'
    response['suggestions'] = []
    if len(my_suggestions) == 0:
        return response
    response['status'] = 'error'

    response['suggestions'] = my_suggestions
    print(response)
    return response

@app.route('/', methods=['POST'])
def calc():
    print('Got ', request.get_json())
    return temp(request.get_json())


if __name__ == '__main__':
    app.run(debug=False, threaded= False)