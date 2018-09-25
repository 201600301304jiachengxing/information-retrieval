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
print(str_dict)
length = len(num_dict)
print(length)

#数据存储
full_path = '/Users/apple/Desktop/ir/altext.txt'
file = open(full_path,'a+')
file.write(context)
file.close()


ins_str = """From: kempmp@phoenix.oulu.fi (Petri Pihko)
Subject: Re: Christian Morality is

Dan Schaertel,,, (dps@nasa.kodak.com) wrote:

> Let us go back , oh say 1000 years or so, whatever.  Pretend someone says to you
> someday there will be men on the moon.  (Now remember, you still think the
> world is flat).  This is quite an extraordinary claim.

I think C.S. Lewis has argued that medieval people did not all think the
world is flat.

However, this argument goes both ways. Pretend someone telling Plato that
it is highly probable that people do not really have souls; their minds
and their consciousness are just something their brains make up, and
their brains (their body) is actually ahead of their mind even in 
voluntarly actions. I don't think Plato would have been happy with this,
and neither would Paul, although Paul's ideas were quite different.
However, if you would _read_ what we discuss in this group, and not
just preach, you would see that there currently is much evidence in
favour of these statements.

The same applies to the theory of natural selection, or other sacred
cows of Christianity on our origins and human nature. I don't believe
in spirits, devils or immortal souls any more than in gods.

> The fact is we can argue the existence of God until the end of time, there really is no
> way to either prove or disprove it, but there will be a time when we all know the truth.  
> I hope and believe I'm right and I hope and pray that you find your way too. 

Ah, you said it. You believe what you want to. This is what I had assumed
all along. 

> OK maybe I shouldn't have said "no way".   I guess I really believe there is
> a way.  But all I can do is plant seeds.  Either they grow or they don't. 

You might be as well planting Satan's seeds, ever thought of this?
Besides, you haven't yet explained why we must believe so blindly,
without any guiding light at all (at least I haven't noticed it).
I don't think this is at all fair play on god's part. 

Your argument sounds like a version of Pascal's Wager. Please read the
FAQ, this fallacy is discussed there.

> But
> they won't if they're not planted.  The Holy Spirit is the nurishment that
> helps them grow and that comes from God.

And I failed to get help from the HS because I had a wrong attitude?
Sorry, Dan, but I do not think this spirit exists. People who claim to have
access to it just look badly deluded, not gifted. 

Petri


--
 ___. .'*''.*        Petri Pihko    kem-pmp@          Mathematics is the Truth.
!___.'* '.'*' ' .    Pihatie 15 C    finou.oulu.fi    Physics is the Rule of
       ' *' .* '*    SF-90650 OULU  kempmp@           the Game.
          *'  *  .*  FINLAND         phoenix.oulu.fi  -> Chemistry is The Game."""

ins_dict = {}
ins_str = cutsyms(ins_str)
ins_str = cutstopwords(ins_str)
ins_str = stemming(ins_str)
ins_dict = wordcount(ins_str)
print(ins_dict)

#for items in str_dict.keys():
#    if items not in ins_str.keys():
#        ins_dict[items] = 0
#    else:
#        ins_dict[items] = ins_str[items]

#tf_idf
sum = 0
for seg in ins_dict.keys():
    sum = sum + ins_dict[seg]
for seg in ins_dict.keys():
    tf = ins_dict[seg]/sum
    idf = math.log(num_txt/num_dict[seg])
    ins_dict[seg] = tf*idf

print(ins_dict)

