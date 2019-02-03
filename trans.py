#coding:utf-8
import requests
from bs4 import BeautifulSoup
import pprint
import re
import sys
import random
import datetime
from urllib.parse import urlparse


list = []
def getSoup(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    return soup

def check_extension(filename):
    match = re.search("(\.jpg|\.png|\.gif|\.svg)",filename)
    if isinstance(match,type(None)):
        return False
    else:
        return True

def getImage(url):
    soup = getSoup(url)
    img = soup.find_all("img")
    #画像がなかった場合何もしない
    if isinstance(img,type(None)):
        pass
    #画像があった場合の処理
    else:
        for i in img:
            try:
                ans = re.match("http",i.get("src"))
                #画像URLがhttpから始まらない場合の処理
                if isinstance(ans,type(None)):
                    img_url = urlparse(url)
                    download_url = img_url.scheme+"://"+img_url.netloc+i.get("src")
                    r = requests.get(download_url)
                    #ファイル名の処理
                    img_url_split = i.get("src").split("/")
                    #拡張子がある場合の処理
                    if check_extension(img_url_split[len(img_url_split)-1]):
                        with open("./img/"+img_url_split[len(img_url_split)-1],"wb") as f:
                            f.write(r.content)
                    #拡張子がない場合の処理
                    else:
                        file_name = img_url_split[len(img_url_split)-1]+".jpg"
                        with open ("./img/"+file_name,"wb") as f:
                            f.write(r.content)
                #画像URLがhttpから始まる場合の処理
                else:
                    r = requests.get(i.get("src"))
                    img_url_split = i.get("src").split("/")
                    #拡張子がある場合の処理
                    if check_extension(img_url_split[len(img_url_split)-1]):
                        with open("./img/"+img_url_split[len(img_url_split)-1],"wb") as f:
                            f.write(r.content)
                    #拡張子がない場合の処理
                    else:
                        file_name = img_url_split[len(img_url_split)-1]+".jpg"
                        with open ("./img/"+file_name,"wb") as f:
                            f.write(r.content)
            except:
                pass


def recursive_url(url):
    getImage(url)
    soup = getSoup(url)
    a = soup.find_all("a")
    pattern = re.compile("http.+")
    print("[+]--------------------現在URL--------------------[+]")
    for i in a:
        if isinstance(i.get("href"),type(None)):
            pass
        else:
            res = pattern.search(i.get("href"))
            if res is not None:
                list.append(i.get("href"))
            else:
                pass
    print(list[random.randint(0,len(list)-1)])
    return recursive_url(list[random.randint(0,len(list)-1)])

url = input("URL: ")
recursive_url(url)
