import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://www.cultura.com/plus-loin-qu-un-reve-0190296533167.html']

    def parse(self, response):
        items = response.xpath('//*[@class="product-main-container"]')
        for item in items:
            yield {
                'marque': item.xpath('.//*[@class="product-name"]//text()').get(),
            }