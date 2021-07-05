import requests
from bs4 import BeautifulSoup


def writeToFile(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.close()


def getHTML(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    return html.prettify()
