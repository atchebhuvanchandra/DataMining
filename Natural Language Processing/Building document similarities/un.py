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

print(bigrams[0])

'''DataBase connection'''
# Connect
db = pymysql.connect(host="localhost", user="root",passwd="abc5s3",db="mydb")
cursor = db.cursor()
cursor.execute("DELETE FROM tf")
cursor.execute("DELETE FROM df")
cursor.execute("DELETE FROM tf_idf")





'''Caluculating DF for all words''' 
DF = {}
for j in range(N):
       tokens = processed_text[j]
       for w in tokens:
           try:
               DF[w].add(i)
           except:
               DF[w] = {i}
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

#deleting alphanumeric and data with dots
cursor.execute("DELETE FROM tf WHERE Term Like '%[A-Za-z0-9]%'")
cursor.execute("DELETE FROM tf WHERE Term Like '%.%'")
cursor.execute("DELETE FROM df WHERE Term Like '%[A-Za-z0-9]%'")
cursor.execute("DELETE FROM df WHERE Term Like '%.%'")
cursor.execute("DELETE FROM tf_idf WHERE Term Like '%[A-Za-z0-9]%'")
cursor.execute("DELETE FROM tf_idf WHERE Term Like '%.%'")

db.close()

print(tf_idf)

    
