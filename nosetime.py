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

class HTTPSConnection(HTTPConnection):
    "This class allows communication via SSL."
    default_port = HTTPS_PORT

    def __init__(self, host, port=None, key_file=None, cert_file=None,
            strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            source_address=None):
        HTTPConnection.__init__(self, host, port, strict, timeout,
                source_address)
        self.key_file = key_file
        self.cert_file = cert_file

    def connect(self):
        "Connect to a host on a given (SSL) port."
        sock = socket.create_connection((self.host, self.port),
                self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        # this is the only line we modified from the httplib.py file
        # we added the ssl_version variable
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)

#now we override the one in httplib
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

def procession(soup,scent_class,res):
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

        res.write(pic + '\t' + name + '\t' + scent + '\t' + score + '\t' + comment + '\t' + scent_class + '\n')



def process(soup,res):
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

        res.write(pic + '\t' + name + '\t' + scent + '\t' + score + '\t' + comment + '\n')



def get_subfra(soup,res):
    cnt = 0

    prefix = 'https://www.nosetime.com/'

    soup = soup.find('div',class_= 'subfra')

    for scent in soup.find_all('a'):
        if cnt == 0:
            smell = scent.get_text()
            cnt += 1
            continue
        else:
            url = scent.get('href')
            url = prefix + url
            res[url] = scent.get_text()
    return smell



def crawl(id,num):
    res = codecs.open('nosetime.txt', 'a', 'utf-8')

    for i in range(1,num+1):
        print "正在爬取第" + str(i) + "页商品"

        #url="https://www.nosetime.com/brand.php?id="+ str(id) + "&page="+ str(i) + "#list"
        url = "https://www.nosetime.com/pinpai/10041254-yidameigui-a-dozen-roses.html"

        data = url_open(url)

        soup = BeautifulSoup(data,'html.parser')

        #print soup

        for item in soup.find_all('div', class_ = 'item' ):
            pic = item.find('img').get('src')
            pic = 'https:' + pic
            pic = pic[:-2]


            data = item.find('div',class_ = 'detail')
            name = data.find('h2').get_text()

            scent = item.find('div',class_ = 'info').get_text()

            reputation = item.find('div',class_ = 'score').get_text()

            details = reputation.split('(')

            score = details[0]
            comment = details[1][:-1]


            res.write(pic + '\t' + name + '\t' + scent + '\t' + 
            score + '\t' + comment + '\n')



    print("任务完成")
    res.close()

def crawl_salon():
    res = codecs.open('nosetime.txt','a','utf-8')

    brands = []

    seed = 'https://www.nosetime.com/pinpai/1-hot-salon.html'

    prefix = 'https://www.nosetime.com/'

    data = url_open(seed)

    soup = BeautifulSoup(data,'html.parser')
    soup = soup.find('div',class_='odorlist')

    for item in soup.find_all('li'):
        brand = item.find('a').get('href')
        brand = prefix + brand
        brands.append(brand)

    for brand in brands:
        raw_data = url_open(brand)
        soup = BeautifulSoup(raw_data,'html.parser')

        process(soup,res)

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
                    process(soup,res)
                else:
                    continue

    print("任务完成")
    res.close()


def crawl_scent():
    res = codecs.open('scent.txt', 'a', 'utf-8')
    subfragences = {}
    url = 'https://www.nosetime.com/xiangdiao/'
    prefix = 'https://www.nosetime.com/'

    data = url_open(url)
    soup = BeautifulSoup(data,'html.parser')
    classification = soup.find('map')

    for item in classification.find_all('area'):
        scent = item.get('href')
        scent = prefix + scent

        #print scent

        raw_data = url_open(scent)
        soup = BeautifulSoup(raw_data,'html.parser')

        smell = get_subfra(soup,subfragences)
        
        procession(soup,smell,res)

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
                    procession(soup,smell,res)
                else:
                    continue


    for fra in subfragences.keys():
        raw = url_open(fra)

        soup = BeautifulSoup(raw,'html.parser')

        smell = subfragences[fra]
        
        procession(soup,smell,res)

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
                    procession(soup,smell,res)
                else:
                    continue
 



if __name__=='__main__':
    httplib.HTTPSConnection = HTTPSConnection
    crawl_salon()

