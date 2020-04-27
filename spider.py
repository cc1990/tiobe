# -*- coding: utf-8 -*-
# @Author  : cc
# @File    : spider.py

import requests
import re
import csv


class TiobeSpider(object):
    def __init__(self):
        self.url = 'https://www.tiobe.com/tiobe-index/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36 Edg/81.0.416.58',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.table = 'tiobe_data.csv'

    def run(self):
        response = requests.get(self.url, headers=self.headers)
        text = response.text

        total_content = ''.join(re.findall(r'series: (.*?)\}\);', text, re.DOTALL))  # re.DOTALL匹配到多行，包含换行符
        total_content = re.findall(r'({.*?})', total_content, re.DOTALL)

        with open(self.table, 'w', newline='') as f:
            self.write = csv.DictWriter(f, ['name', 'value', 'date'])
            self.write.writeheader()
            
            for content in total_content:
                name = ''.join(re.findall(r"{name : '(.*?)'", content, re.DOTALL))
                if name == 'Visual Basic':
                    name = 'VB'
                elif name == 'JavaScript':
                    name = 'JS'
                data = re.findall(r"Date.UTC(.*?)\]", content, re.DOTALL)
                for i in data:
                    i = i.replace(' ', '')  # 去掉空格
                    i = re.sub(r'[()]', '', i)  # 将小括号匹配为空
                    value = i.split(',')[-1]
                    date_list = i.split(',')[:3]
                    time = ''
                    for index, j in enumerate(date_list):
                        if index != 0:
                            if len(j) == 1:
                                j = '0' + j
                            time = time + '-' + j
                        else:
                            time = time + j

                    dict_data = {'name': name, 'value': value, 'date': time}
                    self.write.writerow(dict_data)
        print('爬取完成')


if __name__ == '__main__':
    tiobe = TiobeSpider()
    tiobe.run()