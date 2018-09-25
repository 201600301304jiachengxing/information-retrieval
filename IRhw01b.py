import os
import chardet
import re
import nltk
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
    new_str = re.sub('[1234567890,.\'\"\t\n*_+=?/|!@#$%^&*()`~<>:;\-\[\]]'," ",str)
    return new_str

# 词干提取
def stemming(str):
    s = nltk.stem.SnowballStemmer('english')
    segs = str.replace('\n', '').lower().split(' ')
    new_str = ''
    for seg in segs:
        new_str = new_str + " " + s.stem(seg)
    return new_str

# 读取文本
def readtxt(path):
    global num_txt
    global num_dict
    num_dict = {}
    num_txt = 0
    all_context = ""
    for dirName, subdirList, fileList in os.walk(path):
        fileList.remove(fileList[0])
        for fname in fileList:
            fname = os.path.join(dirName, fname)
            f = open(fname, 'rb')
            data = f.read()
            f.close()

            print(chardet.detect(data))
            print(fname)

            fname = open(fname,'r+',encoding=chardet.detect(data)['encoding'])
            str = fname.read()
            str = cutsyms(str)
            str = cutstopwords(str)
            str = stemming(str)

            strl_ist = str.replace('\n', '').lower().split(' ')
            for seg in strl_ist:
                if seg in num_dict.keys():
                    num_dict[seg] = num_dict[seg] + 1
                else:
                    num_dict[seg] = 1

            all_context = all_context + "\n" + str
            num_txt = num_txt + 1
            fname.close()
    return all_context

# 统计词出现次数
def wordcount(str):
    strl_ist = str.replace('\n','').lower().split(' ')
    count_dict = {}
    for str in strl_ist:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    # count_list=sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
    count_dict.pop('')
    return count_dict

#全部文本读取
num_txt = 0
num_dict = {}
context = readtxt("/Users/apple/Desktop/ir/news")
#context = readtxt("/Users/apple/Desktop/ir/alltxt")

#全部文档记数
str_dict = wordcount(context)
new_dict = str_dict
str_dict = {}
for seg in new_dict:
    if (new_dict[seg] > 10) & (new_dict[seg] < 1000):
        str_dict[seg] = new_dict[seg]
length = len(str_dict)
print(length)

#数据存储
full_path = '/Users/apple/Desktop/ir/altext01.txt'
file = open(full_path,'a+')
file.write(context)
file.close()

# VSM build
for dirName, subdirList, fileList in os.walk('/Users/apple/Desktop/ir/news'):
    fileList.remove(fileList[0])
    for fname in fileList:
        fname = os.path.join(dirName, fname)
        f = open(fname, 'rb')
        data = f.read()
        f.close()

        print(chardet.detect(data))
        print(fname)

        fname = open(fname, 'r+', encoding=chardet.detect(data)['encoding'])
        ins_str = fname.read()
        fname.close()

        ins_dict = {}
        ins_str = cutsyms(ins_str)
        ins_str = cutstopwords(ins_str)
        ins_str = stemming(ins_str)
        ins_dict = wordcount(ins_str)

        # tf_idf
        sum = 0
        outstr = ""
        for seg in ins_dict.keys():
            sum = sum + ins_dict[seg]
        for seg in ins_dict.keys():
            tf = ins_dict[seg] / sum
            if seg in  str_dict.keys():
                idf = math.log(num_txt / num_dict[seg])
            else:
                idf = 0
            ins_dict[seg] = tf * idf
            if ins_dict[seg]!=0:
                outstr = outstr + seg + ":" + str(ins_dict[seg]) + " "

        full_path = '/Users/apple/Desktop/ir/vsmresult01.txt'
        file = open(full_path, 'a+')
        file.write(outstr+"\n\n")
        file.close()



