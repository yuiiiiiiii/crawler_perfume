# coding=utf-8
import urllib2,urllib
import re
import codecs
import socket
import sys
import bs4
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

import httplib
from httplib import HTTPConnection, HTTPS_PORT
import ssl

# ssl_version corrections are done

#打开网页，获取网页内容
def url_open(url):
    headers=("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener=urllib2.build_opener()
    opener.addheaders=[headers]
    urllib2.install_opener(opener)
    response=urllib2.Request(url)
    data=urllib2.urlopen(response).read().decode("utf-8","ignore")
    return data

def procession(soup,p_name,res):
    products = soup.find_all('div',class_='item')

    for product in products:
        pic = product.find('img').get('src')
        pic = 'https:' + pic
        pic = pic[:-2]

        d = product.find('div',class_ = 'detail')
        name = d.find('h2').get_text()

        scent = product.find('div',class_ = 'info').get_text()

        reputation = product.find('div',class_ = 'score').get_text()

        details = reputation.split('(')

        score = details[0]
        comment = details[1][:-1]

        res.write(pic + '\t' + name + '\t' + scent + '\t' + score + '\t' + comment + '\t' + p_name + '\n')



def crawl():
    res = codecs.open('perfumer.txt', 'a', 'utf-8')

    url = "https://www.nosetime.com/tiaoxiangshi/"
    data = url_open(url)

    #print data
    soup = BeautifulSoup(data,'html.parser')


    for data in soup.find_all('dd'):
        perfumer = data.find('a').get('href')
        p_name = data.find('a').get_text()
        perfumer = 'https://www.nosetime.com/' + perfumer

        print perfumer

        raw_data = url_open(perfumer)
        soup = BeautifulSoup(raw_data,'html.parser')

        flag = len(soup.find('div',class_='next_news').get_text()) == 0

        print flag

        if flag == True:
            products = soup.find_all('div',class_='item')

            for product in products:
                pic = product.find('img').get('src')
                pic = 'https:' + pic
                pic = pic[:-2]

                d = product.find('div',class_ = 'detail')
                name = d.find('h2').get_text()

                scent = product.find('div',class_ = 'info').get_text()

                reputation = product.find('div',class_ = 'score').get_text()

                details = reputation.split('(')

                score = details[0]
                comment = details[1][:-1]

                res.write(pic + '\t' + name + '\t' + scent + '\t' + score + '\t' + comment + '\t' + p_name + '\n')
        else:
            procession(soup,p_name,res)

            prefix = 'https://www.nosetime.com/perfumer.php'


            end = False

            while (end == False):
                end = True

                pages = soup.find('div',class_='next_news')
                for page in pages.find_all('a'):
                    sr = page.get_text()
                    suffix = page.get('href')

                    # print sr,end
                    # print suffix

                    if sr == '下一页':
                        end = False
                        url_next = prefix + suffix
                        print url_next
                        data = url_open(url_next)
                        soup = BeautifulSoup(data,'html.parser')
                        procession(soup,p_name,res)
                    else:
                        continue


    print("任务完成")
    res.close()

if __name__=='__main__':
    crawl()

