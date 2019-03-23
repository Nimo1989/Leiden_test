#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:36:06 2019

@author: nimo
"""

import requests
from bs4 import BeautifulSoup
import re
import enchant

d=enchant.Dict("en_US")

excludes = ['the','and','to','of','i','a','in','it','that','is',
            'you','my','with','not','his','this','but','for',
            'me','s','he','be','as','so','him','your', 'viii']
def getText():    
    txt=open('3.txt','r').read()    
    txt=txt.lower()    
    for ch in "·°!~@#$%^&*()_-+=<>?/,.:;{}[]|\'\"\\":    
        txt=txt.replace(ch,' ')       
    return txt    

hamletTxt=getText()    
words= re.findall(r'([a-zA-Z]+)',hamletTxt,re.MULTILINE)    

# words=hamletTxt.split()

counts={}    
sumcount = 0  
for word in words:  
    if len(word)>2:
            if d.check(word)==True:        
                counts[word]=counts.get(word,0)+1  
                sumcount = sumcount + 1 

counts_ex = counts.copy()    
for key in counts.keys():
    if key in excludes:
        counts_ex.pop(key)
items=list(counts_ex.items())    
items.sort(key=lambda x:x[1],reverse=True)    
for i in range(len(items)):    
    word,count=items[i]    
    print('{0:<10}{1:>5}'.format(word,count))    

 #将统计结果写入文本文件中    
outfile = open('frequence.txt', "w")    
lines = []      
lines.append('单词种类：'+str(len(items))+'\n')    
lines.append('单词总数：'+str(sumcount)+'\n')    
lines.append('词频排序如下:\n')    
lines.append('word\tcounts\n')    

outfile2= open('vocabulary.txt',"w")
line=[]
line.append('word\n')

s= ''   
w= '' 
for i in range(0,len(items)):    
    s = '\t'.join([str(items[i][0]), str(items[i][1])])    
    s += '\n'     
    w = str(items[i][0])
    w +='\n'
    lines.append(s)   
    line.append(w)
print('\n统计完成！\n')    
outfile.writelines(lines)    
outfile.close()
outfile2.writelines(line)
outfile2.close()

# word=('Chinese')
for i in range(len(items)):
    word = items[i][0] 
    
    r = requests.get(url='http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index'%word)
    html=r.text
    # 利用BeautifulSoup将获取到的文本解析成HTML
    soup = BeautifulSoup(r.text, "lxml")
    # 获取字典的标签内容
    #s = soup.find(class_='base-word')('ul')[0]('li')

    s = soup.find(class_='clearfix')('ul')[0]('li')
    
    s1 = soup.find(class_='phonetic').text
    
    
    # pattern = re.compile(r"F\(a\((.*)\), a\((.*)\)\)")
    pattern = re.compile(r'[\[](.*?)[\]]',re.S)
    match = re.findall(pattern,s1)
#    print(word)
#    print(match)
    with open(r'wocabulary.txt','a') as f:
        f.write(word +"\n")
        f.write(str(match) +"\n")
    # 输出字典的具体内容
    for item in s:
        if item.text:
            with open(r'wocabulary.txt','a') as f:              
                f.write(item.text +"\n")
    with open(r'wocabulary.txt','a') as f:        
        f.write(' '+"\n")
        f.write(' '+"\n")
#    print('='*40+'\n')