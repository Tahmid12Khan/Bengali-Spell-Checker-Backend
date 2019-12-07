# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:26:36 2019

@author: hp
"""

remove_letters = ['্']
bengali_words = open('bangla_words.txt', 'r', encoding='utf-8')
words = [word for word in bengali_words]
print(len(words))
new_words = []
for word in words:
    new_word = ''
    for letter in word:
        if letter in remove_letters:
            continue
        new_word += letter
    new_words.append(new_word)
    
print(len(new_words))

wr = open('bangla_words_processed.txt', 'w+', encoding='utf-8')

for word in new_words:
    wr.write(word.strip() + '\n');
    