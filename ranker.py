import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
import sys
import json
import ast

corpus_path = r'F:\IR\IR-AS-1\corpus\corpus\corpus'

mapping = {} #this will have {fname: [word,...],...}
posting = {}
docs = []
fileLengths = {}

def remove_headers(file_name):
    with codecs.open(file_name, encoding="utf-8", errors = 'ignore') as f: 
        data = f.read().splitlines()
    
    head = True
    i = 0
    for line in data:
        if ('<html' in line.lower() or\
            '<!doctype html' in line.lower()) \
            and 'content-type:' not in line.lower():
            
            head = False
            file_data = ' '.join(data)
            return file_data
        
        if head == True:
            data[i] = ''
        
        i += 1
        
    file_data = ' '.join(data)
    return file_data

def process_files(path):
    file_names = os.listdir(path)
    doc_id = 1
    term_id = 1
    terms = []
    
    doc_term_positions = []
    term_map = {} #map tokens/words to integer
    
    for file in file_names:
        print(file + ' ' + str(doc_id))
        stopwords = open('stoplist.txt', 'r')
        #ids = open('termids.txt', 'w', encoding="utf-8")
        sp = stopwords.readlines()
        pattern = re.compile('[\W_]+')
            
        #remove header
        data = remove_headers(path + '\\' + file)
        soup = BeautifulSoup(data, "lxml")

        #kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract() 
    
        #get text
        text = soup.get_text()     
        text1 = text.lower();
        text2 = pattern.sub(' ',text1)
        re.sub(r'[\W_]+','', text2)
        
        tokens = word_tokenize(text2)
        
        fileLengths[file] = len(text.split())
        
        # fl = open("fileLen.txt", "a", encoding="utf-8")
        # fl.write(file + ": ")
        # fl.write(str(fileLengths[file]))
        # fl.write("\n")
        # fl.close()
        
        #print("stop wording...\n")           
        stop = [w for w in tokens if w not in sp]
        stopwords.close()
        
        #print("stemming...\n")                
        stemm = [PorterStemmer().stem(s) for s in stop]
        
        mapping[file] = stemm
          
        pos = 1
        for token in stemm:
            if  token not in term_map:
                term_map[token] = term_id
                terms.append(str(term_id) + '\t' + token) #it will be writen to the file
                term_id += 1
            doc_term_positions.append((doc_id, term_map[token], pos))
            pos += 1
         
        #get file name from path and this info  will be written to the .txt file
        docs.append((str(doc_id) + '\t' + file))
        doc_id += 1

    #print("File pre processed.... returning:\n")
    #term_file.close()                               
    return mapping, term_map, fileLengths


def make_word_pos_dict(parameter):
    #input = [word1, word2, ...]
    word_positions = {}
    for index, word in enumerate(parameter):
        if word in word_positions.keys():
            word_positions[word].append(index)
           
        else:
            word_positions[word] = [index]
    
    #output = {word1: [pos1, pos2], word2: [pos2, pos3], ...}       
    return word_positions

def make_hashmap_of_hashmap(parameter):
    #input = {fname: [word1, word2, ...], ...}
    file_word_pos_dict = {}
    for fname in parameter.keys():
        file_word_pos_dict[fname] = make_word_pos_dict(parameter[fname])
    
    #output = {fname: {word: [pos1, pos2, ...]}, ...}
    return file_word_pos_dict


def final_indexing(parameter):
    #input = {fname: {word: [pos1, pos2, ...], ... }}
    final_index = {}
    
    for fname in parameter.keys():
        #iterate through every word in the parameter hash
        for word in parameter[fname].keys():
            #check if that word is present as a key in the final_index. 
            #If it isn’t, then we add it, setting as its value another hashtable
            #that maps the document, in this case by the variable fname, to the list of positions of that word.
            if word in final_index.keys():
                
                #If it is a key, then check: if the current document is in each 
                #word’s hashtable; the one that maps filenames to word positions(fname).
                #If yes, we extend the current positions list with this list of positions
                if fname in final_index[word].keys():
                   final_index[word][fname].extend(parameter[fname][word][:])
                
                #set the positions equal to the positions list for this filename.
                else:
                   final_index[word][fname] = parameter[fname][word]
            else:
                final_index[word] = {fname: parameter[fname][word]}
    
    #res = {word: {fname: [pos1, pos2]}, ...}, ...}
    return final_index

