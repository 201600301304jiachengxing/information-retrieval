import json
import nltk
import re
import math

# 去除停用词
def cutstopwords(str):
    stopwords = {}.fromkeys([line.rstrip() for line in open('estopwords.txt')])
    segs = str.replace('\n','').lower().split(' ')
    new_str = ''
    for seg in segs:
        if seg not in stopwords:
            new_str = new_str + " " +seg
    return new_str

# 去除标点
def cutsyms(str):
    new_str = re.sub('[,.\'\"\t\n*_+=?/|!@#$%^&*()`~<>:;\-\[\]]'," ",str)
    return new_str

# 词干提取
def stemming(str):
    s = nltk.stem.SnowballStemmer('english')
    segs = str.replace('\n', '').lower().split(' ')
    new_str = ''
    for seg in segs:
        new_str = new_str + " " + s.stem(seg)
    return new_str

k=10
b=0.5

path = 'tweets.txt'
file = open(path,'r',encoding='UTF-8',errors='ignore')
tweets = []
twords = {}
tdocnum = {}
tdocword = [0]*40000
counts = 0
for line in file:
    tweets.append(json.loads(line))
    tweets[counts]['text'] = tweets[counts]['text'].lower()
    tweets[counts]['text'] = cutsyms(tweets[counts]['text'])
    tweets[counts]['text'] = cutstopwords(tweets[counts]['text'])
    tweets[counts]['text'] = stemming(tweets[counts]['text'])
    if counts not in tdocnum.keys():
        tdocnum[counts] = {}
    for seg in tweets[counts]['text'].split(' '):
        tdocword[counts] = tdocword[counts] + 1
        if seg in tdocnum[counts].keys():
            length = len(twords[seg])
            tdocnum[counts][seg] = tdocnum[counts][seg] + 1
            if twords[seg][length-1]!=counts:
                twords[seg].append(counts)
                twords[seg][0] = twords[seg][0] + 1
        else:
            tdocnum[counts].update({seg:1})
            twords[seg] = []
            twords[seg].append(1)
            twords[seg].append(counts+1)
    counts = counts + 1
    print(counts)
file.close()

sum = 0
avg = 0
for i in range(counts):
    sum = sum + tdocword[i]
avg = sum / counts

def qTest():
    # query
    path = '/Users/apple/Desktop/ir/hw3/topics.MB171-225.txt'
    file = open(path, 'r', encoding='UTF-8', errors='ignore')
    txt = file.read()
    file.close()
    txt.replace('\n', ' ')
    txtlist = txt.split(' ')
    numq=0;
    for i in range(len(txtlist)):
        if txtlist[i] == '</num>\n<query>':
            i = i + 1
            string = ""
            while txtlist[i] != '</query>\n<querytime>':
                string = string + txtlist[i] + " "
                i = i + 1

            numq = numq + 1
            string = string.lower()
            string = cutsyms(string)
            string = cutstopwords(string)
            string = stemming(string)
            print(string)

            [st1,st2]=rank(string,400)

            for j in range(400):
                outstr = str(numq + 170) + " " + tweets[st1[j][0]]['tweetId']
                full_path = 'result400bm25.txt'
                file = open(full_path, 'a+')
                file.write(outstr + "\n")
                file.close()

                outstr = str(numq + 170) + " " + tweets[st2[j][0]]['tweetId']
                full_path = 'result400pivo.txt'
                file = open(full_path, 'a+')
                file.write(outstr + "\n")
                file.close()

def rank(string,top):
    bm25 = {}
    pivoted = {}
    slist = string.lower().split(" ")
    for seg in slist:
        if seg != "":
            for w in range(counts):
                if w not in bm25.keys():
                    bm25[w] = 0
                    pivoted[w] = 0
                p = 0
                q = 0
                if seg in tdocnum[w].keys():
                    p = (math.log((counts + 1) / twords[seg][0])) * (k + 1) * (tdocnum[w][seg] / tdocword[w]) / ((tdocnum[w][seg] / tdocword[w]) + k * (1 - b + b * tdocword[w] / avg))
                    q = (math.log((counts + 1) / twords[seg][0])) * math.log(1 + math.log(1 + tdocnum[w][seg] / tdocword[w])) / (1 - b + b * tdocword[w] / avg)
                bm25[w] = bm25[w] + p
                pivoted[w] = pivoted[w] + q

    sk1 = sorted(bm25.items(), key=lambda x: x[1], reverse=True)
    sk2 = sorted(pivoted.items(), key=lambda x: x[1], reverse=True)
    return sk1[0:top],sk2[0:top]

qTest()