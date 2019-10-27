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
from rank_bm25 import BM25Okapi

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
from math import log10
import xml.etree.ElementTree as et

id = []
# Function to parse the queries
def queryParser():
    queries = []
    freq = {}
    data = et.parse('topics.xml')
    d = data.getroot()
    query2 = []
    
    for i in range(0, 10):
        query = (d[i][0].text)
        id.append(d[i].get('number'))
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
        
        query3 = [w.replace("world'", 'world') for w in query2]
        
        for word in query3:
            freq[word] = queryFrequency(query3) #it is the tf(q, i) according to formula
        
        queries.append(query3)

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
def calculateBM25(w, name, fLen, avgLen, df, tdf, freq):
    
    K = 1.2 * ((1 - 0.75) + (0.75 * ((fLen[name])/avgLen)))
    score = (log10((3495 + 0.5)/(df + 0.5)) * ((2.2 * tdf) / (K + tdf)) * (((1 + 1000) * (freq[w])) / (1000 + freq[w])))
    
    return score
    # l = fLen[name]
    # K = 1.2 * (0.25 + (0.75 * (l/avgLen)))
    # df1 = df + 0.5
    # t = 3495.5/df1
    
    # score1 = log(t)
    
    # score2 = ((2.2 * tdf) / (K + tdf))
    
    # score3 = ((101 * freq[w]) / (100 + freq[w]))
    
    #return score 

if __name__=="__main__":
    
    queries, freq = queryParser()
    
    with open("index.txt", "r") as ch:
        data = [line.rstrip() for line in ch.readlines()]

    name_dict = {}
    with open("fileLen.txt", "r", encoding="utf-8") as f:
        for line in f:
            (key, val) = line.split(':')
            name_dict[key] = int(val)
    
    my_list = []
    for d in data:
        name = d.split(' ')
        my_list.append(name)
        
    avgLen = calculateAverageLength(name_dict)
    
    with open("postingsFile.txt", "r") as pf:
        tdf = [int(p) for p in pf.readlines()]
    
    BM25ScoreList = {}
    count = 0
    index = 0
    for words in queries:
        score = 0
        df = (len(my_list[index]))
        index += 1
        for w in words:
            for name in name_dict.keys():
                if count < 22034:
                    pos = tdf[count]
                    score = calculateBM25(w, name, name_dict, avgLen, df, pos, freq)
                    count += 1
                    if name in BM25ScoreList.keys():
                        BM25ScoreList[name] += score

                    else:
                        BM25ScoreList[name] = score
    
            sortedScoreList = (sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True))
            
            if index < 10:
                with open("output.txt", "a") as out:
                    rank = 1
                    for tup in sortedScoreList:
                        out.write(str(id[index]) + "\t" + "0"+ "\t" + str(tup) + "\t\t\t" + str(rank) + "\t" + "BM25" + "\n")
                        rank += 1