import linecache
from math import log
import xml.etree.ElementTree as et

# Declaring global variables
k1 = 1.2
k2 = 100
b = 0.75
R = 0.0
r = 0
N = 1000
QUERY = "topics.xml"
BM_25_SCORE_LIST = "BM_25_SCORE_LIST"
INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY

# Function to parse the queries
def queryParser():
    queries = []
    freq = {}
    data = et.parse('topics.xml')
    d = data.getroot()
    query2 = []
    
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
        
        for word in query2:
            #res = (term_map.get(word, "Not Found!"))
            #print(word)
        
            #file = "term_index.txt"
            #file1 = "term_info.txt"
            
            # f =  linecache.getline(term_map_file, word)
            # print(f)
            #with open("term_index.txt", "r") as line:
                #l = line.readlines()[res-1]
                #l = np.asarray(list(line))
                #op = open("postings.txt", "a")
                #op.write(l)
            
            #op.write("\n")
            #op.close()
            freq[word] = queryFrequency(query2) #it is the tf(q, i) according to formula
        
        #query2 = [w.replace("world'", 'world') for w in query2]
        queries.append(query2)

    return queries, freq

def queryTitle():
    names = []
    data = et.parse('topics.xml')
    d = data.getroot()
    
    for i in range(0, 10):
        query = (d[i][0].text)
        query.lower()
        query1 = query.splitlines()
        names.append(query1)
        
    return names    

# Function that returns a dictionary of term and its frequency in a query
def queryFrequency(query):
    queryFreq = {}
    for term in query:
        if term in queryFreq.keys():
            queryFreq[term] += 1
        else:
            queryFreq[term] = 1
    return queryFreq[term]

# Function to calculate average length of all the documents in the corpus
def calculateAverageLength(fileLengths):
    avgLength = 0
    
    for file in fileLengths.keys():
        avgLength += fileLengths[file]
    
    return (avgLength/3495)

# Function to calculate BM25 score
def calculateBM25(index, w, name, fLen, avgLen, df, tdf, freq):
    
    K = 1.2 * ((1 - 0.75) + (0.75 * ((fLen[name])/avgLen)))
    score = (log((3495 + 0.5)/(df + 0.5)) * ((2.2 * tdf) / (K + tdf)) * (((1 + 100) * (freq[w])) / (100 + freq[w])))
    
    return score 

# Function to score the documents based on the given query
def findDocumentsForQuery(query, invertedIndex, fileLengths):
    queryFreq = queryFrequency(query)
    
    avdl = calculateAverageLength(fileLengths)
    
    BM25ScoreList = {}
    
    for term in query:
        if term in invertedIndex.keys():
            qf = queryFreq[term]
            docDict = invertedIndex[term]
            
            for doc in docDict:
                n = len(docDict)
                f = docDict[doc]
                dl = fileLengths[doc]
                
                BM25 = calculateBM25(n, f, qf, r, N, dl, avdl)
                
                if doc in BM25ScoreList.keys():
                    BM25ScoreList[doc] += BM25
                
                else:
                    BM25ScoreList[doc] = BM25
    
    return BM25ScoreList

