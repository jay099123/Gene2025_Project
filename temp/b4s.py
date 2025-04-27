from bs4 import BeautifulSoup

with open("index.html", "r") as file:
    content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    