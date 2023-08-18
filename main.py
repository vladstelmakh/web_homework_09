import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'quote': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

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
    print('Виберіть що ви хочете отримати \n'
          '1)quotes.json\n'
          '2)authors.json\n')
    choose=int(input('->'))
    from scrapy.crawler import CrawlerProcess
    if choose==1:
        process = CrawlerProcess(settings={
            'FEED_FORMAT': 'json',
            'FEED_URI': 'quotes.json',
        })
        process.crawl(QuotesSpider)
        process.start()
    elif choose==2:
        process1 = CrawlerProcess(settings={
            'FEED_FORMAT': 'json',
            'FEED_URI': 'authors.json',
        })
        process1.crawl(AuthorSpider)
        process1.start()
    else:
        print('Try again')
