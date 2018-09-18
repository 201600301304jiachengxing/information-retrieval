import jieba
import jieba.analyse
import numpy as np
# import json
import re

def Textrank(content):
    result = re.sub(r'[^\u4e00-\u9fa5]', "", content)
    seg = jieba.cut(result)
    jieba.analyse.set_stop_words('stopwords.txt')
    keyList = jieba.analyse.textrank('|'.join(seg), topK=10, withWeight=False)
    return keyList


def TF_IDF(content):
    result = re.sub(r'[^\u4e00-\u9fa5]', "", content)
    seg = jieba.cut(result)
    jieba.analyse.set_stop_words('stopwords.txt')
    keyWord = jieba.analyse.extract_tags(
        '|'.join(seg), topK=10, withWeight=False, allowPOS=())  # 关键词提取，在这里对jieba的tfidf.py进行了修改
    return keyWord

#A = "我们一起去加州旅行";
#print(Textrank(A))
#print(TF_IDF(A))

import os
import jieba

# 去除停用词
def cutstopwords(str):


# 读取文本
def readtxt(path):
    context = ""
    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:
            fname = os.path.join(dirName, fname)
            fname = open(fname,'r')
            context = context + " " + fname.read()
            fname.close()
    return context

# 统计词出现次数
def wordcount(str):
    strl_ist = str.replace('\n','').lower().split(' ')
    count_dict = {}
    for str in strl_ist:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    count_list=sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
    return count_list

context="""The US media reports suggest Robert Mueller's inquiry has taken the first step towards possible criminal charges.
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
#context = readtxt("/Users/apple/Desktop/ir/news")
print(wordcount(context))
