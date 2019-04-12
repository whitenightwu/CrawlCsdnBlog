# from urllib.request import urlopen
from bs4 import BeautifulSoup
import tomd
from urllib import urlopen

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

url = 'https://blog.csdn.net/wydbyxr/article/details/81024079'
html = urlopen(url)
bsObj = BeautifulSoup(html, 'html.parser')

md = bsObj.find('div', {'class': 'article_content'})
print(md.prettify())
convert = tomd.convert(md.prettify())
with open('TestTomd.md', 'w') as f:
    f.write(convert)
