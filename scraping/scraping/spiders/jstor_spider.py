import re

from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scraping.items import ArticleItem

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
                for poet in ['Byron', 'Keats', 'Shelley'])

    def after_search(self, response):
        r"""
        Process search results by storing current page and generating
        a new `Request` for the next result page.
        """
        hxs = HtmlXPathSelector(response)
        
        # syntax for dates is not perfectly consistent
        # but the year is always followed by a ')'
        year_regex = re.compile(r"""(.+)((?P<year>[1-2][0-9][0-9][0-9])\))(.*)""")
 
        page_entries = hxs.select('//div[@class="unit size4of5"]')
        for entry in page_entries:
            item = ArticleItem()
            title_xpath = 'div[@class="hd"]/div[@class="title"]/a/text()'
            source_xpath = 'div[@class="bd"]/div[@class="srcInfo"]/text()'
            item['title'] = entry.select(title_xpath).extract()[0]
            source = entry.select(source_xpath).extract()[0]
            item['year'] = year_regex.match(source).group('year')
            yield item
        link_xpath = '//div[@class="pageResultsNav txtC prSearchRes"]/ul/li/a' 
        links = hxs.select(link_xpath)
        for link in links:
            text = link.select('text()').extract()
            if text and 'next' in text[0].lower():
                href = link.select('@href').extract()[0]
                url = 'http://www.jstor.org' + href
                yield Request(url, callback=self.after_search) 
                break # only need one instance of 'next' link
