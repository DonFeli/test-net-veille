#  Install the Python ScrapingBee library:
# `pip install scrapingbee`
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='EK4ORXQHWDH2XJDOY6F54JHXNIEORC6EBUE067H3K9EJ568QH752VKO3MGXWEBB6VS62P1KH3RBMKTT3')
response = client.get(
    'https://www.cultura.com/musique/genres-musicaux.html?p=1',
    params={
        'premium_proxy': 'true',
        'country_code': 'fr',
        'js_scroll_wait': '8000',
        'js_scroll_count': '3',
    },
)
print('Response HTTP Status Code: ', response.status_code)
print('Response HTTP Response Body: ', response.content)