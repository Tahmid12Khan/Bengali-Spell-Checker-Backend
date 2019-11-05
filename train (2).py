# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 07:21:00 2019

@author: tahmid
"""

from gensim.models import Word2Vec

w2v = Word2Vec.load('word2vec_300_5.model')
print(len(w2v.wv.vocab))
w2vSorted=dict(sorted(w2v.wv.vocab.items(), key=lambda x: x[1],reverse=True))

cc = 0
for j in w2vSorted:
    cc += 1
    if cc == 1300000: 
        print(j, w2vSorted[j])

for word, vocab_obj in w2v.vocab.items():

print(w2v.wv.most_similar('আমি'))

w2v.wv.similarity('কাপড়', 'পড়ি')
w2v.wv.similarity('কাপড়', 'পরি')
w2v.wv.similarity('কাপড়', 'পরী')
w2v.wv.similarity('কাপড়', 'খাই')
w2v.wv.similarity('কাপড়', 'পোশাক')
w2v.wv.similarity('পড়ি', 'পোশাক')
w2v.wv.similarity('পোশাক', 'পড়ি')
w2v.wv.similarity('পোশাক', 'পরি')

w2v.wv.similarity('আমি', 'পড়ি')
w2v.wv.similarity('আমি', 'পরি')

w2v.wv.similarity('ভাল', 'কাপড়')
w2v.wv.similarity('ভালো', 'কাপড়')

w2v.wv.similarity('সূর্য', 'সূর্যের')
w2v.wv.similarity('সূর্যের', 'আলু')
w2v.wv.similarity('সূর্যের', 'আলো')
w2v.wv.similarity('সূর্য', 'আলো')
w2v.wv.similarity('সূর্য', 'আলু')

w2v.wv.distance('কাপড়', 'পড়ি')
w2v.wv.distance('কাপড়', 'পরি')
w2v.wv.distance('কাপড়', 'পরী')
w2v.wv.distance('কাপড়', 'খাই')
w2v.wv.distance('কাপড়', 'পোশাক')
w2v.wv.distance('পড়ি', 'পোশাক')

# সূর্য সূর্যের আল আলু আলো এলো 
# আমি কাপর কাপড় পড়ি পরী পরি 
# বই জামা পোশাক তুমি ভাত খাই তারা আসবে না 
# কাপর ভালো ভাল 