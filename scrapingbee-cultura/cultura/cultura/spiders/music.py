import scrapy
from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest
import math


class MusicCulturaSpider(ScrapingBeeSpider):
    name = 'music_cultura'
    start_urls = [
        'https://www.cultura.com/musique/genres-musicaux.html?p=1',
    ]
    url='https://www.cultura.com/musique/genres-musicaux.html?p={page_number}'

    def start_requests(self):
        for url in self.start_urls:
            yield ScrapingBeeRequest(
                url,
                callback=self.access_product_page,
                params={
                    'premium_proxy': 'true',
                    'country_code': 'fr',
                    'render_js': 'true',
                    # 'js_scroll': 'true',
                    # 'js_scroll_count': '5',
                    # 'js_scroll_wait': '8000',
                    'transparent_status_code': 'true'
                }
            )

    # def parse_scrolled(self, response):
    #     print(response.body)
    #     items = response.xpath('//*[@class="item"]')
    #     for item in items:
    #         yield {
    #             'marque': item.xpath('.//*[@class="product-subtitle-b"]/text()').get(),
    #             'modele': item.xpath('.//*[@class="product-name"]//@title').get(),
    #         }

    def get_all_pages(self, response):
        print(response.body)
        products_total = response.xpath('//*[@class="amount"]/strong/text()').get()
        products_total = products_total.replace(' ', '')
        products_total = math.ceil(int(products_total))
        products_per_page = int(len(response.xpath('//*[@class="item"]').getall()))
        number_of_pages = int(products_total / products_per_page)

        for page_number in range(1, 10):
            yield ScrapingBeeRequest(
                url=self.url.format(page_number=page_number),
                callback=self.access_product_page,
                params={
                    'premium_proxy': 'true',
                    'country_code': 'fr',
                    'transparent_status_code': 'true'
                }
            )

    def access_product_page(self, response):
        print(response.body)
        product_link = response.xpath('//*[@class="product-item"]//@href').get()
        # for product_link in product_links:
        #     yield scrapy.Request(
        #         url=product_link,
        #         callback=self.parse_product_page
        #     )
        print(product_link)
        yield ScrapingBeeRequest(
            url=product_link,
            callback=self.parse_product_page,
            params={
                'premium_proxy': 'true',
                'country_code': 'fr',
                'transparent_status_code': 'true'
            }
        )

    def parse_product_page(self, response):
        print(response.body)
        yield {
            'marque': response.xpath('.//*[@class="product-name"]//text()').get(),
            'modele': response.xpath('.//*[@class="people peoplemin open"]//span/text()').get(),
            # 'ref_interne': item.xpath().get(),
            # 'ean': item.xpath().get(),
            # 'prix': item.xpath().get(),
            # 'prix_barre': item.xpath().get(),
            # 'promotion': item.xpath().get(),
            # 'stock': item.xpath().get(),
            # 'url': item.xpath().get(),
            # 'url_image': item.xpath().get(),
            # 'menu': item.xpath().get(),
            # 'page': item.xpath().get(),
            # 'position': item.xpath().get()
        }

