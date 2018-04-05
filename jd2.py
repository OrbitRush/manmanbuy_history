#!/usr/bin/python
# -*- coding: utf-8 -*-
#json string:
import urllib3
import random
import execjs #安装 pip install PyExecJS
import json
import re

def GET_Data(): #获取数据并保存
    HTTP=urllib3.PoolManager()
    Goods_ID=Random_Num() #随机生成的商品ID
    #Goods_ID = '5556351'
    Token=Cre_Token_Js(Goods_ID) #用JavaScript将含有商品ID的链接，加密生成token
    URL='http://tool.manmanbuy.com/history.aspx?DA=1&action=gethistory&url=http%253A%2F%2Fitem.jd.com%2F'+Goods_ID+'.html&bjid=&spbh=&cxid=&zkid=&w=951&token='+Token
    print(Goods_ID)
    print(URL)
    Header_Dict = {
        'Host': 'tool.manmanbuy.com', 'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5083.400 QQBrowser/10.0.988.400',
        'Referer': 'http://tool.manmanbuy.com/history.aspx?w=951&h=580&h2=420&m=1&e=1&browes=1&url=http%3A//item.jd.com/' + Goods_ID + '.html&token='+Token,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
            }
    Re_Str=HTTP.request('GET',url=URL,headers=Header_Dict).data
    if Re_Str:
        Re_Str = str(Re_Str, encoding='gbk')
        Re_Json=json.loads(Re_Str,encoding='gbk') #json解析
        Re_Date=Spr_Date(Re_Json['datePrice']) #Date数据查询的整理
        Data=Re_Json['spName']+","+Re_Json['spUrl']+","+str(Re_Json['spPic'])+","+Re_Date+ "\n" #拼接数据：商品名，商品链接，商品图片链接，调价日期
        Save_To_File('d:\l.csv', Data) #保存数据
    else:
        print(Re_Str)

def Random_Num(): #生成随机的商品ID
    return str(random.randint(1000000,9999999))

def Cre_Token_Js(Goods_ID_F): #JavaScript加密生成token
    Js_File_Name="D:/Code/MMM_GET_TOKEN.js" #JS的路径，根据需要修改
    f = open(Js_File_Name, 'r', encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    #return htmlstr
    js = execjs.compile(htmlstr)
    Token=js.call('d.encrypt','http://item.jd.com/'+Goods_ID_F+'.html','2','true')
    return Token

def Spr_Date(Date): #Date数据查询的整理
    Re_Date=re.findall("\[Date.UTC\(([\s\S]*?,[\s\S]*?,[\s\S]*?)\),(.*?)\]",Date)
    Re_Date_Final=''
    for Date_i in Re_Date:
        Re_Date_Final =Re_Date_Final+  str(Date_i[0].replace(',','.',)) + "," + str(Date_i[1].replace(',','.',)) + ","
    print(Re_Date_Final)
    return Re_Date_Final

def Save_To_File(file_name, contents): #保存文件
    fh = open(file_name, 'a',encoding='gbk')
    fh.write(contents)
    fh.close()
    #with open(file_name, 'a',encoding='utf-8') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(contents)
    #f.close()

if __name__ == '__main__':
    for i in range(1000): #循环1000次
        GET_Data()