# -*- coding:utf-8 -*-

#爬取淘宝商品
import urllib.request
import pymysql
import re

#打开网页，获取网页内容
def url_open(url):
    headers = ("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
    return data

#将数据存入数据库中
def data_Import(sql):
    conn = pymysql.connect(host="127.0.0.1",user = 'root',password = "123456",db = "tbsp",charset="utf8")
    conn.query(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    try:
        #定义要查询的商品关键词
        keywd = "短裙"
        keywords = urllib.request.quote(keywd)
        #定义要爬取的页数
        num = 100
        for i in range(num):
            url = "https://s.taobao.com/search?q="+keywords+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(i*44)
            data = url_open(url)
            #定义各个字段正则匹配规则
            #商品图片
            img_pat = '"pic_url":"(//.*?)"'
            #商品标题
            name_pat = '"raw_title":"(.*?)"'
            #店铺名称
            nick_pat = '"nick":"(.*?)"'
            #商品价格
            price_pat = '"view_price":"(.*?)"'
            #邮费
            free_pat = '"view_fee":"(.*?)"'
            #付款人数
            sales_pat = '"view_sales":"(.*?)"'
            #评论
            comment_pat = '"comment_count":"(.*?)"'
            #地区
            city_pat = '"item_loc":"(.*?)"'
            #查找满足匹配规则的内容，并存在列表中
            imgL = re.compile(img_pat).findall(data)
            nameL = re.compile(name_pat).findall(data)
            nickL  = re.compile(nick_pat).findall(data)
            priceL = re.compile(price_pat).findall(data)
            freeL = re.compile(free_pat).findall(data)
            salesL = re.compile(sales_pat).findall(data)
            commentL = re.compile(comment_pat).findall(data)
            cityL = re.compile(city_pat).findall(data)

            for j in range(len(imgL)):
                img = "http:" + imgL[j]
                name = nameL[j]
                nick = nickL[j]
                price = priceL[j]
                free = freeL[j]
                sales =salesL[j]
                comment = commentL[j]
                if (comment==""):
                    comment=0
                city = cityL[j]
                print("正在爬取第"+str(i)+"页，第"+str(j)+"个商品信息...")
                sql = "insert into taobao(name,price,free,sales,comment,city,nick,img) value('%s','%s','%s','%s','%s','%s','%s','%s')" %(name,price,free,sales,comment,city,nick,img)
                                   #taobao(表示数据表)
                data_Import(sql)
                print("爬取完成，且数据存入数据库")

    except Exception as e:
        print(str(e))
print("任务完成")

