import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import json

URL = "https://www.luogu.com.cn/training/list"
options = Options()
options.add_argument("--headless") # 无头模式
options.set_preference("permissions.default.image", 2) # 无图模式
profile = FirefoxProfile()
profile.set_preference("permissions.default.frame", 3) # 禁用加载 iframe 的功能 (bilibili嵌套)
options.profile = profile
driver = webdriver.Firefox(options=options)
driver.get(URL)
print("[LOG] 加载索引")
TITLE_XPATH_TEMPLATE = '//*[@id="app"]/div[2]/main/div/div[2]/div/div[1]/div[2]/div[TDNUM]/span[2]/a'
TDID_XPATH_TEMPLATE = '//*[@id="app"]/div[2]/main/div/div[2]/div/div[1]/div[2]/div[TDNUM]/span[1]'
title_elements = list()
titles = list()
tdid_elements = list()
tdids = list()
for i in range(1, 41):
    ele1 = driver.find_element(By.XPATH, TITLE_XPATH_TEMPLATE.replace("TDNUM", str(i)));
    ele2 = driver.find_element(By.XPATH, TDID_XPATH_TEMPLATE.replace("TDNUM", str(i)));
    title_elements.append(ele1)
    tdid_elements.append(ele2)
for title_element in title_elements:
    titles.append(title_element.text)
for tdid_element in tdid_elements:
    tdids.append(tdid_element.text)
print("[LOG] 成功加载索引")
# print(titles)
# print(tdids)
TID_TEMPLATE = '//*[@id="app"]/div[2]/main/div/div[2]/div/div[1]/div[2]/div[TNUM]/span[2]'
cnt = 0
plancfg = list()
descriptions = list()
for tdid in tdids:
    print("[LOG] 加载编号: " + tdid)
    cnt += 1
    tids = list()
    driver.get("https://www.luogu.com.cn/training/" + tdid)
    eleone = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div[2]/section[2]/div/div[2]')
    descriptions.append(eleone.text)
    tab2 = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div[1]/div/ul/li[2]/span')
    tab2.click()
    totalnum_ele = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/span[2]')
    for i in range(1, int(totalnum_ele.text)):
        tidone = driver.find_element(By.XPATH, TID_TEMPLATE.replace("TNUM", str(i)))
        tid = tidone.text
        tids.append("LG" + tid) # 适配 XJYOJ
    totalinf = dict()
    totalinf = {"_id": cnt, "title": titles[cnt - 1], "requireNids": [], "pids": tids}
    plancfg.append(totalinf)
markdown_description = ""
for i,j in zip(descriptions, titles):
    markdown_description += "\n"
    markdown_description += "## "
    markdown_description += j
    markdown_description += "\n"
    markdown_description += i
jsoncfg = json.dumps(plancfg)
with open('cfg.json', 'w') as file1:
    file1.write(jsoncfg)
with open('description.md', 'w') as file2:
    file2.write(markdown_description)
with codecs.open('cfg.json', 'r', encoding='unicode_escape') as f:
    content = f.read()
with codecs.open('cfg.json', 'w', encoding='utf-8') as f:
    f.write(content)
with open('description.md', 'r') as f:
    content = f.read()
modified_content = content.replace('\n', '  \n')
with open('description.md', 'w') as f:
    f.write(modified_content)
driver.quit()
