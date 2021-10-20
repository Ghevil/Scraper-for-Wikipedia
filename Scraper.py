#coding:utf-8

from os import name
from typing import Counter
import requests
from bs4 import BeautifulSoup
from langconv import *

COUNT=0


def convert(text):
    return Converter('zh-hans').convert(text)

def the_spider(name):
    response = requests.get('https://zh.wikipedia.org/wiki/'+name,timeout=10)

    html=response.text
    print(response.status_code)#当前网站返回的状态码
    #print(type(response.text))#网页内容的类型

    print(type(html))#返回值的类型
    soup = BeautifulSoup(html,'lxml')
    inp=((soup.body.find(id='content').find(id='bodyContent').find(id='mw-content-text')))

    tt=inp.select('p')
    re=''
    for i in tt:
        if(len(re+i.text)>=520):
            return re
        else: 
            re=re+i.text
    return re

def context_process(context):
    re=''
    for i in context:
        if i=='\n':
            continue
        else:
            re+=i
    context=re
    re=''

    f=False
    for i in context:
        if (not f) :
            if i=='[':
                f=True
            else :
                re+=i
        if f:
            if i==']':
                f=False
    return re

def format_output(file,name,context):
    global COUNT
    file.write('    {\n      "paragraphs": [\n        {\n          "id": "TRAIN_%d",\n          "context": "%s",\n          "qas": [\n          ]\n        }\n      ],\n      "id": "TRAIN_%d",\n      "title": "%s"\n    },\n'%(COUNT,context,COUNT,name),)
    COUNT+=1

if __name__=='__main__':
    ff=open("D:\\Training.json",'w+',encoding='utf-8')
    
    str="虎 " #以空格分隔的词条
    name = ''
    f=False
    for i in str:
        if(i!=' '):
            name+=i
        if(i==' '):
            print(COUNT,end='. ')
            print(name)
            T1=the_spider(name)
            context=convert(T1)
            print(context_process(context))
            format_output(ff,name,context_process(context))
            name=''


    ff.close()