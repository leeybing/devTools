# -*- coding:utf-8 -*-
# autu :liyongbing  
# time: 2022/8/26
import time, csv, threading
import datetime
from pprint import pprint
import pandas as pd

import requests, matplotlib.pyplot as plt
from pylab import mpl

# 2存贮数据
fo = open('股票数据.csv', mode='w', encoding='utf-8', newline='')

csv_write = csv.DictWriter(fo, fieldnames=['股票名称', '股票代码', '当前价格', '成交量'])

csv_write.writeheader()
url_list = [
    "https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_={}".format(
        page, round(time.time() * 1000)) for page in range(1, 5)]


# 1 爬取数据
def request_data(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }

    # data = {
    #     'page': 1,
    #     'size': 30,
    #     'order': 'desc',
    #     'orderby': 'percent',
    #     'order_by': 'percent',
    #     'market': 'CN',
    #     'type': 'sh_sz',
    #     '_': int(round(time.time() * 1000))
    # }
    re = requests.get(url, headers=header)
    dataList = re.json().get('data').get('list')
    # 获取需要的数据
    if dataList:
        dict_temp = {}
        for data in dataList:
            dict_temp['股票名称'] = data.get('name')
            dict_temp['股票代码'] = data.get('symbol')
            dict_temp['当前价格'] = data.get('current')
            dict_temp['成交量'] = data.get('volume')
            csv_write.writerow(dict_temp)


# 多线程爬取数据
def request_thread(url_lists):
    threadList = []
    for url in url_lists:
        t = threading.Thread(target=request_data, args=(url,))
        threadList.append(t)
    for i in threadList:
        i.start()
        time.sleep(1)
    for i in threadList:
        i.join()


def show_data(file='股票数据.csv'):
    # 4清洗数据
    # 从csv文件导入数据
    data_pd = pd.read_csv(file)
    # 剔除确实的行
    df = data_pd.dropna()
    # 获取数据
    df1 = df[['股票名称', '当前价格', '股票代码', '成交量']]
    # 绘制图像，横纵坐标
    df2 = df1.iloc[0:10]
    plt.bar(df2['股票名称'].values, df2['当前价格'].values, label='分析结果')
    plt.show()


if __name__ == '__main__':
    request_thread(url_list)
    fo.close()
    show_data()
