import json
import nltk
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
            twords[seg].append(counts+1)
    counts = counts + 1
    print(counts)
file.close()

def fAnd(listA,listB):
    list = []
    la = len(listA)
    lb = len(listB)
    ca = 0
    cb = 0
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
    return list

def fOr(listA,listB):
    list = []
    la = len(listA)
    lb = len(listB)
    ca = 0
    cb = 0
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
        if (ca==la)&(cb<lb):
            for i in range(cb, lb):
                list.append(listB[i])
            break
        if (cb==lb)&(ca<la):
            for i in range(ca, la):
                list.append(listA[i])
            break
    return list

def fNot(listA):
    la = len(listA)
    list = []
    ca = 0
    global counts
    for i in range(counts):
        if ca<la:
            if listA[ca] > i:
                list.append(i)
            else:
                if listA[ca] < i:
                    ca = ca + 1
    return list

print(twords.keys())

# 使用函数实现简单的多元关系的检索
test = 'NOT home AND house OR circle'
test = cutsyms(test)
tlist = test.split(' ')
tcount = {}
tlen = len(tlist)

for i in range(tlen):
    if tlist[i] == 'AND':
        tcount[i+1] = twords[tlist[i+1]]
        tcount[i+1] = fAnd(tcount[i-1], tcount[i+1])
    elif tlist[i] == 'OR':
        tcount[i+1] = twords[tlist[i+1]]
        tcount[i+1] = fOr(tcount[i-1], tcount[i+1])
    elif tlist[i] == 'NOT':
        tcount[i+1] = twords[tlist[i+1]]
        tcount[i+1] = fNot(tcount[i+1])
    elif i not in tcount.keys():
        tcount[i] = twords[tlist[i]]

print(tcount[tlen-1])

# 使用函数实现一定程度的多元关系的检索，先处理not，后处理and，最后处理or
test = 'NOT home AND house AND NOT sarge OR NOT circle AND unlikely AND NOT recall'
test = cutsyms(test)
tlist = test.split(' ')
tcount = {}

i=0
while i<len(tlist):
    if (tlist[i]!='NOT')&(tlist[i]!='AND')&(tlist[i]!='OR'):
        tcount[tlist[i]] = twords[tlist[i]][1:len(twords[tlist[i]])]
    i=i+1

i=0
while i<len(tlist):
    if tlist[i] == 'NOT':
        tcount[tlist[i+1]] = fNot(tcount[tlist[i+1]])
        tlist.remove(tlist[i])
        i=i-1
    i=i+1
print(tlist)

i=0
while i<len(tlist):
    if tlist[i] == 'AND':
        tcount[tlist[i+1]] = fAnd(tcount[tlist[i-1]],tcount[tlist[i+1]])
        tlist.remove(tlist[i])
        tlist.remove(tlist[i-1])
        i=i-1
    i=i+1
print(tlist)

i=0
while i<len(tlist):
    if tlist[i] == 'OR':
        tcount[tlist[i+1]] = fOr(tcount[tlist[i-1]],tcount[tlist[i+1]])
        tlist.remove(tlist[i])
        tlist.remove(tlist[i-1])
        i=i-1
    i=i+1
print(tlist)

print(tcount[tlist[len(tlist)-1]]) #result=[1, 52]
