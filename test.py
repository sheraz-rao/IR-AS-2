import xml.etree.ElementTree as et
from nltk import PorterStemmer
from nltk.tokenize import word_tokenize

queries = []
data = et.parse('topics.xml')
d = data.getroot()

for i in range(0, 10):
    # query = (d[i][0].text)
    # query.lower()
    # query1 = query.split()
    
    # huge_list = []

    # with open("stoplist.txt", "r") as f:
    #     huge_list = f.read().split()

    # for w in query1: 
    #     if w in huge_list:
    #         #print(query1)        
    #         query1.remove(w)
            
    # query2 = [PorterStemmer().stem(s) for s in query1]
    # print(query2)
    # query2 = [w.replace("world'", 'world') for w in query2]
    # queries.append(query2)
    
    query = d[i].get('number')
    print(query)        
    
    
    
    """
        avgLen = calculateAverageLength(fLen)
        
        score = 0
        #queryID = 1
        
        BM25ScoreList = {}
        
        for word in queries:
            #print(word)
            score = 0
            for w in word:
                #print(index[w])
                df = (len(index[w]))
                
                for name in fLen.keys():
                    result = index[w].get(name, "Not Found!")

                    if result != "Not Found!":
                        tdf = len(index[w][name])
                        
                        score = calculateBM25(index, w, name, fLen, avgLen, df, tdf, freq)
                        #print(w + "\t\t" + name + "\t\t" + str(score))
                        if name in BM25ScoreList.keys():
                            BM25ScoreList[name] += score
                
                        else:
                            BM25ScoreList[name] = score

            sortedScoreList = (sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True))
            """
            # if not os.path.exists(BM_25_SCORE_LIST):
            #     os.makedirs(BM_25_SCORE_LIST)
        
            # file = open( BM_25_SCORE_LIST + "/BM_25_SCORE_LIST_" + str(queryNames[queryID-1]) + ".txt", "w")
            
            # for rank in range(0, 10):
            #     data = et.parse('topics.xml')
            #     d = data.getroot()
                
            #     ID = d[rank].get('number')
            #     temp = (sortedScoreList)
            #     text = str(ID) +  "   " + "0" +  "   " + str(temp[0]) + "\t\t" + str(temp[1]) + "\t\t" + str(rank+1) + " BM25" +"\n"
            #     file.write(text)
            #     i += 1
            
            # queryID += 1
        
    
        #print(sortedScoreList) 
        
        
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