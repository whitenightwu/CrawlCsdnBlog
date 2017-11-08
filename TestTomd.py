from urllib.request import urlopen
from bs4 import BeautifulSoup
import tomd


url = 'http://blog.csdn.net/u012814856/article/details/78470647'
html = urlopen(url)
bsObj = BeautifulSoup(html, 'html.parser')

md = bsObj.find('div', {'class': 'article_content'})
convert = tomd.convert(md.prettify())
with open('TestTomd.md', 'w') as f:
    f.write(convert)
