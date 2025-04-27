from bs4 import BeautifulSoup

with open("index.html", "r") as file:
    content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    # get dom with classname recommend-ware

    recommend_ware = soup.find_all("div", class_="recommend-ware")

    for dom in recommend_ware:
        # get content under recommend-ware
        content = dom.find_all("div", class_="content")
        # <a class = "title" href = "https://rent.591.com.tw/18685808" target = "_blank"
        #                                     data-v-93fbb22b > 竹科園區金山街精品*大套房*私人陽台及機車位 < /a >
        #                                 <div class="address-info" data-v-93fbb22b><span class="address"
        #                                         data-v-93fbb22b><span class="community" data-v-93fbb22b>金山街 竹科
        #                                             金山社區</span><span data-v-93fbb22b>東區-金山十八街</span></span><!----><span
        #                                         class="area" data-v-93fbb22b>8.5坪</span></div><!---->
        #                                 <div class="price-info" data-v-93fbb22b><span class="price font-arial"
        #                                         data-v-93fbb22b>14,500</span><span class="unit"
        #                                         data-v-93fbb22b>元/月</span></div>

        # get title
        title = content[0].find("a", class_="title").text
        # get price
        price = content[0].find("span", class_="price").text
        # get area
        area = content[0].find("span", class_="area").text
        # get address
        address = content[0].find("span", class_="address").text

        print("title: ", title)
        print("price: ", price)
        print("area: ", area)
        print("address: ", address)
        print("=====================================")
        