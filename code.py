#!/usr/bin/env python
# coding: utf-8

# In[66]:


import csv
import math
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')
nltk.download('wordnet')


# In[67]:


# remove punctuation from the string
tokenizer = RegexpTokenizer(r'\w+')
# convert word to its base form like running to run.
lemmatizer = WordNetLemmatizer() 
# get stem of the word.
stemmer = SnowballStemmer("english")


# In[68]:


# Read all words mapping from the file.
word_mapping = {}
with open('wordmapping.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        word = stemmer.stem( lemmatizer.lemmatize(row[0]) )
        word_mapping[ word ] = row[1]


# In[69]:


# Read dataset line by line
with open('dataset-CalheirosMoroRita-2017.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    skip_first = True
    csv_lines = []
    current_line = 1
    list_of_socres = {}
    for row in csv_reader:
#       each row is a review, convert it into a string, then tokenize it using nltk.tokenizer
#       get lemma of each word, then get stem of each word in review.
        string = ''.join(row)
        tokens = tokenizer.tokenize(string.lower())
        tokens = [lemmatizer.lemmatize(token)  for token in tokens]
        tokens = [stemmer.stem(token)  for token in tokens]
#       save each review in list to access reveiws using list indexing
        csv_lines.append(string)
        if skip_first:
            skip_first = False
            continue
#       check if words in reviews exist in specific review if yes then get its word mapping.
        words = []
        total_weight = 0
        for i in tokens:
            if i in word_mapping:
                val = int(word_mapping.get(i))
                total_weight += val
                words.append( (i, val) )
#       calculate the setimental score of each review and save it into dictionary structure.
        sentimental_score = math.ceil( (total_weight/len(tokens))*100 )
        list_of_socres[current_line] = {"score":sentimental_score, 
                                        "weight": total_weight, "total_words":len(tokens),
                                        "words weight": words
                                       }
        current_line += 1        


# In[70]:


# details for each syntax can be get from list_of_socres list variable, like below
syntax = 2
print(f"Syntax: {syntax} details ", list_of_socres[syntax])


# In[ ]:




