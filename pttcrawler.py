import urllib.parse
from requests_html import HTML
import requests
from bs4 import BeautifulSoup
import time
requests.packages.urllib3.disable_warnings()


searches = ['張小虹', '廖彥棻', '黃馨瑩', '黃恆綜', '楊乃冬', '張嘉倩']
title = "大一英文"
num_pages = 1


# =========================================================
search_endpoint_url = 'https://www.ptt.cc/bbs/NTUcourse/search?page=1&q='
domain = 'https://www.ptt.cc/'


def parse_article_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries


def parse_article_meta(ent):
    try:
        link = ent.find('div.title > a', first=True).attrs['href']
        return link
    except AttributeError:
        return None


def get_metadata_from(url):

    def parse_next_link(doc):
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return link
    resp = requests.get(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)
    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link


def get_paged_meta(url, num_pages):
    collected_meta = []

    for i in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin(domain, link)
        print("parsing pages...(%d/%d)" % (i+1, num_pages))

    return collected_meta


def crawl_pages(searches=searches, title=title, numPages=num_pages):
    print('====================START====================')

    URLlist = []
    x = 0
    for search in searches:
        x += 1
        print("searching pages data...(%d/%d)" % (x, len(searches)))
        start_url = search_endpoint_url + search
        URLlist += get_paged_meta(start_url, numPages)

    # =========================================================
    strNext = "\n\n\n\n************************下一篇************************\n\n\n\n\n"
    content = ''
    i = 0
    for URL in URLlist:
        i += 1
        URL = urllib.parse.urljoin(domain, URL)
        res = requests.get(URL, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.select('.bbs-screen.bbs-content')[0].text
        content += (data + strNext)
        time.sleep(0.05)
        print("searching individual data...(%d/%d)" % (i, len(URLlist)))
    print('====================CrawlEnded====================')
    return content


def write_pages(content):
    with open(title+'.txt', 'wb') as f:
        f.write(content.encode('utf8'))


# =========================================================
if __name__ == '__main__':
    write_pages(crawl_pages(searches, title, num_pages))
