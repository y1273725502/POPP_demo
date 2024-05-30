# 根据指定的NCID获取物种分类信息，写入数据库中（可更改数据库）
import json
import random
import sqlite3

import requests
from retrying import retry


# 设置重试装饰器
@retry(
    stop_max_attempt_number=5,  # 最大重试次数
    wait_fixed=1000,  # 重试之间的等待时间（毫秒）
    retry_on_exception=lambda x: isinstance(x, requests.exceptions.RequestException)
)
def make_request(Name):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent': random.choice(user_agents)}
    url = f"https://ngdc.cncb.ac.cn/cgir/genome/search?term={Name}&orgName=&genus=&family=&orgOrder=&orgClass=&orgGroup=&category=&draw=2&columns%5B0%5D.data=assembly&columns%5B0%5D.name=&columns%5B0%5D.searchable=true&columns%5B0%5D.orderable=false&columns%5B0%5D.search.value=&columns%5B0%5D.search.regex=false&columns%5B1%5D.data=tbOrganism.orgName&columns%5B1%5D.name=&columns%5B1%5D.searchable=true&columns%5B1%5D.orderable=true&columns%5B1%5D.search.value=&columns%5B1%5D.search.regex=false&columns%5B2%5D.data=tbOrganism.orgName&columns%5B2%5D.name=&columns%5B2%5D.searchable=true&columns%5B2%5D.orderable=false&columns%5B2%5D.search.value=&columns%5B2%5D.search.regex=false&columns%5B3%5D.data=synonym&columns%5B3%5D.name=&columns%5B3%5D.searchable=true&columns%5B3%5D.orderable=true&columns%5B3%5D.search.value=&columns%5B3%5D.search.regex=false&columns%5B4%5D.data=tbOrganism.taxid&columns%5B4%5D.name=&columns%5B4%5D.searchable=true&columns%5B4%5D.orderable=true&columns%5B4%5D.search.value=&columns%5B4%5D.search.regex=false&columns%5B5%5D.data=tbOrganism.orgGroup&columns%5B5%5D.name=&columns%5B5%5D.searchable=true&columns%5B5%5D.orderable=true&columns%5B5%5D.search.value=&columns%5B5%5D.search.regex=false&columns%5B6%5D.data=tbOrganism.family&columns%5B6%5D.name=&columns%5B6%5D.searchable=true&columns%5B6%5D.orderable=true&columns%5B6%5D.search.value=&columns%5B6%5D.search.regex=false&columns%5B7%5D.data=assembly&columns%5B7%5D.name=&columns%5B7%5D.searchable=true&columns%5B7%5D.orderable=true&columns%5B7%5D.search.value=&columns%5B7%5D.search.regex=false&columns%5B8%5D.data=synonymId&columns%5B8%5D.name=&columns%5B8%5D.searchable=true&columns%5B8%5D.orderable=true&columns%5B8%5D.search.value=&columns%5B8%5D.search.regex=false&columns%5B9%5D.data=size&columns%5B9%5D.name=&columns%5B9%5D.searchable=true&columns%5B9%5D.orderable=true&columns%5B9%5D.search.value=&columns%5B9%5D.search.regex=false&columns%5B10%5D.data=gc&columns%5B10%5D.name=&columns%5B10%5D.searchable=true&columns%5B10%5D.orderable=true&columns%5B10%5D.search.value=&columns%5B10%5D.search.regex=false&order%5B0%5D.column=0&order%5B0%5D.dir=asc&start=0&length=10&search.value=&search.regex=false"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 抛出HTTP错误（4xx, 5xx等）
    return response


def tax_info(Name,ncID, databaseName):
    try:
        response = make_request(Name)
    except requests.exceptions.RequestException as e:
        print(f"Failed to make the request: {e}")
        return


    if response.status_code == 200:
        parsed_data = response.json()

        if len(parsed_data['data']) > 0:

            # 提取所需字段
            org_info = parsed_data['data'][0]['tbOrganism']
            orgName = org_info['orgName']
            orgGroup = org_info['orgGroup']
            orgClass = org_info['orgClass']
            orgOrder = org_info['orgOrder']
            family = org_info['family']
            genus = org_info['genus']
            orgNameC = org_info['orgNameC']

            # 连接到 SQLite 数据库
            conn = sqlite3.connect(databaseName)
            c = conn.cursor()

            # 创建表格（如果不存在）
            c.execute('''CREATE TABLE IF NOT EXISTS organisms
                             (orgName TEXT, ncID TEXT,orgGroup TEXT, orgClass TEXT, orgOrder TEXT, family TEXT, genus TEXT, orgNameC TEXT)''')

            # 插入数据
            c.execute("INSERT OR IGNORE INTO organisms VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (orgName, ncID, orgGroup, orgClass, orgOrder, family, genus, orgNameC))

            # 提交更改并关闭连接
            conn.commit()
            conn.close()
        else:
            print("No organism")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
