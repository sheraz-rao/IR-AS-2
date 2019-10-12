import xml.etree.ElementTree as et
from nltk import PorterStemmer
from nltk.tokenize import word_tokenize

queries = []
data = et.parse('topics.xml')
d = data.getroot()

for i in range(0, 10):
    query = (d[i][0].text)
    query.lower()
    query1 = query.split()
    stopwords = open('stoplist.txt', 'r')
    sp = stopwords.readlines()
    
    filtered_sentence = [] 
    
    for w in query1: 
        if w not in sp: 
            filtered_sentence.append(w)
    
    stopwords.close()            
    
    query2 = [PorterStemmer().stem(s) for s in filtered_sentence]
    queries.append(query2)
    
print(queries)        