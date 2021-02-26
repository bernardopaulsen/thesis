"""
Title      : Splash Spider
Description: Spider to crawl Estadao.
Author     : Bernardo Paulsen
Versão     : 0.1.0
"""


import scrapy
from scrapy_splash import SplashRequest 

scrpt = """function main(splash)
    local element = splash:select('.element')
    local bounds = element:bounds()
    assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
end"""

class EconomicsSpider(scrapy.Spider):
    name = 'economics'
    start_urls = ['http://https://economia.estadao.com.br/']

    def start_requests(self): 
        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
           ) 

    def parse(self, response):
