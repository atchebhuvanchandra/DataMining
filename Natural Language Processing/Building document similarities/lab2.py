from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.util import ngrams
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import numpy as np
import nltk
import pymysql


tag_removal = re.compile(r'<[^>]+>')

def remove_tags(text):
    return tag_removal.sub('',text)
'''The process of removing html tags from the text by replacing with null'''
for i in range(1,6):
    string = open('doc'+str(i)+'.txt').read()
    open('doc'+str(i)+'.txt','w').write(remove_tags(string))

''' #Removing all the symbols like punctuation marks ,question marks etc...
    and replacing by ' '(space)
'''
for i in range(1,6):
   string1 = open('doc'+str(i)+'.txt').read()
   new_str = re.sub('[^a-zA-Z0-9\n\.]',' ',string1)
   string1 = re.sub("\S*\d\S*", "", new_str).strip()
   open('doc'+str(i)+'.txt','w').write(string1)

'''Removing stop words using tokenize and stop_words in python '''
stop_words = stopwords.words("english")
for i in range(1,6):
    string2= open('doc'+str(i)+'.txt').read()
    open('doc'+str(i)+'.txt','w').write(' '.join([word for word in string2.split() if word not in stop_words]).lower()+' ')

''' #Stemming data
stemmer  = PorterStemmer()
temp_string = ""

for i in range(1,6):
    string = open('doc'+str(i)+'.txt').read()
    tokens = word_tokenize(string)
    for w in tokens:
         temp_string = temp_string+" "+stemmer.stem(w)
    open('doc'+str(i)+'.txt','w').write(temp_string)

'''

'''Creating tokens '''
processed_text = []

for i in range(1,6):
    string3 = open('doc'+str(i)+'.txt').read()
    processed_text.append(word_tokenize(string3))



'''function to create ngrams from a list of words '''
def generate_ngrams(words_list,n):
    ngrams_list = []

    for num in range(0,len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list

'''Replacing data mining and machine learning'''
bigrams=[]
for i in range(0,5):
    bigrams.append(generate_ngrams(processed_text[i],2))
    

data=[]
'''Total N '''
for i in range(0,5):
    processed_text[i] = processed_text[i] + bigrams[i]
    data.extend(processed_text[i])
    #data.extend(bigrams[i])
    
N = len(data)


'''DataBase connection'''
# Connect
db = pymysql.connect(host="localhost", user="root",passwd="abc5s3",db="mydb")
cursor = db.cursor()
cursor.execute("DELETE FROM tf")
cursor.execute("DELETE FROM df")
cursor.execute("DELETE FROM tf_idf")


'''Calculating DF for all words'''
DF = {}

for j in range(0,5):
    tokens = processed_text[j]
    for w in tokens:
        try:
            DF[w].add(j)
        except:
            DF[w] = {j}

for i in DF:
    DF[i] = len(DF[i])


total_vocab_size = len(DF)

total_vocab = [x for x in DF]

def doc_freq(word):
    c =0
    try:
        c = DF[word]
    except:
        pass
    return c




'''Calculating TF-IDF '''
doc = 1

tf_idf = {}
vtf = {}
for j in processed_text:
       tokens = j
       
       counter = Counter(tokens)
       words_count = len(tokens)

       for token in np.unique(tokens):

            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1))
            L = [str(token),int(doc),int(counter[token])]
            cursor.execute("INSERT INTO tf VALUES(%s,%s,%s)",L)
            #vtf[doc,token]=counter[token]
            L1 = [str(token),doc_freq(token)]
            cursor.execute("INSERT INTO df VALUES(%s,%s)",L1)       
            
            tf_idf[doc,token] = tf*idf
            L2=[int(doc),str(token),float(tf_idf[doc,token])]
            cursor.execute("INSERT INTO TF_IDF VALUES(%s,%s,%s)",L2)
       doc +=1

d_f=pd.DataFrame(index=[1,2,3,4,5],columns=['engineering','research','data','mining','data mining','machine learning'])

for i in d_f.index:
    for j in d_f.columns:
        te = [str(j),i]
        cursor.execute("SELECT tfidf FROM tf_idf WHERE `TERM` =%s AND `DOC#` =%s",te)
        _tfidf = cursor.fetchall()
        if len(_tfidf) > 0:
           d_f.at[i,j] = float(_tfidf[0][0])
        else :
           d_f.at[i,j] = 0
print('-------------------------TF-IDF-----------------------------')
print(d_f)

cosinesimilarity = pd.DataFrame(index=[0,1,2,3,4],columns=[0,1,2,3,4])
a =cosine_similarity(d_f)
print('------------------Cosine Similarity-------------------')

cosinesimilarity=pd.DataFrame(data=a,index=['doc1','doc2','doc3','doc4','doc5'],columns=['doc1','doc2','doc3','doc4','doc5'])
print(cosinesimilarity)
