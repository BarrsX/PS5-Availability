import requests
from random import choice
from bs4 import BeautifulSoup
from plyer import notification
import pandas as pd

data = {'Amazon': ['No'],
        'Best Buy': ['No'],
        'WalMart': ['No']}

df = pd.DataFrame(data, columns=['Amazon', 'Best Buy', 'WalMart'])

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
                'Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))}
    return proxy


print(proxy_generator())


class Page:
    def __init__(self, url):
        self.url = url

    def req(self):
        webpage = requests.get(self.url, proxies=proxy_generator(), headers=headers)
        soup = BeautifulSoup(webpage.content, "lxml")
        return soup


def check(url, name):
    amazon = Page(url)
    ps5 = amazon.req()
    print(ps5)
    avail = ps5.find("span", attrs={"class": 'a-size-medium a-color-price'})
    amazon_value = avail.string

    if (amazon_value.strip()) != 'Currently unavailable.' and (amazon_value.strip()) != 'Sold Out' and (
            (amazon_value.strip()) != 'Out of stock'):
        notification.notify(
            title='PS5 Available',
            message='A PS5 is available on {0}'.format(name),
            app_icon=None,
            timeout=10,
        )
        df[name] = df[name].replace({'No': 'Yes'})
    else:
        df[name] = df[name].replace({'Yes': 'No'})


check(
    'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=sr_1_1?dchild=1&keywords=ps5&qid=1600547494&sr=8-1&th=1',
    'Amazon')
check('https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161', 'Best Buy')
# check('https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815', 'WalMart')


print(df)
