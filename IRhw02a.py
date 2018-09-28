import os
import chardet
import re
import nltk
import numpy

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
    global class_dict
    global class_num
    global class_list
    global num_txt
    global num_dict
    num_dict = {}
    num_txt = 0
    all_context = ""
    for dirName, subdirList, fileList in os.walk(path):
        fileList.remove(fileList[0])
        for fname in fileList:
            class_name = dirName.split('/')[6]
            num = class_list[class_name]
            class_num[num] = class_num[num] + 1

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

            str_list = str.replace('\n', '').lower().split(' ')
            for seg in str_list:
                if seg in num_dict.keys():
                    num_dict[seg] = num_dict[seg] + 1
                else:
                    num_dict[seg] = 1

            for seg in str_list:
                if seg in class_dict[class_name].keys():
                    class_dict[class_name].update({seg:class_dict[class_name][seg] + 1})
                else:
                    class_dict[class_name].update({seg:1})

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
class_list = {'alt.atheism':0,'comp.graphics':1,'comp.os.ms-windows.misc':2,'comp.sys.ibm.pc.hardware':3,'comp.sys.mac.hardware':4,'comp.windows.x':5,'misc.forsale':6,'rec.autos':7,'rec.motorcycles':8,'rec.sport.baseball':9,'rec.sport.hockey':10,'sci.crypt':11,'sci.electronics':12,'sci.med':13,'sci.space':14,'soc.religion.christian':15,'talk.politics.guns':16,'talk.politics.mideast':17,'talk.politics.misc':18,'talk.religion.misc':19}
class_num = [0]*20
class_dict = {'alt.atheism':{},'comp.graphics':{},'comp.os.ms-windows.misc':{},'comp.sys.ibm.pc.hardware':{},'comp.sys.mac.hardware':{},'comp.windows.x':{},'misc.forsale':{},'rec.autos':{},'rec.motorcycles':{},'rec.sport.baseball':{},'rec.sport.hockey':{},'sci.crypt':{},'sci.electronics':{},'sci.med':{},'sci.space':{},'soc.religion.christian':{},'talk.politics.guns':{},'talk.politics.mideast':{},'talk.politics.misc':{},'talk.religion.misc':{}}
context = readtxt("/Users/apple/Desktop/ir/train")

#全部文档记数，去除高频低频词
str_dict = wordcount(context)
new_dict = str_dict
str_dict = {}
for seg in new_dict:
    if (new_dict[seg] > 5) & (new_dict[seg] < 1500):
        str_dict[seg] = new_dict[seg]
length = len(str_dict)
print(length)

for i in class_list.keys():
    z_num = class_list[i]
    newc_dict = {}
    for seg in str_dict:
        if seg in class_dict[i].keys():
            newc_dict[seg] = class_dict[i][seg]
    class_dict[i] = newc_dict

class_sum = [0]*20
for i in class_list.keys():
    x_num = class_list[i]
    for j in class_dict[i].keys():
        class_sum[x_num] = class_sum[x_num] + class_dict[i][j]

#classification
classification = [[0 for x in range(20)]for y in range(20)]
for dirName, subdirList, fileList in os.walk('/Users/apple/Desktop/ir/test'):
    fileList.remove(fileList[0])
    for fname in fileList:
        name = dirName.split('/')[6]
        num = class_list[name]
        print(name)

        fname = os.path.join(dirName, fname)
        f = open(fname, 'rb')
        data = f.read()
        f.close()

        fname = open(fname, 'r+', encoding=chardet.detect(data)['encoding'])
        ins_str = fname.read()
        fname.close()

        ins_dict = {}
        ins_str = cutsyms(ins_str)
        ins_str = cutstopwords(ins_str)
        ins_str = stemming(ins_str)
        ins_dict = wordcount(ins_str)

        class_pro = [1]*20
        for i in class_list.keys():
            y_num = class_list[i]
            for seg in ins_dict.keys():
                if seg in class_dict[i].keys():
                    class_pro[y_num] = class_pro[y_num] * ((class_dict[i][seg]+1)/(class_sum[y_num]+200)) * ((class_num[y_num])/(5000))
                else:
                    class_pro[y_num] = class_pro[y_num] * ((1)/(class_sum[y_num]+200)) * ((class_num[y_num])/(5000))

        index = numpy.argmax(class_pro)
        classification[num][index] = classification[num][index] + 1

print(classification)













