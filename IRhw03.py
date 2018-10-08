import json
import nltk
import numpy
import re

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

# 读取文本并进行处理
path = '/Users/apple/Desktop/ir/hw3/tweets.txt'
file = open(path,'r',encoding='UTF-8',errors='ignore')
tweets = []
twords = {}
counts = 0
for line in file:
    tweets.append(json.loads(line))
    tweets[counts]['text'] = tweets[counts]['text'].lower()
    tweets[counts]['text'] = cutsyms(tweets[counts]['text'])
    #tweets[counts]['text'] = cutstopwords(tweets[counts]['text'])
    #tweets[counts]['text'] = stemming(tweets[counts]['text'])
    for seg in tweets[counts]['text'].split(' '):
        if seg in twords:
            length = len(twords[seg])
            if twords[seg][length-1]!=counts:
                twords[seg].append(counts)
                twords[seg][0] = twords[seg][0] + 1
        else:
            twords[seg] = []
            twords[seg].append(1)
            twords[seg].append(counts)
    counts = counts + 1
    print(counts)
file.close()

def fAnd(listA,listB):
    list = []
    la = len(listA)
    lb = len(listB)
    ca = 1
    cb = 1
    while (ca!=la)&(cb!=lb):
        if (listA[ca]==listB[cb]):
            list.append(listA[ca])
            ca = ca + 1
            cb = cb + 1
        else:
            if listA[ca]>listB[cb]:
                cb = cb + 1
            else:
                ca = ca + 1
        if (ca==la):
            if (listA[ca-1]<listB[cb]):
                break
        if (cb==lb):
            if (listB[cb-1]<listA[ca]):
                break
    return list

def fOr(listA,listB):
    list = []
    la = len(listA)
    lb = len(listB)
    ca = 1
    cb = 1
    while (ca!=la)&(cb!=lb):
        if (listA[ca]==listB[cb]):
            list.append(listA[ca])
            ca = ca + 1
            cb = cb + 1
        else:
            if listA[ca]>listB[cb]:
                list.append(listB[cb])
                cb = cb + 1
            else:
                list.append(listA[ca])
                ca = ca + 1
        if (ca==la):
            if (listA[ca-1]<listB[cb]):
                for i in range(cb,lb):
                    list.append(listB[i])
                break
        if (cb==lb):
            if (listB[cb-1]<listA[ca]):
                for i in range(ca,la):
                    list.append(listA[i])
                break
    return list

def fNot(listA):
    la = len(listA)
    list = []
    ca = 1
    global counts
    for i in range(counts):
        if ca<la:
            if listA[ca] > i:
                list.append(i)
            else:
                if listA[ca] < i:
                    ca = ca + 1
    return list

# 使用函数实现简单的二元关系的检索
test = 'home OR circle'
test = cutsyms(test)
tlist = test.split(' ')
print(tlist[1])

if tlist[1]=='AND':
    print(fAnd(twords[tlist[0]],twords[tlist[2]]))
if tlist[1]=='OR':
    print(fOr(twords[tlist[0]],twords[tlist[2]]))
if tlist[1]=='NOT':
    print(fNot(twords[tlist[0]]))



