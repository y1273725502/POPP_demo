import os
import random

import requests
from bs4 import BeautifulSoup
from lxml import html
from retrying import retry


def getID(ncID):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent': random.choice(user_agents)}
    print("下载" + ncID + "中")
    # 获取ncid
    url1 = 'https://www.ncbi.nlm.nih.gov/nuccore/' + ncID + '?report=gilist&log$=seqview&format=text'
    response = requests.get(url1, headers=headers)
    response.raise_for_status()  # 抛出HTTP错误（4xx, 5xx等）
    return response


def getCDS(ncid):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent': random.choice(user_agents)}
    url = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta_cds_na&id=' + ncid + '&conwithfeat=on&withparts=on&show-sequence=on&hide-cdd=on'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 抛出HTTP错误（4xx, 5xx等）
    return response


def download_file(ncID, Folder):
    ncid = None

    try:
        response = getID(ncID)
    except requests.exceptions.RequestException as e:
        print(f"Failed to make the request: {e}")
        return None

    tree = html.fromstring(response.content)
    pre_elements = tree.xpath('//body/pre')
    if pre_elements:
        for pre in pre_elements:
            ncid = pre.text
    else:
        print('Element not found.')
        return

    try:
        response = getCDS(ncid)
    except requests.exceptions.RequestException as e:
        print(f"Failed to make the request: {e}")
        return None

    print(Folder + "/" + ncID + '.txt')
    # 保存文件
    with open(Folder + "/" + ncID + '.txt', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # 检查文件是否有效
    if os.path.isfile(Folder + "/" + ncID + '.txt'):
        # 如果文件的大小是1字节，则删除文件
        if os.path.getsize(Folder + "/" + ncID + '.txt') == 1:
            os.remove(Folder + "/" + ncID + '.txt')
            print('已删除1字节文件: {}'.format(Folder + "/" + ncID + '.txt'))
        else:
            print('文件字节大小不为1，未进行删除操作: {}'.format(Folder + "/" + ncID + '.txt'))
    else:
        print('该路径无效或文件不存在: {}'.format(Folder + "/" + ncID + '.txt'))
    print("下载成功")
