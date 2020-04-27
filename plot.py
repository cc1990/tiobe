# -*- coding: utf-8 -*-
# @Author  : cc
# @File    : plot.py

from matplotlib import pyplot as plt
import pandas as pd


def sort_key(dict_data, reversed=False):
    keys = sorted(dict_data.keys(), reverse=reversed)
    new_dict = {}
    for key in keys:
        new_dict[key] = dict_data[key]
    return new_dict


data = pd.read_csv('tiobe_data.csv')
names = list(set(data['name']))

# 保存所有的月份信息
month_list = data[data['name'].isin(['Java'])]['date'].values

# 创建嵌套列表，每隔日期下保留的是每种编程语言的热度值
per_month_lan_dict = {i: {j: 0 for j in names} for i in month_list}
for month in month_list:
    for name in names:
        try:
            per_month_lan_dict[month][name] = data[(data['name'] == name) & (data['date'] == month)]['value'].values[0]
        except Exception as e:
            continue

dict_data = sort_key(per_month_lan_dict)

# 设置柱状图的颜色
colors = ['k', 'r', 'sienna', 'yellow', 'g', 'aquamarine', 'dodgerblue', 'pink', 'b', 'darkviolet']
color_dict = dict(zip(names, colors))

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 设置图像大小和像素
plt.figure(figsize=(20, 8), dpi=80)

for data_item in dict_data.items():
    plt.cla()
    temp = sorted(data_item[1].items(), key=lambda item: item[1])

    x = [item[0] for item in temp]
    color = [color_dict[i] for i in x]
    y = [item[1] for item in temp]

    plt.barh(range(1, len(names) + 1), y, color=color)
    plt.title(data_item[0], fontsize=24)
    plt.yticks(range(1, len(names) + 1), list(x), fontsize=16)
    plt.xticks(range(0, 30, 100))
    for x, y in zip(range(1, len(names) + 1), y):
        plt.text(y + 0.1, x - 0.1, str(y))
    plt.pause(0.1)

plt.show()
