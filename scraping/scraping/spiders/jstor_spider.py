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

        This method will proceed to search for *articles* that have
        a particular poet's name in their *title*.
        """
        return (FormRequest.from_response(response,
                                          formname='advSearchForm',
                                          formdata={'q0' : poet,
                                                    'f0' : 'ti', # in title
                                                    'ar' : 'on'}, # articles
                                          callback=self.after_search)
                for poet in ['Byron'])

    def after_search(self, response):
        r"""
        Process search results by storing current page and generating
        a new `Request` for the next result page.
        """
        hxs = HtmlXPathSelector(response)
        page_entries = hxs.select('//div[@class="unit size4of5"]')
        with open('output', 'wb') as fh:
            for entry in page_entries:
                title_xpath = 'div[@class="hd"]/div[@class="title"]/a/text()'
                title = entry.select(title_xpath).extract()
                fh.write(str(title) + '\n')

