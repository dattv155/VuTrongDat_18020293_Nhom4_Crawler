# -*- coding: utf-8 -*-
import scrapy
import json

OUTPUT_FILE = '/home/trongdat/PycharmProjects/VuTrongDat_18020293_Nhom4_Crawler/Output/baomoi.json'


class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    allowed_domains = ['baomoi.com']
    start_urls = ['https://baomoi.com']
    COUNT = 0

    def parse(self, response):
        if response.status == 200 and response.xpath('//meta[@property="og:type"]/@content').extract()[0] == 'article':
            data = {
                'href': response.xpath('//meta[@property="og:url"]/@content').extract()[0],
                'title': response.xpath('//meta[@property="og:title"]/@content').extract()[0],
                'description': response.xpath('//meta[@property="og:description"]/@content').extract()[0]
            }

            with open(OUTPUT_FILE, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.COUNT += 1
                self.crawler.stats.set_value('CRAWLER_COUNT', self.COUNT)

            #yield from response.follow_all(xpath='//a[starts-with(@href, "https://baomoi.com"], //a[starts-with(@href, "/")]', callback=self.parse)
        yield from response.follow_all(css='a[href^="https://baomoi.com"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)


