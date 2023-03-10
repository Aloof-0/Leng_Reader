# -*- coding: utf-8 -*-
# @Time    : 2023/3/10 9:11
# @Author  : Leng
# @Git     : Aloof-0
# @File    : thread_reader.py
# @Software: PyCharm
import json
import random
import time

import requests
from PyQt5.QtCore import QThread, pyqtSignal


# 定义一个线程类
class New_Thread(QThread):
    finishSignal = pyqtSignal(str)

    def __init__(self, circulate, W3_R1, speed, parent=None):
        super(New_Thread, self).__init__(parent)
        self.circulate = circulate
        self.W3_R1 = W3_R1
        self.speed = speed

    def run(self):
        while True:
            if self.circulate:
                self.W3_R1.verticalScrollBar().setValue(self.W3_R1.verticalScrollBar().value() + 20)
                time.sleep(self.speed)


# 定义一个爬虫线程类
class Requests_Thread(QThread):
    finishSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Requests_Thread, self).__init__(parent)
        self.headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
        self.data = {"routeType": "publish_list",
                     "page": random.randint(2, 7),  # 第5页到第七页
                     "pageSize": 10,
                     "type": "created"}
        with open("conf/proxy.json", "r", encoding="utf8") as f:
            self.proxies = json.loads(f.read()).get("proxy_list")[random.randint(0, 100)].get("proxy")

    def run(self):
        crawler = requests.post(url=r"https://www.003kk.top/index.php/joe/api", data=self.data, headers=self.headers,
                                proxies={"http": self.proxies})
        print(crawler.json())
        if crawler.status_code == 200:
            try:
                try:
                    onlie_list = [{"permalink": i.get("permalink"), "image": i.get("image")[0],
                                   "image_local": i.get("image")[0].split("/")[-1], "title": i.get("title"),
                                   "column": "{}{}阅读{}评论{}点赞".format(i.get("created"), i.get("views"),
                                                                           i.get("commentsNum"),
                                                                           i.get("agree"))} for i in
                                  crawler.json().get("data")[1:]]
                    Web_Images = [i.get("image")[0] for i in crawler.json().get("data")[1:]]
                except Exception as e:
                    print(e)
                else:
                    if onlie_list:
                        with open("conf/html.json", "w", encoding="utf8") as f:
                            f.write(json.dumps(onlie_list))
                        for i in Web_Images:
                            with open('asset/{}'.format(i.split("/")[-1]), 'wb') as file_obj:
                                file_obj.write(requests.get(i).content)
            except Exception as e:
                print(e)
