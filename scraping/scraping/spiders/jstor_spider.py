from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scraping.items import ArticleItem

# currently still a BaseSpider, not a CrawlSpider
# need to get a better feel for Scrapy first...
class JstorSpider(BaseSpider):
    name = "jstor"
    allowed_domains = ["jstor.org"]

    def parse(self, response):
        r"""
        Return items scraped (as `ArticleItem`s) and further
        pages to be scraped (as `Request`s).
        """
        filename = 'AdvancedSearch'
        hxs = HtmlXPathSelector(response)
        with open(filename, 'wb') as fh:
            fh.write(response.body)

    def start_requests(self)
        r"""
        Return an iterable containing the initial requests for
        the JStor spider.

        These requests are `FormRequest`s which use JStor's
        advanced search functionality.
        """
        return (FormRequest('http://www.jstor.org/action/showAdvancedSearch')
                for poet in ['Byron', 'Keats', 'Shelley'])
