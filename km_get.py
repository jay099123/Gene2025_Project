from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.common.keys import Keys  
import pandas as pd
from selenium.common.exceptions import TimeoutException


df = pd.read_csv("total_copy.csv", encoding="utf-8-sig")
kilo = []

## 啟用Options方法
options = Options()
## 關掉通知
options.add_argument(" - disable-notifications")
options.add_argument("--incognito")

chrome_browser = webdriver.Chrome()

chrome_browser.get("https://www.google.com.tw/maps?hl=zh-TW")
time.sleep(3)

# 獲得"路線"按鈕元素
route_btn = chrome_browser.find_element(By.ID, "hArJGc")
# 觸發點擊事件
route_btn.click()
time.sleep(1)

vehicle_btn = chrome_browser.find_elements(By.CLASS_NAME, "m6Uuef")
vehicle_btn[2].click()

# 獲得"路線搜尋框"元素([0]:起, [1]:迄)
search_route_start = chrome_browser.find_elements(By.CLASS_NAME, "tactile-searchbox-input")
search_route_start[0].click()
search_route_start[0].send_keys("陽明交大機車停車棚H")
time.sleep(1)

search_route_start[1].send_keys("東區-富群街2號")
time.sleep(1)

search_route_start[1].send_keys(Keys.ENTER)
time.sleep(2)


# 找出距離，等待內部的 <div> 文字內容出現，例如「3.2 公里」
element = WebDriverWait(chrome_browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ivN21e.tUEI8e.fontBodyMedium > div"))
)

text = element.text
print(text)  # 3.2 公里

value, unit = text.strip().split()
print(value)  # 3.2
print(unit)   # 公里
kilo.append(value)

time.sleep(1)

for i in range(1, len(df)):
    time.sleep(1)
    # search_route_start[0].click()
    # time.sleep(1)
    # search_route_start[0].send_keys("陽明交大機車停車棚H")
    # time.sleep(2)
    search_route_start[1].click()
    time.sleep(1)
    search_route_start[1].send_keys(df.loc[i, "address"])  # 取得第i列的 title 欄
    time.sleep(1)
    search_route_start[1].send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        element = WebDriverWait(chrome_browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ivN21e.tUEI8e.fontBodyMedium > div"))
        )
        text = element.text
        value, unit = text.strip().split()
        kilo.append(value)
    except TimeoutException:
        print(f"第{i+1}筆：找不到距離，已略過")
        kilo.append("")
    # print(value)  # 3.2
    # print(unit)   # 公里

    

print(kilo)
df["distance"] = kilo
df.to_csv("total_copy.csv", index=False, encoding = "utf-8-sig")


# 等待用戶輸入，防止瀏覽器自動關閉
input("按下 Enter 鍵以關閉瀏覽器...")

# 關閉瀏覽器
chrome_browser.quit()


