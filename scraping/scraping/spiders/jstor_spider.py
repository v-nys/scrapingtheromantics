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
                                          formname='advSearchForm',
                                          formdata={'q0' : poet,
                                                    'f0' : 'ti'},
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
            fh.writelines(['# entries: {num}'.format(num=len(page_entries))])
            for entry in page_entries:
                # don't start searching from root!
                title = entry.select('//div[@class="title"]/a/text()').extract()
                fh.write(title)

