import scrapy
import json

OUTPUT_FILE = '/home/trongdat/PycharmProjects/VuTrongDat_18020293_Nhom4_Crawler/Output/fptshop.json'


class FptshopSpider(scrapy.Spider):
    name = 'fptshop'
    allowed_domains = ['fptshop.com.vn']
    start_urls = ['https://fptshop.com.vn']

    COUNT = 0

    def parse(self, response):
        if response.status == 200 and response.xpath('//meta[@name="pageType"]/@content').get() == 'productPage':
            data = {
                'name': response.xpath('//div[@class="fs-dtt-col1"]/h1[@class="fs-dttname"]/text()').get(),
                'rate': response.xpath('//div[@class="fs-dtt-col1"]/div[@class="fs-dttrate"]/p[@class="active fs-dptrtq"]/a[1]/text()').get(),
                'url': response.xpath('//meta[@property="og:url"]/@content').get(),
                'description': response.xpath('//meta[@itemprop="description"]/@content').get(),
                'type': response.xpath('//meta[@name="adx:sections"]/@content').get(),
                'keywords': response.xpath('//meta[@name="keywords"]/@content').get(),
                'special_price': response.xpath('//div[@class="fs-dtinfo"]/div[@class="fs-pr-box"]//strong/text()').extract()[0],
                #'normal_price': response.xpath('//div[@class="fs-dtinfo"]/div[@class="fs-pr-box"]//strong/text()').extract()[1],
                'promotion': '. '.join(response.xpath('//div[@class="fk-main"]/div/ul/li/text()').extract()),
            }

            with open(OUTPUT_FILE, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.COUNT += 1
                self.crawler.stats.set_value('CRAWLER_COUNT', self.COUNT)

        # yield from response.follow_all(xpath='//a[starts-with(@href, "https://baomoi.com"], //a[starts-with(@href, "/")]', callback=self.parse)
        yield from response.follow_all(css='a[href^="https://fptshop.com.vn"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)
