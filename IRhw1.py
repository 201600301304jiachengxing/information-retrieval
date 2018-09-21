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
    new_str = re.sub('[,.''""?/{}()=+_<>!`~@#$%^&*]'," ",str)
    return new_str

# 词干提取
def stemming(str):
    s = nltk.stem.SnowballStemmer('english')
    segs = str.replace('\n', '').lower().split(' ')
    new_str = ''
    for seg in segs:
        new_str = new_str + " " + s.stem(seg)
    return new_str

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
    # count_dict.remove(count_list[0])
    return count_dict

# 读取文本
def readtxt(path):
    global num_txt;
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
            all_context = all_context + "\n" + str
            num_txt = num_txt + 1
            fname.close()
    return all_context


#全部文本读取
context = readtxt("/Users/apple/Desktop/ir/news")
num_txt = 0
num_dict = {}

#预处理
context = re.sub('[,.''""?/{}()=+_<>!`~@#$%^&*]'," ",context)
context = cutstopwords(context)
context = stemming(context)

#数据存储
full_path = '/Users/apple/Desktop/ir/news/text.txt'
file = open(full_path,'a+')
file.write(context)
file.close()

context = wordcount(context)

#词频等信息记录
for items in context.keys():
    if items not in num_dict:
        num_dict[items] = 1
    else:
        num_dict[items] = num_dict[items] + 1


#样例文本测试，如需计算全部文本的词向量可树形遍历文件
ins_context="""The US media reports suggest Robert Mueller's inquiry has taken the first step towards possible criminal charges.
According to Reuters news agency, the jury has issued subpoenas over a June 2016 meeting between President Donald Trump's son and a Russian lawyer.
The president has poured scorn on any suggestion his team colluded with the Kremlin to beat Hillary Clinton.
In the US, grand juries are set up to consider whether evidence in any case is strong enough to issue indictments for a criminal trial. They do not decide the innocence or guilt of a potential defendant.
The panel of ordinary citizens also allows a prosecutor to issue subpoenas, a legal writ, to obtain documents or compel witness testimony under oath.
Trump: US-Russia relations are at 'dangerous low'
The Trump-Russia saga in 200 words
Russia: The 'cloud' over the White House
Now it's deadly serious
Anthony Zurcher, BBC North America reporter
Robert Mueller's special counsel investigation has always been a concern for the Trump administration. Now it's deadly serious business.
With the news that a grand jury has been convened in Washington DC, and that it is looking into the June 2016 meeting between Donald Trump Jr and Russian nationals, it's clear the investigation is focusing on the president's inner circle.
This news shouldn't come as a huge shock, given that Mr Mueller has been staffing up with veteran criminal prosecutors and investigators. It is, however, a necessary step that could eventually lead to criminal indictments. At the very least it's a sign that Mr Mueller could be on the trail of something big - expanding the scope beyond former National Security Adviser Michael Flynn and his questionable lobbying. It also indicates his investigation is not going to go away anytime soon.
In the past, when big news about the Russia investigation has been revealed, Mr Trump has escalated his rhetoric and taken dead aim at his perceived adversaries. The pressure is being applied to the president. How will he respond?
At a rally in Huntington, West Virginia, on Thursday evening, Mr Trump said the allegations were a "hoax" that were "demeaning to our country".
"The Russia story is a total fabrication," he said. "It's just an excuse for the greatest loss in the history of American politics, that's all it is."
The crowd went wild as he continued: "What the prosecutor should be looking at are Hillary Clinton's 33,000 deleted emails."
"Most people know there were no Russians in our campaign," he added. "There never were. We didn't win because of Russia, we won because of you, that I can tell you."
Mr Trump's high-powered legal team fielding questions on the Russia inquiry said there was no reason to believe the president himself is under investigation.
Ty Cobb, a lawyer appointed last month as White House special counsel, said in a statement: "The White House favours anything that accelerates the conclusion of his work fairly.
"The White House is committed to fully co-operating with Mr Mueller."
Earlier on Thursday, the US Senate introduced two separate cross-party bills designed to limit the Trump administration's ability to fire Mr Mueller.
The measures were submitted amid concern the president might dismiss Mr Mueller, as he fired former FBI director James Comey in May, citing the Russia inquiry in his decision."""

ins_d = {}
ins_context = re.sub('[,.''""?/{}()=+_<>!`~@#$%^&*]'," ",ins_context)
ins_context = cutstopwords(ins_context)
ins_context = stemming(ins_context)
ins_context = wordcount(ins_context)

for items in context.keys():
    if items not in ins_context.keys():
        ins_d[items] = 0
    else:
        ins_d[items] = context[items]

#tf_idf
sum = 0
for seg in ins_d.keys():
    sum = sum + ins_d[seg]
for seg in ins_d.keys():
    tf = ins_d[seg]/sum
    idf = math.log(num_txt/num_dict[seg])
    ins_d[seg] = tf*idf

print(ins_d)
