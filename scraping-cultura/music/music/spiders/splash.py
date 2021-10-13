import scrapy
from scrapy_splash import SplashRequest


class SpashSpider(scrapy.Spider):
    name = 'splash'

    lua_script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://www.cultura.com/musique/genres-musicaux.html?p=1',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.lua_script,
            }
        )
        
    def parse(self, response):
        print(response.body)