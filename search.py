import time,os,re
import itchat
from itchat.content import TEXT,PICTURE
import pymysql
import requests

Nicklist = ["Scorpio","Hana是我是Hana"]
url_list = []


def searchImage(text):
	imgs = []
    conn = pymysql.connect(host='localhost',user='root',db='biaoqingbao')
    cursor=conn.cursor()
    sql = """select * from urls where title like '%{0}%'""".format(text)
    print(sql)
    try:
        cursor.execute(sql)
    except:
        print("execute sql search failed")
    # rows=cursor.fetchall()
    # for row in rows:
    #     #url_list.append(row[1])
    #     download_image(row[1],path)
    for i in range(6):
        row = cursor.fetchone()
        if row:
            imgs.append(download_image(row[1],path))
        else:
            print("Don't found photo")


def download_image(url,path):
    req = requests.get(url).content
    name=url.split('/')[-1]
    try:
        with open(path+name,'wb') as f:
            f.write(req)
    except OSError:
        print('Length failed')
    return path+name


@itchat.msg_register([PICTURE,TEXT])
def text_reply(msg):
    print(msg.text)
    if msg['User']['NickName'] in Nicklist and bool(re.match("\"(.*)\"",msg.text)):
    #if msg['User']['NickName'] == 'Hana是我是Hana':
        keyword = re.match("\"(.*)\"",msg.text).group(1)
        imgspath = searchImage(keyword)
        time.sleep(10)
        if len(imgs) != 0:
            for img in imgspath:
                itchat.send_image(img,toUserName=msg['FromUserName'])
                # msg.user.send_image(img)
                time.sleep(0.3)
                print('开始发送表情：',img)
                os.remove(img)
        else:
            itchat.send_msg("Sorry,No image found, please change keywords")

if __name__ == '__main__':
    path = "D:\\Simon\\biaoqingbao\\"
    if not os.path.exists(path):
        os.makedirs(path)

    itchat.auto_login()
    #itchat.auto_login(hotReload=True)
    itchat.run()

# path = "D:\\Simon\\biaoqingbao\\"
# if not os.path.exists(path):
#     os.makedirs(path)
# searchImage('???')
