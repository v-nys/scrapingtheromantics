class MuseSpider(BaseSpider)

    name = "muse"
    allowed_domains = ['muse.jhu.edu']
    start_urls = ['http://muse.jhu.edu/results']

    def parse(self, response):
        # not clear how to proceed yet
        # MUSE seems to use POST requests, need to figure out contents
        pass
