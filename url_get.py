import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# urlJumpIp=1; Domain=.591.com.tw; Path=/; Expires=Mon, 27 Apr 2026 10:37:46 GMT

cookie = {
    "urlJumpIp": "1",
    "Domain": ".591.com.tw",
    "Path": "/",
    "Expires": "Mon, 27 Apr 2026 10:37:46 GMT"
}


def parse_content(content, df):
    """
    Parse content
    :param content: content
    :return: None
    """
    soup = BeautifulSoup(content, "html.parser")

    href_list = []

    for idx, row in df.iterrows():
        expected_title = str(row["title"]).strip()
    
        if not expected_title or expected_title.lower() == "nan":
            print(f"第 {idx+1} 筆 : 資料無效(空白或NaN)\n")
            continue
        
        # 精確搜尋 title 屬性
        matches = soup.find_all("a", title=lambda t: t and expected_title in t)
    
        if matches:
            found = False
            for tag in matches:
                href = tag.get("href", "").strip()
                if href:
                    # print(f"第 {idx+1} 筆：成功找到標題包含「{expected_title}」")
                    # print(f"連結：{href}\n")
                    # href_list.append(href)
                    href_list.append({
                        "title": row["title"],
                        "price": row["price"],
                        "area": row["area"],
                        "address": row["address"],
                        "url": href
                      })
                    found = True
            if not found:
                print(f"第 {idx+1} 筆：找到符合標題「{expected_title}」，但無 href\n")
                # continue
        else:
            # print(f"第 {idx+1} 筆：找不到任何 title 包含「{expected_title}」的連結\n")
            continue

    # print(href_list)

    return href_list

def get_content(url):
    """
    Get content from url
    :param url: url
    :return: content
    """

    response = requests.get(url, headers=headers, cookies=cookie, verify=False)

    # print("content got: ", response.status_code)
    return response.text


def get_urls():

    urls = []

    # get total pages
    # total pages : 網站底下總共有幾頁(表可隨時間更新資料)

    first_page = requests.get("https://rent.591.com.tw/list?region=4&kind=2",
                              headers=headers, cookies=cookie, verify=False)
    soup = BeautifulSoup(first_page.text, "html.parser")

    links = soup.find_all("a")
    filtered_links = filter(
        lambda link: "/list?region=4&kind=2" in link["href"], links)
    filtered_links = list(filtered_links)
    print("filtered_links: ", filtered_links[-2].text)

    total_pages = int(filtered_links[-2].text)

    for i in range(1, total_pages+1):
    # for i in range(1, 2):

        if i == 1:
            urls.append("https://rent.591.com.tw/list?region=4&kind=2")
        else:
            urls.append("https://rent.591.com.tw/list?region=4&kind=2&page=" + str(i))

    return urls


if __name__ == "__main__":
    # get url
    urls = get_urls()

    houses = []

    df = pd.read_csv("活頁簿2.csv", encoding="utf-8-sig")

    if "url" not in df.columns:
        df["url"] = ""

    for url in tqdm(urls):

        content = get_content(url)

        results = parse_content(content, df)
    

        # print(results)

        for result in results:
            # houses.append({
            #     "title": result["title"],
            #     "price": result["price"],
            #     "area": result["area"],
            #     "address": result["address"],
            #     "url": result["url"]
            # })

            # 更新原本 df 中對應 title 的 url 欄位
            df.loc[df["title"] == result["title"], "url"] = result["url"]
            # 也可選擇同步存進 houses（如需 json 輸出）
            houses.append(result)
    # dump json to file with numpy
    json_dump = json.dumps({"houses": houses}, ensure_ascii=False, indent=4)

    with open("591.json", "w", encoding="utf-8-sig") as f:
        f.write(json_dump)
        print("json dump to file: 591.json")
    
    # 新增：存成 csv
    df.to_csv("活頁簿2.csv", index=False, encoding="utf-8-sig")

    print("已將資料存成 活頁簿2.csv")

