from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from os.path import basename, isfile
from time import sleep

FIRST_PAGE = 'https://minecraft.wiki/w/Category:InvSprite_files'
WIKI_BASE_URL = 'https://minecraft.wiki'
IMAGE_BASE_URL = 'https://minecraft.wiki/images/'
HEADERS={'User-Agent': "Minecraft Wiki inventory icons scraper"}

ICON_FOLDER = './invicon'

req = urlopen(Request(FIRST_PAGE, headers=HEADERS))
current_page = BeautifulSoup(req.read(), 'html.parser')

errored = False

while current_page != None and not errored:
    for icon in current_page.select('.mw-file-description'):
        icon_link = icon['href']
        icon_name = basename(icon_link).replace('File:', '')
        icon_image_url = IMAGE_BASE_URL + icon_name

        icon_out_fp = f'{ICON_FOLDER}/' + icon_name

        if not isfile(icon_out_fp):
            with open(icon_out_fp, 'wb') as f:
                res = urlopen(Request(icon_image_url, headers=HEADERS))
                if res.status != 200:
                    print(res.status)
                    errored = True
                f.write(res.read())
            sleep(0.25)
    
    next_page_link = current_page.find('a', href=True, string='next page')
    if next_page_link == None:
        current_page = None
    else:
        next_page_url = (WIKI_BASE_URL + next_page_link['href'])
        next_page_res = urlopen(Request(next_page_url, headers=HEADERS))
        if next_page_res.status != 200:
            print(next_page_res.status)
            errored = True
        current_page = BeautifulSoup(next_page_res.read(), 'html.parser')

    sleep(0.25)