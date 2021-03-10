import os, sys
import scrapy
from scrapy.loader import ItemLoader
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
from items import NewsItem

def extract_text(s):
    s = s[s.find('>')+1:]
    s = s.replace('</p>','')
    s = s.replace('</a>','')
    while True:
        first = s.find('<')
        if first >= 0:
            last = s.find('>')
            s = s.replace(s[first:last+1],'')
        else:
            break
    return s

def transform(ps):
    l = []
    for s in ps:
        l.append(extract_text(s))
    res = ' '.join(l)
    return res

n = 1
class BasicSpider(scrapy.Spider):
    name = 'economics2'
    start_urls = ['https://g1.globo.com/economia/']

    def parse(self, response):
        global n
        print(n)
        for page in response.xpath("//*[@class='feed-post-body']//a/@href").getall():
            yield response.follow(page, self.parse_article)
        n += 1
        if n <= 2000:
            next_page = ("https://g1.globo.com/economia/index/feed/pagina-%d.ghtml" % (n))
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        p1 = response.xpath("//article//p[@class='content-text__container theme-color-primary-first-letter']").extract()
        p2 = response.xpath("//article//p[@class='content-text__container ']").extract()
        ps = p1 + p2
        text = transform(ps)
        l = ItemLoader(item = NewsItem(), response = response)
        l.add_value('link',  response.url)
        l.add_xpath('date',  "//time[@itemprop='datePublished']/text()")
        l.add_value('text',  text)
        l.add_xpath('title', "//h1[@class='content-head__title']/text()")
        return l.load_item()
