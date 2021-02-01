import os, sys
import scrapy
from scrapy.loader import ItemLoader
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
from items import NewsItem

n = 1
class BasicSpider(scrapy.Spider):
    name = 'politics'
    start_urls = ['https://g1.globo.com/politica/']

    def parse(self, response):
        global n
        for page in response.xpath("//*[@class='feed-post-body']//a/@href").getall():
            yield response.follow(page, self.parse_article)
        n += 1
        if n <= 2000:
            next_page = ("https://g1.globo.com/politica/index/feed/pagina-%d.ghtml" % (n))
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        l = ItemLoader(item = NewsItem(), response = response)
        l.add_value('link',  response.url)
        l.add_xpath('date',  "//time[@itemprop='datePublished']/text()")
        l.add_xpath('title', "//h1[@class='content-head__title']/text()")
        l.add_xpath('text',  "//article//p/text()")
        l.add_xpath('text',  "//article//a/text()")
        return l.load_item()
