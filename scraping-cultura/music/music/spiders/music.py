import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from urllib.parse import urlencode
import requests
import re
import time
import sys
import os
from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class MusicSpider(scrapy.Spider):
    name = 'music'
    main_url = 'https://www.cultura.com/musique/genres-musicaux.html'
    # captcha_url = 'https://geo.captcha-delivery.com/captcha/?initialCid=AHrlqAAAAAMAm_qLxJOJdBEAWSi3jg%3D%3D&hash=0E1A81F31853AE662CAEC39D1CD529&cid=DkOFGGGl8MDmoqxp7cTH5mMHqazYyqPLfb9cKyQu-SAe6MfAyhfiUJSSB-Q09LhIcK9p_.4K2xP9mRLjqQIV~xe.ALEXDtSolPH3Xw7Hix&t=fe&referer=https%3A%2F%2Fwww.cultura.com%2Fmusique%2Fgenres-musicaux.html&s=11861'
    # api_key = os.getenv('APIKEY_2CAPTCHA')
    config = {
        'server': '2captcha.com',
        'apiKey': 'f8fbdcdd87f4b36713721d35159ba510',
        'defaultTimeout': 120,
        'recaptchaTimeout': 600,
        'pollingInterval': 10,
    }
    solver = TwoCaptcha(**config)

    def start_requests(self):
        yield SeleniumRequest(
            url=self.main_url,
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        # items = response.xpath('//li[@class="item"]')
        # for item in items:
        #     yield {
        #         "modele": item.xpath('.//a[@class="product-image"]/@title').get()
        #     }
        print("INITIAL RESPONSE :\n", response.body)
        # html = response.meta['driver'].page_source
        # response_obj = Selector(text=html)

        captcha = response_obj.xpath('//div[@class="captcha"]').get()
        if captcha:
            try:
                result = self.solver.recaptcha(
                    sitekey='6LcSzk8bAAAAAOTkPCjprgWDMPzo_kgGC3E5Vn-T',
                    url=self.captcha_url,
                )
            except Exception as e:
                sys.exit(e)
            else:
                print(str(result))




            # request_input = requests.get(
            #     f"http://2captcha.com/in.php?key=f8fbdcdd87f4b36713721d35159ba510&method=userrecaptcha&googlekey"
            #     f"=6LcSzk8bAAAAAOTkPCjprgWDMPzo_kgGC3E5Vn-T&pageurl={self.captcha_url}")
            # id_2captcha = re.search("[0-9]+", request_input.text)
            #
            # request_result = requests.get(
            #     f"http://2captcha.com/res.php?key=f8fbdcdd87f4b36713721d35159ba510&action=get&id={id_2captcha.group(0)}")
            #
            # if request_result.text == 'CAPCHA_NOT_READY':
            #     time.sleep(5)
            #
            # elif request_result.text.startswith('OK'):
            #     print('SOLVED CAPTCHA :\n', request_result.text)
