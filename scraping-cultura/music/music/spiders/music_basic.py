import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy_splash import SplashRequest
from twocaptcha import TwoCaptcha
import sys
import re
from urllib.parse import urlparse, parse_qsl, urlencode
from pprint import pprint


class MusicHeadless(scrapy.Spider):
    """
    Spider using scrapy-selenium and its middleware.
    doc: https://github.com/clemfromspace/scrapy-selenium
    """
    name = 'music_basic'
    target_url = 'https://www.cultura.com/musique/genres-musicaux.html'
    captcha_url = ''

    def start_requests(self):
        """
        Send initial request to target link with Selenium in order to execute javascript and avoid 403.
        """
        self.log('---------------------- Sending initial request to target website ----------------------')
        print(self.target_url)
        yield SeleniumRequest(
            url=self.target_url,
            wait_time=4,
            callback=self.check_captcha
        )

    @staticmethod
    def extract_request_headers(captcha_url):
        """
        Extract requests headers from the captcha api url.
        Structure of url = scheme://netloc/path;parameters?query#fragment
        Ref : https://docs.python.org/3/library/urllib.parse.html
        """
        parsed_captcha_url = urlparse(captcha_url)
        captcha_request_headers = dict(parse_qsl(parsed_captcha_url.query))
        print(captcha_request_headers)
        return captcha_request_headers

    def check_captcha(self, response):
        """
        Check if response contains a captcha. If so send new request to the captcha API.
        """
        self.log('---------------------- Checking for captcha ----------------------')
        self.captcha_url = response.xpath('//iframe[contains(@src, "captcha")]/@src').get()
        if self.captcha_url:
            self.log('---------------------- Captcha found ----------------------')
            yield SeleniumRequest(
                url=self.captcha_url,
                wait_time=3,
                callback=self.solve_captcha
            )
        # else:
        # self.log('---------------------- No captcha found ----------------------')
            # yield SeleniumRequest(
            #     url='https://www.cultura.com/musique/genres-musicaux.html',
            #     wait_time=4,
            #     callback=self.parse_target_website
            # )

    def solve_captcha(self, response):
        """
        Solve captcha with 2captcha API then send request with captcha response token.
        doc: https://2captcha.com/2captcha-api#solving_recaptchav2_new
        """
        self.log('---------------------- Solving captcha with 2captcha API ----------------------')
        captcha_data = response.xpath('//iframe[@title="reCAPTCHA"]/@src').get()
        match = re.search(r'(?<=k=)[\w-]*', captcha_data)
        sitekey = match.group(0)
        config = {
            'server': '2captcha.com',
            'apiKey': 'f8fbdcdd87f4b36713721d35159ba510',
            'defaultTimeout': 120,
            'recaptchaTimeout': 600,
            'pollingInterval': 10,
        }
        solver = TwoCaptcha(**config)

        try:
            captcha_response = solver.recaptcha(
                sitekey=sitekey,
                url=self.captcha_url,
            )
        except Exception as e:
            sys.exit(e)
        else:
            self.log('---------------------- Captcha solved. Captcha reponse : ----------------------')
            print(captcha_response)
            return self.send_captcha_response(captcha_response)

    def send_captcha_response(self, captcha_response):
        """
        Replicate the next requests made in the browser :
        1. A POST request with SplashRequest since Selenium can't send POST
           Ref : https://splash.readthedocs.io/en/stable/scripting-ref.html
        2. A GET Request
        """
        # # 1. POST www.google.com/recaptcha/api2/userverify
        # # Ref: https://developers.google.com/recaptcha/docs/verify
        # self.log('---------------------- Sending POST www.google.com/recaptcha/api2/userverify ----------------------')
        # lua_script = '''
        #     function main(splash, args)
        #         splash.private_mode_enabled = false
        #         splash:on_request(function(request)
        #             request:set_header('cookie', '_GRECAPTCHA=09AP3dVC3YkkNlgAyw7Y9uXCXpI2reQPfalVCIp6OJzQ-M0RiO2VxzWMUCc7Q48zPPXSAMMwbu3gs-oSGDAC7ahNo')
        #         end)
        #         splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        #         splash:go{
        #             splash.args.url,
        #             http_method=splash.args.http_method,
        #             body=splash.args.body
        #         }
        #         assert(splash:wait(5))
        #         return splash:html()
        #     end
        # '''
        # userverify_formdata = {
        #     'v': 'qljbK_DTcvY1PzbR7IG69z1r',
        #     'c': captcha_response,
        #     'response': 'eyJyZXNwb25zZSI6WzQsMiwzLDExXSwiZSI6ImJMQjNpa0RuRVkxc0h4Q0ludXl5T0IybnRIUFNDTDFVcVMwMTRYUk01RnQ5bUxQbjBKM2g1cUYwMjcyWkY0c0kyV18wYSJ9',
        #     't': '50347',
        #     'ct': '50347',
        #     'bg': '!NzGgMXzIAAZPdGyVT3RHHnf4ZNDMAqM-ACkAIwj8RtJT8no1wT5lhFxSRyke-byo61nmylLyJyP2UuwYpY95wqukBAcAAACRVwAAAANtAQecBhKYeePf_uEjb4CDqAK3U1i2w4gJL4gNvZ03XMpzJyWoJfsJx62tDbiP0fUtIfFkNNNtP5G7BQS7G9xJ72hZObjyeah1qRxDifOcFTneX5EHaiS0WJex9Oi1gsQqY69D5oyD0zESRXh6Qp0THZ1a6wDjMpoZoCTyGP9FqrBI-W4G0zKOdPdP3sXRwTH3pNXyoDpPUwaHV8MB6A1tq4lwNGDgwIk3MKXLgkgK8cxpP9AhrbdgNsHkEig69TlSG8m6FZoD5nAfPANtD9MpwYUL0MCWc45XxashdPkGGcHu4cVe45K41L92y6ZCfj39TYd54NGlslk6NI8VlFULYEkJ2ttbxAV0J1AJpcfd-jUkWdg7U40a1kCoMZPufUzyso66RYLH70vdII9QYMStLie6H9YLUaSD5KaUoF7ntm0g40YDiTnpwnvpYg6JBk5wDV_-A7G91ZWKpt5mRWqzf01HmoZpKP_qDrLFjgydEvabynW398jvNKHrzGNMiHm2ZQEMZqOVyKZq_kYEwyLRmrc_RSruskc-8EYHZPBWP1Mn3y0J4OiozMGw3jDRgfYxuL_jR0EvVQgWcN4vhDZf483zL0DC58CxEaQwBIcHrl72FY21aJqisvh5iFOahE5OtfX1fPvaUxzTHFi9n24BD4esWc9x6JzPY3Kl7VkHgHPmGXYh0WdyIsEF0IAcv5n27AfRmTsVEKeo6k11aVK6gBFA4LPoqT4slK0kmFrgzVV9owdgpCSX9ZPPkKXUMQNjdWT93tyU7NQ13xJJSDVoVmdETIjHb8xXV7U6gpUduApEVCpI8pnJcyK1Qd7aBaEo5LOsNcznTvbnryk06Van-pIdUHUyK1_r64gQdUz4HejQNNVQkm1tdL4gUSt_WgJ0Jf3rCTtNEh-hNnKcoBW3cCQXBhz3VkjEhHIgU_ahRBhX796EZxKtHJeSxZFU86BxlYEuKL93B7HsG5AD0hIAyFJfV5n3NzUT7jM6SPPpiXXqZGU0VYOryBdcXj4G8Dlohd6Mra6pXP95HSvlQCK1s_dhylipBms_wrGK3y77IO0hxJeKXcbtK6ejmfSZ80LiRAhGdsvrMCrN6W9rklCUyneO8LzRGZFv2d9Jb6TIWc2uqUBWz0cH0AyEpc0m0sg0qpnc0-4061wmUNr-UOvvuNY1972vFisiTedklQpezGjTMsFGfSIzNHFAewcxzvOpH9YaGRjPct3wPlTQT-jz_Wcm7gif_Tb0AG4UPc9IQRLuvce1Lm8zMiiKSYKoJcQZFQT5LJ9m7LOxSbF6QoOX31kD67GA3aBLIsx-4hz-I8ychhD0xcK507Rw9ZVD-pbt28BFSHeaUw_sOqA5W_sI1clEEngOJnsn15J6ih1wq0J5c4irzOrLqZEVlJLvWf4xOm6i-SbjKFPZBYnS5q3DzA3NvRK40CpAgFipVSQTye6zbOZMqaHNWS2-4_saNvBxxlulyx4Pb4iQkbqZZbdyFMma15SZ1Nkd4jrg6EjvGosDWGdFpAiw3SqAx54ySAQgTDqX9idE-l17SWyUzPVky1dGapHMpk561qA8276aiuR_8zKghr2XdmHY5vVvF4icmhNwGDbiCZbluE-ze9MhQTwE4ti-DHxAagobMiskATkLzXrf0JDlBPR5EHPfsze6JyMbWhepv9hHIXUwlYOngEi6Y3hLINPjcPF5VmGKXq2eI7k6Mn22bzNgdwvRWWnyRYt5lBo-V5M9PWsichkRhxSa_hBWKfbngvngIje3c5lIw86874wFi3fbITRgOG9nW8wAyCNtoTMCA-DIX9BQrCFwvhdM_yfRuxox9IT-bNXecbhNoct8XxVOvX8oxtTTQpIe4wYCLXbbSdedLZY3GDxPQaC-xnd6caOde-Whx4JmXnBYef601ajsYX5Ox-dclN0zIPkRiOHjg9LVmC-7355Vq1zeUfw6B_F_TfMut5aoBHjMMWactO6Ex7fg0bd0BXKopELtBy67J--JZeXaImJGjgLD8beCV8Hn1_rVOYosHmq_El0-ir9mSHYZt9DVROFC65Mnga5d8tDsAKML1_ax_Y5d41w'
        # }
        # pprint(userverify_formdata)
        # yield SplashRequest(
        #     url='https://www.google.com/recaptcha/api2/userverify?k=6LcSzk8bAAAAAOTkPCjprgWDMPzo_kgGC3E5Vn-T',
        #     callback=self.parse_splash,
        #     endpoint='execute',
        #     magic_response=True,
        #     meta={'handle_httpstatus_all': True},
        #     args={
        #         'lua_source': lua_script,
        #         'http_method': 'POST',
        #         'formdata': userverify_formdata
        #     }
        # )

        # 2. GET Request to geo.captcha-delivery.com/captcha/check
        self.log('---------------------- GET Request to geo.captcha-delivery.com/captcha/check ----------------------')
        captcha_headers = self.extract_request_headers(self.captcha_url)
        params = {
            'cid': captcha_headers['cid'],
            'icid': captcha_headers['initialCid'],
            'ccid': '',
            'g-recaptcha-response': captcha_response['code'],
            'hash': captcha_headers['hash'],
            'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'referer': captcha_headers['referer'],
            'parent_url': 'https://www.cultura.com/',
            # 'x-forwarded-for': '',
            'x-forwarded-for': '89.40.183.133',
            'captchaChallenge': captcha_response['captchaId'],
            's': captcha_headers['s']
        }
        pprint(params)
        check_url = 'https://geo.captcha-delivery.com/captcha/check?' + urlencode(params)
        pprint(check_url)
        yield SeleniumRequest(
            url=check_url,
            wait_time=5,
            callback=self.parse_cookie_response
        )

    def parse_cookie_response(self, response):
        """
        Browser cookies are identified and read by “name-value” pairs.
        These tell cookies where to be sent and what data to recall.
        your browser will send it back to the server to recall data from your previous sessions

        Unfortunately you can't change the UserAgent request header when using Selenium,
        I recommend you try with Splash.
        """
        self.log('---------------------- Cookie obtained : ----------------------')
        cookie_data = response.xpath('//pre/text()').get()
        print(cookie_data)
        # cookie = cookie_data['cookie']
        # print(cookie)
        matched_value = re.search(r'datadome=[^;]*', cookie_data)
        cookie_value = matched_value.group(0)
        print(cookie_value)
        return self.parse_captcha_after_submit(cookie_value)

    def parse_captcha_after_submit(self, cookie_value):
        self.log('---------------------- Sending request to target website with new cookie ----------------------')
        lua_script = '''
            function main(splash, args)
                url = args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                return splash:html()
            end
        '''
        yield SplashRequest(
            url=self.target_url,
            callback=self.parse_splash,
            endpoint='execute',
            args={
                'lua_source': lua_script,
                'splash_headers': {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                              'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept_encoding': 'gzip, deflate, br',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'cookie': cookie_value,
                    'referer': 'https://www.cultura.com/musique/genres-musicaux.html?p=1',
                    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': 'macOS',
                    'sec-ch-fetch-dest': 'document',
                    'sec-ch-fetch-mode': 'navigate',
                    'sec-ch-fetch-site': 'same-origin',
                    'sec-ch-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                }
            }
        )

    def parse_splash(self, response):
        print(response.request.headers)
        print(response.body)

    def scroll(self, response):
        pass
        # yield SeleniumRequest(
        #     url=url,
        #     callback=self.parse_result,
        #     script='window.scrollTo(0, document.body.scrollHeight);',
        # )