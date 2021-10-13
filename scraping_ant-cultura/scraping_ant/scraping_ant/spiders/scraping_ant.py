import http.client
import scrapy
from scrapy.selector import Selector


class ScrapingAntSpider(scrapy.Spider):
    name = 'scraping_ant'
    start_urls = []

    def start_requests(self):
        # conn = http.client.HTTPSConnection("api.scrapingant.com")
        # headers = {
        #     'x-api-key': "35fa15031e6047b698b29259c123263d"
        # }
        # conn.request("GET", "/v1/general?url=https%3A%2F%2Fwww.cultura.com%2Fmusique%2Fgenres-musicaux.html&proxy_type=residential&proxy_country=FR", headers=headers)
        # res = conn.getresponse()
        # data = res.read()
        # print(data.decode("utf-8"))
        yield scrapy.Request(
            url='https://api.scrapingant.com/v1/general?url=https%3A%2F%2Fwww.cultura.com%2Fmusique%2Fgenres-musicaux.html&proxy_type=residential&proxy_country=FR',
            callback=self.parse,
            headers={
                'x-api-key': "35fa15031e6047b698b29259c123263d"
            }
        )

    def parse(self, response):
        print(response.body)
        with open('cultura_music_p1.html', 'w') as f:
            f.write(response.text)
        # html = Selector(text=response)
        # yield {
        #     'marque': html.xpath('.//*[@class="product-name"]//text()').get(),
        #     'modele': html.xpath('.//*[@class="people peoplemin open"]//span/text()').get()
        # }
