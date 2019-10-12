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
    
    huge_list = []

    with open("stoplist.txt", "r") as f:
        huge_list = f.read().split()

    for w in query1: 
        if w in huge_list:
            #print(query1)        
            query1.remove(w)
            
    query2 = [PorterStemmer().stem(s) for s in query1]
    print(query2)
    query2 = [w.replace("world'", 'world') for w in query2]
    queries.append(query2)
    
print(queries)        