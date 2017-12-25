# coding=utf-8
import urllib2,urllib
import re
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#打开网页，获取网页内容
def url_open(url):
    headers=("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener=urllib2.build_opener()
    opener.addheaders=[headers]
    urllib2.install_opener(opener)
    response=urllib2.Request(url)
    data=urllib2.urlopen(response).read().decode("utf-8","ignore")
    return data

def crawl(keywd,num):
    res = codecs.open('result.txt', 'a', 'utf-8')

    keywords=urllib.quote(keywd)


    for i in range(num):

        if num == 1:
            url = 'https://s.taobao.com/search?q='+keywords+'&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171217&ie=utf8'
        else:
            url="https://s.taobao.com/search?q="+keywords+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(i*44)
        data=url_open(url)

        #print data
        #定义各个字段正则匹配规则
        item_pat = '"comment_url":"(//.*?)"'
        img_pat='"pic_url":"(//.*?)"'
        name_pat='"raw_title":"(.*?)"'
        nick_pat='"nick":"(.*?)"'
        price_pat='"view_price":"(.*?)"'
        fee_pat='"view_fee":"(.*?)"'
        sales_pat='"view_sales":"(.*?)"'
        comment_pat='"comment_count":"(.*?)"'
        city_pat='"item_loc":"(.*?)"'
        itemID_pat = '"nid":"(.*?)"'
        #查找满足匹配规则的内容，并存在列表中
        urlL    = re.compile(item_pat).findall(data)
        imgL    = re.compile(img_pat).findall(data)
        nameL   = re.compile(name_pat).findall(data)
        nickL   = re.compile(nick_pat).findall(data)
        priceL  = re.compile(price_pat).findall(data)
        feeL    = re.compile(fee_pat).findall(data)
        salesL  = re.compile(sales_pat).findall(data)
        commentL= re.compile(comment_pat).findall(data)
        cityL   = re.compile(city_pat).findall(data)
        nidL = re.compile(itemID_pat).findall(data)

        for j in range(3,len(salesL)):

            img="http:" + imgL[j]#商品图片链接
            name=nameL[j]#商品名称
            nick=nickL[j]#淘宝店铺名称
            price=priceL[j]#商品价格
            fee=feeL[j]#运费
            sales=salesL[j]#商品付款人数
            comment=commentL[j]#商品评论数，会存在为空值的情况
            ID = nidL[j]
            if(comment==""):
                comment=0
            city=cityL[j]#店铺所在城市
            
            urls = "http://item.taobao.com/item.htm?id="+str(ID)+"&ns=1&abbucket=8#detail"

            print('正在爬取第'+str(i)+"页，第"+str(j)+"个商品信息...")
            res.write( name.encode('utf-8') + '\t' + urls.encode('utf-8') + '\t' + str(price) + '\t' + str(fee) + '\t' + str(sales) + '\t' + str(comment) + '\t' + 
            str(city) + '\t' + str(nick) + '\t' + str(img) + '\n')

    print("任务完成")
    res.close()



if __name__=='__main__':
    to_crawl_list = [
    ('纳茜素香水',35),('橘滋香水',18),('蒂埃里穆勒香水',4),('浪凡香水',100),('D二次方香水',2),('卡地亚香水',40),
    ('维特罗夫香水',3),('高缇耶香水',4),('王薇薇香水',5),('莱俪香水',19),('密使香水',3),('川久保玲香水',3),('帝门特香水',4),
    ('芦丹氏香水',73),('阿蒂仙香水',53),('潘海利根香水',52),('蒂普提克香水',55),('安霓可古特尔香水',4),('欧珑香水',25),
    ('帕尔玛之水香水',25),('拜里朵香水',2),('信仰香水',31),('配枪朱丽叶香水',1),('马丁马吉拉香水',1),('香水实验室香水',6),
    ('nasomatto香水',2),('克利安香水',1),('别样公司香水',1),('ormonde jayne香水',2)]

    for i in to_crawl_list:
        crawl(i[0],i[1])

