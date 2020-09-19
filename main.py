import requests
from bs4 import BeautifulSoup

URL = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=sr_1_1?dchild=1&keywords=ps5&qid=1600547494&sr' \
      '=8-1 '
headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
amazon = requests.get(URL, headers=headers)
soup = BeautifulSoup(amazon.content, "lxml")
avail = soup.find("span", attrs={"class": 'a-size-medium a-color-price'})
avail_value = avail.string

if (avail_value.strip()) == 'Currently unavailable.':
    print('Unavailable')
