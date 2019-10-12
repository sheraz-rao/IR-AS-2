import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
import sys

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
                    
        print("stop wording...\n")           
        stop = [w for w in tokens if w not in sp]
        stopwords.close()
        
        print("stemming...\n")                
        stemm = [PorterStemmer().stem(s) for s in stop]
        
        mapping[file] = stemm
          
        pos = 1
        for token in stemm:
            if  token not in term_map:
                term_map[token] = term_id
                terms.append(str(term_id) + '\t' + token) #it will be write to the file
                term_id += 1
            doc_term_positions.append((doc_id, term_map[token], pos))
            pos += 1
         
        #get file name from path and this info  will be written to the .txt file
        docs.append((str(doc_id) + '\t' + file))
        doc_id += 1

    print("File pre processed.... returning:\n")
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
    data = et.parse('topics.xml')
    d = data.getroot()
    
    for i in range(0, 10):
        query = (d[i][0].text)
        query.lower()
        query1 = query.split()
        stopwords = open('stoplist.txt', 'r')
    
        filtered_sentence = [] 
        
        for w in query1: 
            if w not in stopwords: 
                filtered_sentence.append(w)
        stopwords.close()            
        query2 = [PorterStemmer().stem(s) for s in filtered_sentence]
        queries.append(query2)
    
    return queries

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
    return queryFreq

# Function to calculate average length of all the documents in the corpus
def calculateAverageLength(fileLengths):
    avgLength = 0
    for file in fileLengths.keys():
        avgLength += fileLengths[file]
    return avgLength/N

# Function to calculate BM25 score
def calculateBM25(n, f, qf, r, N, dl, avdl):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    Q1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    Q2 = ((k1 + 1) * f) / (K + f)
    Q3 = ((k2 + 1) * qf) / (k2 + qf)
    return Q1 * Q2 * Q3

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
        sortedScoreList = sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True)
        
        if not os.path.exists(BM_25_SCORE_LIST):
            os.makedirs(BM_25_SCORE_LIST)
        
        file = open( BM_25_SCORE_LIST + "/BM_25_SCORE_LIST_" + str(queryNames[queryID-1]) + ".txt", "w")
        
        for rank in range(100):
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
    
        # query = input("\nEnter Word to Search: ")
        # #print(query)
        
        # query1 = PorterStemmer().stem(query)
        # res = (term_map.get(query1, "Not Found!"))
        # #print(res)
        
        # file = "term_info.txt"
        
        # f =  linecache.getline(file, res)
        # print("TermID, offset, t_pos, docs_count")
        # print((f))
        
        queries = queryParser()
        writeToFile(queries, index, fLen)