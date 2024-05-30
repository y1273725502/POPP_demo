import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
def get_chloroplast_nuccore_result(fold):
    old_file_name='nuccore_result.txt'
    new_file_name='chloroplast_nuccore_result.txt'

    # 创建设置项
    options = webdriver.EdgeOptions()

    # 创建新默认路径与下载设置
    prefs = {"download.default_directory": f"{fold}", "download.prompt_for_download": False}

    # 将创建的下载部分的设置添加到option中
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')
    # 修改设置使程序结束后浏览器不自动关闭
    options.add_experimental_option('detach', True)
    #options.add_argument('--headless')
    # 实例化Edge浏览器对象，并将options传入该实例对象
    driver = webdriver.Edge(options=options)


    # 打开一个网页
    driver.get('https://www.ncbi.nlm.nih.gov/nuccore')
    # 找到要输入的元素。这里我们假设元素可以通过其id找到
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/div[2]/div[2]/div/div/div/div/input')
    #
    # # 在元素中输入内容
    element.send_keys('(genome AND plants[filter] AND chloroplast[filter] AND ( "100000"[SLEN] : "200000"[SLEN] ))')

    # # 找到要点击的元素。这里我们假设元素可以通过其id找到
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/div[2]/div[2]/div/div/button')
    element.click()

    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[1]/h4/a')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[1]/div[4]/div[1]/fieldset/ul/li[1]/label')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[1]/div[4]/div[1]/div[1]/button')
    element.click()
    # 等待文件下载完成
    # 检查文件是否存在
    if os.path.exists(os.path.join(fold, new_file_name)):
        # 删除文件
        os.remove(os.path.join(fold, new_file_name))
        print("文件已删除")
    else:
        print("文件不存在")
    print("downloading")
    while not os.path.exists(os.path.join(fold, old_file_name)):
        time.sleep(1)
    # 重命名文件
    os.rename(os.path.join(fold, old_file_name), os.path.join(fold, new_file_name))
    driver.quit()
