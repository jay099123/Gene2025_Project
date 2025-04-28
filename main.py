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


def parse_content(content):
    """
    Parse content
    :param content: content
    :return: None
    """

    """
    recommend-ware：每一筆物件資料都有的部分
    ，用來找出每一筆物件的位置(搜尋有20個表每一頁有20筆資料)
    """


    soup = BeautifulSoup(content, "html.parser")
    # find all items
    recommend_ware = soup.find_all("div", class_="recommend-ware")

    data = []

    for dom in recommend_ware:
        # get content under recommend-ware
        content = dom.find_all("div", class_="content")

        title = content[0].find("a", class_="title").text
        price = content[0].find("span", class_="price").text
        # area = content[0].find("span", class_="area").text
        areas = content[0].find_all("span", class_="area")
        area = areas[len(areas)-1].text
        address = content[0].find("span", class_="address").text
        url = content[0].find("a", class_="title")["href"]

        data.append({
            "title": title,
            "price": price,
            "area": area,
            "address": address,
            "url": url
        })

    return data


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

    first_page = requests.get("https://rent.591.com.tw/list?region=4", headers=headers, cookies=cookie, verify=False)
    soup = BeautifulSoup(first_page.text, "html.parser")

    links = soup.find_all("a")
    filtered_links = filter(lambda link: "/list?region=4" in link["href"], links)
    filtered_links = list(filtered_links)
    print("filtered_links: ", filtered_links[-2].text)

    total_pages = int(filtered_links[-2].text)

    # for i in range(1, total_pages+1):
    for i in range(1, 3):

        if i == 1:
            urls.append("https://rent.591.com.tw/list?region=4")
        else:
            urls.append("https://rent.591.com.tw/list?region=4&page=" + str(i))

    return urls


if __name__ == "__main__":
    # get url
    urls = get_urls()

    for url in tqdm(urls):
        # print("get url: ", url)
        # get content
        content = get_content(url)
        # print("get content")
        # parse content
        results = parse_content(content)
        # print("parse content")

        # for result in results:
        #     print("title: ", result["title"])
        #     print("price: ", result["price"])
        #     print("area: ", result["area"])
        #     print("address: ", result["address"])
        #     print("url: ", result["url"])
        #     print("=====================================")
