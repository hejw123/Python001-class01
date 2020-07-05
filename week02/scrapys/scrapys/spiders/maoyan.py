import scrapy
import time
from scrapy import Selector
from scrapys.items import MaoyanItem
from selenium import webdriver

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def __init__(self):
        try:
            browser = webdriver.Chrome()
            browser.get('https://passport.meituan.com/account/unitivelogin')
            time.sleep(1)

            # 输入账号和密码
            browser.find_element_by_xpath('//*[@id="login-email"]').send_keys('13552656607')
            browser.find_element_by_xpath('//*[@id="login-password"]').send_keys('')
            time.sleep(1)

            # 点击登陆
            browser.find_element_by_xpath('//*[@id="J-normal-form"]/div[5]/input[5]').click()

            cookie = browser.get_cookies()
            self.headers(cookie)
        except Exception as e :
            print("----获取header头失败，可能会抓取失败！----")
            print(e)
        finally:
            browser.close()

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//*[@class="movie-item film-channel"]')
        for movie in movies :
            link = "https://maoyan.com" + movie.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=link,callback=self.parse2)

    def parse2(self ,response):
        item = MaoyanItem()
        time = Selector(response=response).xpath('//div[3]/div/div[2]/div[1]/ul/li[3]/text()').extract_first()
        name = Selector(response=response).xpath('//div[3]/div/div[2]/div[1]/h1/text()').extract_first()
        list_t = ""
        tyeps = Selector(response=response).xpath('//div[3]/div/div[2]/div[1]/ul/li[1]/a')
        for type in tyeps :
            list_t = list_t + type.xpath('./text()').extract_first()

        item['time'] = time
        item['name'] = name
        item['type'] = list_t.strip()
        yield item
