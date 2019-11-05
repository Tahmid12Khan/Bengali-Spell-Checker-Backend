#from gensim.models import Word2Vec
#w2v = Word2Vec.load('word2vec_300_5.model')

from confusion_set import *
from phonetic_encoder import doublemetaphone_encode, soundex_encode

import nltk
priority = 0.8

def score(similarity, word, candidate):
    ds = nltk.edit_distance(word, candidate)
    if is_sounds_same(word, candidate):
        ds = 0
    return priority * similarity + (1-priority) * (2 - ds);

def get_valid_context(words, word_index, left_count, right_count):
    
    list = words[max(word_index - left_count, 0): word_index] + words[word_index + 1: word_index + 1 + right_count]
    
    return [valid_word for valid_word in list if valid_word in w2v.wv.vocab]

def is_sounds_same(word, candidate):
    try:
        return doublemetaphone_encode(word) == doublemetaphone_encode(candidate)
    except:
        return False

def test(test_input, output):
    global total_word, word_correct, sentence_correct, total_sentence, write, true_true, true_false, false_true, false_false, yep, nope
    total_sentence += 1
    output_words = output.split()
    input_words = test_input.split()
    correct = True
    for index, word in enumerate(input_words):
        total_word += 1
        context = get_valid_context(input_words, index, 2, 2)
        suggestions = []
        print(word)
        print(candidates(word))
        for candidate in candidates(word):
            suggestions.append((score(w2v.wv.n_similarity([candidate], context), word, candidate), candidate))
        
        suggestions.sort(reverse = True)
        
        scores = [suggestion[-2] for suggestion in suggestions[:5]]
        suggestions = [suggestion[-1] for suggestion in suggestions[:5]]
        
        #todo delete
#        if word in suggestions:
#            suggestions = [word]
        
        if output_words[index] not in suggestions:            
#            print('Suggestion ' +  str(suggestions) + '\n')
#            print('Scores ' + str(scores) + '\n')
#            print('Current Score: ' + str( score(w2v.wv.n_similarity([candidate], context), word, word)) + '\n')
#            print('Error for ' + str(test_input) +  '->' + str(output) + '\n')
#            print('Did not find valid suggestion at ' + str(index) + ' for ' + str(output_words[index]) + '\n')
#            write.write('------------------------------------------------------'+ '\n')
            correct = False
            if word == output_words[index]:
                true_false += 1
            else:
                false_true += 1
        else:
            if word == output_words[index]:
                if word in suggestions[0:3]:
                    yep += 1
                else: nope += 1
            
            if word == output_words[index]:
                true_true += 1
            else:
                false_false += 1
            word_correct += 1
        input_words[index] = output_words[index]

    if correct:
        sentence_correct += 1
#        print('Suggestions given correctly')
#        print('Incorrect: ', test_input)
#        print('Correct: ', output)

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


read = open('sample.txt', 'r', encoding='utf-8')
arr = []
for line in read:
    arr.append(line)
print(len(arr))

def test_this():
    global total_word, word_correct, sentence_correct, total_sentence, write, true_true, true_false, false_true, false_false, yep, nope
    write = open('output.txt', 'w+', encoding = 'utf-8')
    total_word = 0    
    word_correct = 0
    sentence_correct = 0
    total_sentence = 0
    
    true_true = 0
    true_false = 0
    false_true = 0
    false_false = 0
    
    yep = 0
    nope = 0

    for i in range(0, 1):
        print('Processing ', i + 1, ' Sentences')
        test_input, output = arr[i].split('>')
        try:
            test(get_valid_lines(test_input), get_valid_lines(output)) 
        except Exception as e:
            print(e)
            continue
        if i % 10 == 0:
            print('Total ', total_word, ' correct word ', word_correct)
            print('Total ', total_sentence, ' correct sentence ', sentence_correct)
            print(true_true, '\t', true_false)
            print(false_true, '\t', false_false)
            print('Word Accuracy ', word_correct/total_word)
            print('Sentence Accuracy ', sentence_correct/total_sentence)
            print('yep: ', yep, ', nope: ', nope)

    print('Total ', total_word, ' correct word ', word_correct)
    print('Total ', total_sentence, ' correct sentence ', sentence_correct)
    print('Word Accuracy ', word_correct/total_word)
    print('Sentence Accuracy ', sentence_correct/total_sentence)
    print(true_true, '\t', true_false)
    print(false_true, '\t', false_false)
    #print(nltk.edit_distance('অন্য', 'অহ্ন'))
test_this()
candidates('যে')
doublemetaphone_encode('যে')
#candidates('অন্ন')
#print(soundex_encode('অন্য'))
#print(doublemetaphone_encode('অন্য'))
#print('অন্ন' in candidates('অন্ন'))
