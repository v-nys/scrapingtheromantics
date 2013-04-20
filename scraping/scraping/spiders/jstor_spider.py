from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scraping.items import ArticleItem

class JstorSpider(BaseSpider):
    name = "jstor"
    allowed_domains = ["jstor.org"]
    start_urls = [
        "http://www.jstor.org/action/showAdvancedSearch"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
