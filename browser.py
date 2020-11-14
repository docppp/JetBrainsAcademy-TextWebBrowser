import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Style

init()
args = sys.argv
user_input = input()
page_history = []


def saveWebPageToFile(page_address, page_text):
    file = args[1] + '/' + (page_address[8:].replace('/', '_').replace('.', '_'))
    with open(file, 'w') as f:
        f.write(page_text)


def checkWebPageHttps(page_address):
    if not page_address.startswith("https://"):
        return "https://" + page_address
    return page_address


def extractAndColorWebPageText(page_address):
    page_text = ''
    r = requests.get(page_address)
    soup = BeautifulSoup(r.content, 'html.parser')
    paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    for paragraph in paragraphs:
        if paragraph.name == 'a':
            page_text += '\033[34m' + paragraph.text + '\033[39m\n'
        else:
            page_text += paragraph.text + "\n"
    return page_text


def handleWebPage(page_address):
    page_address = checkWebPageHttps(page_address)
    page_text = extractAndColorWebPageText(page_address)
    print(Fore.BLUE + page_text)
    page_history.append(page_address)
    saveWebPageToFile(page_address, page_text)


if len(args) == 2:
    os.makedirs(args[1], exist_ok=True)

while user_input != 'exit':

    if user_input == 'back':
        try:
            page_history.pop()
            user_input = page_history.pop()
        except IndexError:
            pass

    if '.' in user_input:
        handleWebPage(user_input)
    else:
        print('Error')

    user_input = input()
