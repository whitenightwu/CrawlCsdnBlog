# 一、引言
在昨天完成了：
[Web Scraping with Python: 使用 Python 下载 CSDN 博客图片](http://blog.csdn.net/u012814856/article/details/78470647)

的实例之后，我开始了思考：
> 可否实现一个导出 CSDN 博客全部文章以及附带图片资源的爬虫程序？

于是也就有了这篇博客。

这篇博客承接了上一篇博客的程序框架，在实现了 CSDN 指定用户博客的全部文章附带图片保存功能之后，又附带添加了博客文章内容的保存功能。

这将是一个非常令人激动不已的程序：
因为这将实现一个博客内容全部导出的功能！
这已然是一个有实际作用的爬虫程序了！

接下来，让我们开始吧：）

# 二、关键：怎样保存文章样式？
我们想要保存一篇博客文章的内容，不可能只单纯的保存纯文本吧。

一篇博客文章，有标题有标题有图片有各式各样的样式。我们要实现的这个爬虫程序，最主要的，就是要解决如何保留样式的保存博客文章的问题。

怎么办呢？

我们爬虫看到的永远都是页面的 Html 框架，那么从 Html，怎么样获取到有样式的文章呢？

**Markdown**

这个单词就像闪电一样划过了我的脑海，对！ Html 绝对是可以完美转换成 Markdown 的，通过 Markdown 观看文档是一件非常人性化的事情（这得益于我对于 Markdown 的偏爱，以至于我都是使用 Markdown 写博客的）。

那么，接下来我们要做的，就是如何将 Html 文本转换成阅读人性化的 Markdown 文件了。

# 三、Tomd 库：从 Html 到 Markdown 的上天之旅
其实从 Html 转换成 Markdown 的过程，我们是可以想象的，比如说：
```html
<h1>This is a title</h1>
```
上面的 Html 就可以转换成 Markdown 的
```
# This is a title
```
文本，这样，就简单实现了 Html 的 h1 标签向 Markdown 标签的转换。

理论上说我们可以这样完成 Html 到 Markdown 的转换，但是我们可是 Pythoner！遇到问题的第一步当然是寻找可以 import 到上天的库呀！

于是我找到了 Tomd。这是它的 GitHub 网址：
[gaojiuli/tomd](https://github.com/gaojiuli/tomd)

看了下作者，居然还是中国人！真是由衷的自豪。

通过观看作者的 ReadMe 介绍，我通过：
```
pip install tomd
```
安装了 Tomd 库。

然后简单写了一个 TestTomd.py 文件：
```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import tomd


url = 'http://blog.csdn.net/u012814856/article/details/78470647'
html = urlopen(url)
bsObj = BeautifulSoup(html, 'html.parser')

md = bsObj.find('div', {'class': 'article_content'})
convert = tomd.convert(md.prettify())
with open('TestTomd.md', 'w', encoding='utf-8') as f:
    f.write(convert)
```

这段代码：
**1.** 我首先使用了 urllib.request.urlopen 获取到了我的一篇博客的 Html 文本

**2.** 然后调用了 Tomd 库的 convert 方法将其转化成了 Markdown 文本

**3.** 最后我使用 with open 将这个 Markdown 文本写入了 .md 文件中

最后的结果是喜人的，看到了人性化的爬取结果：

![test](http://img.blog.csdn.net/20171108111119199?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjgxNDg1Ng==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

通过寻找到了 Tomd 库以及我们的测试程序，我们已经看到了爬取到博客文章并且保留样式的可能性，接下来，让我们直接导出全部的博客文章吧！

# 四、展示：简短的代码，强大的功能

由于这篇博客的大部分代码，包括博客全部文章的爬取以及资源的下载，都已经在上一篇博客中解释的非常清楚了，因此这里直接贴出我的代码，若有不清楚的，可以参看我的上一篇博客：
[Web Scraping with Python: 使用 Python 下载 CSDN 博客图片](http://blog.csdn.net/u012814856/article/details/78470647)

以下是我的全部代码：
```python
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

```

一共 90 多行代码，其中实现了 Html 转换成 Markdown 的关键逻辑的函数是 parse_article_content：
```python
# Parse article content and convert html to markdown.
def parse_article_content(bsObj, directory, title):
    # 1. Find html.
    html = bsObj.find('div', {'class': 'article_content'})
    md = tomd.convert(html.prettify())

    # 2. Write to the file.
    with open('%s/%s.md' % (directory, title), 'w', encoding='utf-8') as f:
        f.write(md)
```
这里尤其要注意写入文档的编码一定要是 utf-8，因此这里在 open 的传参中添加了 encoding 参数。

最后看下我们爬出来的结果吧：

爬出的文件夹（一篇博客一个）
![1](http://img.blog.csdn.net/20171108105551083?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjgxNDg1Ng==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![2](http://img.blog.csdn.net/20171108105603193?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjgxNDg1Ng==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

可见，这里我已经爬出了自己的全部的 159 篇博客信息，并且以编号标识，以博客标题命名了文件夹。

接下来，让我们看看文件夹里面有什么：
![3](http://img.blog.csdn.net/20171108105752622?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjgxNDg1Ng==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

可见，每一篇博客里面附带的图片都已经下载下来，并且生成了一个博客内容的 Markdown 文件：

![4](http://img.blog.csdn.net/20171108111131918?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjgxNDg1Ng==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

结果是非常令人欣喜的！

我们就用短短 90 行的代码，写出了一个强大的博客导出工具！

完结撒花 ^_^

# 五、总结
这是一个非常令人激动不已的爬虫程序。这意味着以后若是我想要保留我的所有博客内容，只需要跑一下这个爬虫程序即可（我之前还在担心要是 CSDN 停止运营了我的博客内容咋办 T_T）。

实践永远是最令人开心的，尤其是学习爬虫这一块。

当然了，学习爬虫之路远远没有走到尽头，还有好多需要学习和尝试。

Love Python,
To be Stronger：）
