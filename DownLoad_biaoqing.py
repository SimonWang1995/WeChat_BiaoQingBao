import os,time
import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import  Queue
import pymysql



class DownloadBiaoqingbao(Thread):
    def __init__(self,queue,path):
        Thread.__init__(self)
        self.queue = queue
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def run(self):
        while True:
            url = self.queue.get()
            try:
                downloadbiaoqingbaos(url,self.path)
            finally:
                self.queue.task_done()

def downloadbiaoqingbaos(url,path):
    req = requests.get(url)
    html = BeautifulSoup(req.text,'lxml')
    image_list = html.find_all('img',class_ = 'ui image lazy')

    for image in image_list:
        src = image['data-original']
        title = image['title']
        print('mysql开始存储：',title)
        image_dict[title]=src




def mysql_save(img_dict):
    conn = pymysql.connect(host='localhost', user='root', db='biaoqingbao')
    cursor = conn.cursor()
    """create table urls (
        id int unsigned not null auto_increment,
        url varchar(255) not null unique,
        title varchar(255) not null,
        primary key(id)
    );"""
    """
        5.修改数据库的编码格式
        1
        mysql>alter database <数据库名> character set utf8;
        6.修改数据表格编码格式
        1
        mysql>alter table <表名> character set utf8;
        7.修改字段编码格式
        1
        2
        mysql>alter table <表名> change <字段名> <字段名> <类型> character set utf8;
        mysql>alter table user change username username varchar(20) character set utf8 not null;
    """

    for title, values in image_dict.items():
        conn.ping(reconnect=True)
        title = pymysql.escape_string(title)
        values = pymysql.escape_string(values)
        sql = """INSERT INTO urls (url,title) VALUES("{0}","{1}")""".format(values,title)
        try:
            cursor.execute(sql)
        except:
            print("Unexpected error:")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    start = time.time()
    image_dict = {}
    path = "D:\\Simon\\biaoqingbao\\"



    _url = "https://fabiaoqing.com/biaoqing/lists/page/{page}.html"
    # urls = [ _url.format(page=page) for page in range(1,200+1)]
    urls = [_url.format(page=page) for page in range(1, 200+1)]
    print(urls)

    queue = Queue()

    for x in range(10):
        worker = DownloadBiaoqingbao(queue, path)
        worker.daemon = True
        worker.start()

    for url in urls:
        queue.put(url)

    queue.join()
    # cursor.close()
    # conn.close()
    print(image_dict)
    mysql_save(image_dict)

    print('down loag finash:',time.time()-start)


