#!/usr/bin/env python
# coding: UTF-8

import urllib, urllib2, sys
from bs4 import BeautifulSoup
import os.path
import cPickle

dir = "."
OPENER = urllib2.build_opener()
OPENER.addheaders = [("User-Agent", "Mozilla/4.0")]
base = 'https://www.google.co.jp/search?site=imghp&tbm=isch&tbs=itp:photo&source=hp&num=20&q='

def SEARCH_WORD_GetHTML(que):
    """
    Google検索にアクセスする
    """
    url = base +  urllib.quote( "\"%s\"" % que)
    html = OPENER.open( url ).read()
    soup = BeautifulSoup( html , "lxml")

    return soup

def DL_img(img_url, word):
    try:
        img = urllib2.urlopen(img_url)
        fname = img_url.split("/")[-1]
        file = '%s/%s/%s.jpg' % (dir, word, fname)
        localfile = open(file, "w")
        print file
        localfile.write(img.read())
        img.close()
        localfile.close()
    except:
        print ""

def Get_imgURL(soup, word):
    Namelist = soup.find_all('img')
    for link in Namelist:
        try:
            img_url = link.get('src')
            # print img_url
            DL_img(img_url, word)
        except Exception as e:
            print e

# 商品名の読み取り
def pickle_load(file_name):
    """
    file loading
    """
    fh = open(file_name)
    result = cPickle.load(fh)
    fh.close
    return result

file = "item_list.pkl"
item_data = pickle_load(file)
item_list = item_data['item_name'].values()[0:101]
print_text = """
    -----------------------------------
    -----------------------------------
    scraipin %s ....... 
    -----------------------------------
    -----------------------------------
    """

def Scraiping_ImgList(item_list):
    count = 0
    for item in item_list:
        dir_name = item + "[%s]"  % count + "code1"
        print print_text % dir_name
        os.mkdir(dir_name)
        soup = SEARCH_WORD_GetHTML(item)
        Get_imgURL(soup, dir_name)
        count += 1

Scraiping_ImgList(item_list)






