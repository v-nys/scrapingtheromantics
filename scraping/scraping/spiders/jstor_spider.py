from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scraping.items import ArticleItem

# currently still a BaseSpider, not a CrawlSpider
# need to get a better feel for Scrapy first...
class JstorSpider(BaseSpider):
    name = "jstor"
    allowed_domains = ["jstor.org"]
    start_urls = ['http://www.jstor.org/action/showAdvancedSearch']

    def parse(self, response):
        r"""
        Process the start pages into new requests.
        """
        return (FormRequest.from_response(response,
                                          formdata={},
                                          callback=self.after_search)
                for poet in ['Byron', 'Keats', 'Shelley'])

    def after_search(self, response):
        r"""
        Process search results by storing current page and generating
        a new `Request` for the next result page.
        """
        with open('AdvancedSearch', 'wb') as fh:
            fh.write(response.body)