# Function to write top 100 ranked documents for each query 
def writeToFile(queries, invertedIndex, fileLengths):
    queryID = 1
    
    queryNames = queryTitle()
    
    for query in queries:
        BM25ScoreList = findDocumentsForQuery(query, invertedIndex, fileLengths)
        print(BM25ScoreList)
        sortedScoreList = sorted(BM25ScoreList.items(), key=lambda x:x[0], reverse=True)
        
        if not os.path.exists(BM_25_SCORE_LIST):
            os.makedirs(BM_25_SCORE_LIST)
        
        file = open( BM_25_SCORE_LIST + "/BM_25_SCORE_LIST_" + str(queryNames[queryID-1]) + ".txt", "w")
        
        for rank in range(0, 10):
            data = et.parse('topics.xml')
            d = data.getroot()
            
            queryID = d[rank].get('number')
            
            text = str(queryID) +  "   " + "0" +  "   " + str(sortedScoreList[rank][0]) + "   " + str(rank+1) +  "   " + str(sortedScoreList[rank][1]) +  "   " + "BM25" +"\n"
            file.write(text)
        
        queryID += 1

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("How to use? Write according to this:\n python file_name.py directory_name/path")
        
    else:
        print(sys.argv[1])
        res, term_map, fLen = process_files(sys.argv[1])
        hashmap = make_hashmap_of_hashmap(res)
        index = final_indexing(hashmap)
        
        queries, freq = queryParser()
        
        with open("index.txt", "r") as ch:
            data = [line.rstrip() for line in ch.readlines()]

        #print(data)

        name_dict = {}
        with open("fileLen.txt", "r", encoding="utf-8") as f:
            for line in f:
                (key, val) = line.split(':')
                name_dict[key] = int(val)
        
        my_list = []
        for d in data:
            name = d.split(' ')
            #print(name)
            my_list.append(name)
            
        avgLen = calculateAverageLength(name_dict)
        
        BM25ScoreList = {}
        tdf = []
        for words in queries:
            score = 0
            #df = (len(my_list[index]))
            #print(df)
            for w in words:
                #k = (my_list[index][j])
                #print(name_dict[k]) #this gives the file len
                #print(k) #this gives the name of files
                for name in name_dict.keys():
                #result = index[w].get(name, "Not Found!")

                #if result != "Not Found!":
                    tdf.append(len(index[w][name]))

                # score = calculateBM25(index, w, name, fLen, avgLen, df, tdf, freq)
                    #if name in BM25ScoreList.keys():
                    #   BM25ScoreList[name] += score

                    #else:
                    #   BM25ScoreList[name] = score
        print(tdf)
            #sortedScoreList = (sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True))    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # my = []
        # with open("index.txt", "r") as ch:
        #     #for words in queries:
        #     for line in ch:
        #         my.append(line.strip())

        # x = [m.strip('\"dict_keys()') for m in my]
        # t = ([y.strip('\"\[\]') for y in x])

        # for i in t:
        #     print(i, end=",")
        
        # name = {}    
        # s = ''      
        # with open("index1.txt", "r") as ch:            
        #     for line in ch:
        #         items = line.split()
        #         key, values = items[0], items[1:]
        #         val = [i for i in values]
        #         name[key] = val
                  
        #         for k in name[key]:
        #             #print(k)
        #             my = json.loads(json.dumps(k))
        #             #print(my)
        #             for n in my:
        #                 s +=''.join(n)
            #print(s)      
                #print([name[0] for name in items[1:]])
                #my_dict[key] = values
            #print(my_dict.values())
                
        # d = {}
        # with open("fileLen.txt", "r", encoding="utf-8") as f:
        #     for line in f:
        #         (key, val) = line.split(':')
        #         d[key] = int(val)
        
        # temp_dict = {}
        # for name, val in my_dict.items():
        #     #for w in dict(words).keys():
        #     v = [name.split() for name in val]
        #     v1 = [s.strip("{") for i in range(len(v)) for s in v[i]]
        #     temp_dict[name] = v1
        
        # for v in my_dict.values():
        #     print(v)
    
        #print(d)
        #avglen = 0
        # for key, value in my_dict.items():
        #     for k in value:
        #         for name in k.keys():
        #             print(name)
                 #for fname, pos in values.items():
            #name = ((values))
            # n = name.replace(':', '')
            # n1 = (n.strip('"'))
            # n2 = (n1.strip("'"))
            #avglen += (d[n2])
            #print(name)
            # for dic in values:
            #     for key in dic:
            #         print(dic[int(key)].replace("{", ''))                           
        #file = "termids.txt"
        
        #queryNames = queryTitle()
                           