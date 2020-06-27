import scrapy
from scrapy import Selector
from scrapys.items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

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
