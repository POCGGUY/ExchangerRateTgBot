from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

def parse():
    url = 'https://ru.investing.com/currencies/usd-rub'
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    print(page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    blockall = soup.find('div', class_ = 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')
    usd = blockall.string
    usd = usd.replace(',', '.')
    return usd

