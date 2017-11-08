# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import tomd


# Parse one page's articles.
def parse_page(bsObj, url):
    articles = bsObj.findAll('div', {'class': 'article_item'})
    links = []
    for article in articles:
        links.append(article.h1.a.attrs['href'])
        print(links[-1])
        parse_article(urljoin(url, links[-1]))


# Parse one article.
def parse_article(url):
    global blogCount
    # 1. Open article site.
    html = urlopen(url)
    bsObj = BeautifulSoup(html, 'html.parser')

    # 2. Parse title and create directory with title.
    title = bsObj.h1.get_text()
    print('Article title is: %s' % title)
    convertTitle = replace_deny_char(title)
    blogCount += 1
    directory = 'CSDN Blog/%d.%s' % (blogCount, convertTitle)
    if os.path.exists(directory) is False:
        os.makedirs(directory)

    # 3. Parse and download images.
    images = bsObj.find('div', {'class': 'article_content'}
                        ).findAll('img')
    count = 0
    for img in images:
        count += 1
        imgUrl = urljoin(url, img.attrs['src'])
        print('Download image url: %s' % imgUrl)
        urlretrieve(imgUrl, '%s//%d.jpg' % (directory, count))

    # 4. Parse blog content and convert html to markdown.
    parse_article_content(bsObj, directory, convertTitle)


# Parse article content and convert html to markdown.
def parse_article_content(bsObj, directory, title):
    # 1. Find html.
    html = bsObj.find('div', {'class': 'article_content'})
    md = tomd.convert(html.prettify())

    # 2. Write to the file.
    with open('%s/%s.md' % (directory, title), 'w', encoding='utf-8') as f:
        f.write(md)


# Replace deny char, used to name a directory.
def replace_deny_char(title):
    deny_char = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|', '：']
    for char in deny_char:
        title = title.replace(char, ' ')
    print('Convert title is: %s' % title)
    return title


print('Please input your CSDN name:')
name = input()
url = 'http://blog.csdn.net/%s' % name
blogCount = 0

while True:
    # 1. Open new page.
    html = urlopen(url)
    bsObj = BeautifulSoup(html, 'html.parser')
    print('Enter new page: %s' % url)

    # 2. Crawl every article.
    parse_page(bsObj, url)

    # 3. Move to next page.
    next_url = bsObj.find('a', text='下一页')
    if next_url is not None:
        url = urljoin(url, next_url.attrs['href'])
    else:
        break
