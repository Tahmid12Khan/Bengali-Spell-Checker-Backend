# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 07:21:00 2019

@author: tahmid
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('prothomalo_2017.csv', encoding='utf8', error_bad_lines=False)
X = dataset.iloc[:, -1].values
# =============================================================================
# 
# write_text = open('news.txt', 'w+', encoding='utf-8')
# j = 0
# for i in X:
#    # j += 1
#     #print(j, "---------------")
#     print(i, file=write_text)
# =============================================================================

# Splitting the dataset into the Training set and Test set

#read file
read = open('news.txt', 'r', encoding='utf-8')
lines = []

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

for line in read:
    lines.append(get_valid_lines(line))

dic = {}

for line in lines:
    for letter in line:
        if not letter in dic:
            dic[letter] = 0
        dic[letter] += 1
        
for (key,value) in sorted(dic.items()):
    print(key, ord(key), '---', value)

from bengali_stemmer import BengaliStemmer
bs = BengaliStemmer()
bs.stem_word(word = 'হেরে')
 #টানা তিন ম্যাচে হেরে হোয়াইটওয়াশ
s = {}
cnt = 0
for line in lines:
    for one in line.splitlines():
        cnt += 1
        for two in one.split():
            word = bs.stem_word(two)
            if not word in s:
                s[word] = 0
            s[word] += 1

print(len(s), cnt)

write_words = open('words_stem_reverse_value.txt', 'w+', encoding='utf-8')

for (key, value) in sorted(s.items()):

    write_words.write(key + ' ' + str(value) + '\n')

for key, value in sorted(s.items(), key=lambda item: item[1], reverse=True):
    write_words.write(key + ' ' + str(value) + '\n')

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
