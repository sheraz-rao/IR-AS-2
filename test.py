import xml.etree.ElementTree as et
from nltk import PorterStemmer

queries = []
data = et.parse('topics.xml')
d = data.getroot()

for i in range(0, 10):
    query = (d[i][0].text)
    query.lower()
    query.split()
    # stopwords = open('stoplist.txt', 'r')
    # stop = [w for w in query if w not in stopwords]
    # stopwords.close()
                
    stemm = [PorterStemmer().stem(s) for s in query]
    queries.append(stemm)
    
print(queries)        