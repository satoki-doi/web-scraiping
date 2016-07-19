#!/usr/bin/env python
# coding: UTF-8

import urllib
import urllib2
import sys
from bs4 import BeautifulSoup
import os.path
import cPickle

dir = "../output_data"
OPENER = urllib2.build_opener()
OPENER.addheaders = [("User-Agent", "Mozilla/4.0")]
base = 'https://www.google.co.jp/search?site=imghp&tbm=isch&tbs=itp:photo&source=hp&num=20&q='


def SEARCH_WORD_GetHTML(que):
    """
    Google検索にアクセスする
    """
    url = base +  urllib.quote( "\"%s\"" % que )
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

file_name = "../input_data/item_list.pkl"
item_data = pickle_load(file_name)
item_list = item_data['item_name'].values()
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
        dir_name = item + "[%s]" % count 
        print print_text % dir_name
        os.mkdir(dir_name)
        soup = SEARCH_WORD_GetHTML(item)
        Get_imgURL(soup, dir_name)

        stop_time = poisson(lam=6) + 1
        time.sleep(stop_time)
        print "waiting %s seconds" % stop_time
        count += 1

Scraiping_ImgList(item_list)
