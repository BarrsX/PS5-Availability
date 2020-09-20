import requests
from bs4 import BeautifulSoup
from plyer import notification
import pandas as pd

data = {'Amazon': ['No'],
        'Best Buy': ['No'],
        'WalMart': ['No']}

df = pd.DataFrame(data, columns=['Amazon', 'Best Buy', 'WalMart'])
print(df)

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
amazon_value = avail.string

if (amazon_value.strip()) != 'Currently unavailable.':
    notification.notify(
        title='PS5 Available',
        message='A PS5 is available on Amazon',
        app_icon=None,
        timeout=10,
    )
    df['Amazon'] = df['Amazon'.replace('No', 'Yes')]
else:
    df['Amazon'] = df['Amazon'.replace('No', 'Yes')]

bestbuy = Page('https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161')
bb = bestbuy.req()
bbAvail = bb.find("button", attrs={'class': 'btn btn-disabled btn-lg btn-block add-to-cart-button'})
bb_value = bbAvail

if (bb_value.strip()) != 'Coming Soon':
    notification.notify(
        title='PS5 Available',
        message='A PS5 is available on Best Buy',
        app_icon=None,
        timeout=10,
    )
    df['Best Buy'] = df['Best Buy'.replace('No', 'Yes')]
else:
    df['Best Buy'] = df['Best Buy'.replace('No', 'Yes')]

walmart = Page('https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815')
wm = walmart.req()
walmartAvail = wm.find("span", attrs={'class': 'display-block-xs font-bold'})
wm_value = walmartAvail

if (wm_value.strip()) != 'Out of stock':
    notification.notify(
        title='PS5 Available',
        message='A PS5 is available on WalMart',
        app_icon=None,
        timeout=10,
    )
    df['WalMart'] = df['WalMart'.replace('No', 'Yes')]
else:
    df['WalMart'] = df['WalMart'.replace('No', 'Yes')]

print(df)
