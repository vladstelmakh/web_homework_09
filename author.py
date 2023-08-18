import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'fullname': extract_with_css('h3.author-title::text'),
            'born_date': extract_with_css('.author-born-date::text'),
            'description': extract_with_css('.author-description::text'),
            'born_location':extract_with_css('.author-born-location::text')
        }
if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json',
    })
    process.crawl(AuthorSpider)
    process.start()