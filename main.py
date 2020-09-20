import requests
from bs4 import BeautifulSoup
from plyer import notification

headers = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                'Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


class Page:
    def __init__(self, url):
        self.url = url

    def req(self):
        webpage = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(webpage.content, "lxml")
        return soup


amazon = Page(
    'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=sr_1_1?dchild=1&keywords=ps5&qid=1600547494&sr=8-1&th=1')
ps5 = amazon.req()
avail = ps5.find("span", attrs={"class": 'a-size-medium a-color-price'})
avail_value = avail.string

if (avail_value.strip()) == 'Currently unavailable.':
    notification.notify(
        title='PS5 Available',
        message='A PS5 is available on Amazon',
        app_icon=None,
        timeout=10,
    )
