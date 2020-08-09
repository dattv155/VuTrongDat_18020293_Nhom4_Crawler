import scrapy
import json

OUTPUT_FILE = '/home/trongdat/PycharmProjects/VuTrongDat_18020293_Nhom4_Crawler/Output/fptshop_phone.json'


class FptshopPhoneSpider(scrapy.Spider):
    name = 'fptshop_phone'
    allowed_domains = ['fptshop.com.vn']
    start_urls = ['https://fptshop.com.vn']

    COUNT = 0

    def parse(self, response):
        if self.COUNT >= 200:
            return
        if response.status == 200 and response.xpath('//meta[@name="pageType"]/@content').get() == 'productPage':
            name = response.xpath('//div[@class="fs-dtt-col1"]/h1[@class="fs-dttname"]/text()').get()
            company = response.xpath('//meta[@name="adx:sections"]/@content').get().split('/')[-1]
            if response.xpath('//div[@class="fs-dtinfo"]/div[@class="fs-pr-box"]/*[1]/@class').get() == "fs-gsocul clearfix":
                now_price = response.xpath('//div[@class="fs-dtinfo"]/div[@class="fs-pr-box"]//strong/text()').get()
            else:
                now_price = response.xpath('//div[@class="fs-dtinfo"]/div[@class="fs-pr-box"]/p/text()').get().strip()
            rate = response.xpath('//div[@class="fs-dtrt-col fs-dtrt-c1"]/h5/text()').get()
            num_comment = response.xpath('//div[@class="fs-dtrt-col fs-dtrt-c1"]/p/text()').get().split(' ')[0]
            promotion = '. '.join(response.xpath('//div[@class="fk-main"]/div/ul/li/text()').extract())
            url = response.xpath('//meta[@property="og:url"]/@content').get()
            img = response.xpath('//div[@class="easyzoom"]/a/@href').get().lstrip('/')
            description = response.xpath('//meta[@itemprop="description"]/@content').get()
            keywords = response.xpath('//meta[@name="keywords"]/@content').get()
            # accessories = response.xpath('//div[@class ="fs-trhcj fancybox-access-box"]/text()').get().strip()

            screen = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[0]
            front_camera = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[1]
            rear_camera = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[2]
            ram = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[3]
            memory = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[4]
            battery = response.xpath('//div[@class="fs-dtbox main_spec"]/div[2]//li/span/text()').extract()[7]

            data = {
                'name': name,
                'company': company,
                'now_price': now_price,
                'rate': rate,

                'screen': screen,
                'front_camera': front_camera,
                'rear_camera': rear_camera,
                'ram': ram,
                'memory': memory,
                'battery': battery,

                'num_comment': num_comment,
                'promotion': promotion,
                'url': url,
                'img': img,
                'description': description,
                'keywords': keywords,
            }

            with open(OUTPUT_FILE, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.COUNT += 1
                self.crawler.stats.set_value('CRAWLER_COUNT', self.COUNT)

        yield from response.follow_all(css='a[href^="https://fptshop.com.vn/dien-thoai"]::attr(href), a[href^="/dien-thoai"]::attr(href)', callback=self.parse)
        #yield from response.follow_all(xpath='//a[starts-with(@href, "https://baomoi.com"], //a[starts-with(@href, "/")]', callback=self.parse)

