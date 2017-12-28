import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class CdiscountSpider(scrapy.Spider):
    name = "cdiscount"
    allowed_domains = ["cdiscount.com"]
    base_url = "https://www.cdiscount.com"
    start_urls = [
        base_url + '/informatique/ordinateurs-pc-portables/pc-portables/l-1070992.html'
    ]
    src_no_image = "src-no-image"
    nb_page = None

    def parse(self, response):

        if self.nb_page is None:
            self.nb_page = response.xpath('//ul[@id="PaginationForm_ul"]/li[last()]/a/text()').extract_first()
            if self.nb_page is not None:
                self.nb_page = self.nb_page.strip()
                for x in range(1, int(self.nb_page)):
                    yield Request(self.base_url + "/informatique/ordinateurs-pc-portables/pc-portables/l-1070992-" + str(x) + ".html", callback=self.parse)

        if not response.xpath('//h1[@itemprop="name"]/text()').extract():
            urls = response.xpath('//ul[@id="lpBloc"]//div[' + utils.xpath_class('prdtBloc') + ']/a/@href').extract()
            for url in urls:
                url = url.strip()
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//div[@id="bc"]//li[3]//span/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//div[@id="bc"]//li[position() >= 4 and position() < last()]//span/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            brand = response.xpath('//table[' + utils.xpath_class('fpDescTb fpDescTbPub') + ']//span[@itemprop="brand"]//span[@itemprop="name"]/text()').extract_first()
            if brand is not None:
                brand = brand.strip()

            name = re.sub(' +', ' ', response.xpath('//h1[@itemprop="name"]/text()').extract_first().strip())

            price_old = response.xpath('//div[@id="fpBlocPrice"]//span[' + utils.xpath_class('fpStriked') + ']/text()').extract_first()
            if price_old is not None:
                price_old = utils.string_to_float(re.sub(' .*$', '', price_old.strip()).replace(" ", ""))

            price = response.xpath('//div[@id="fpBlocPrice"]//span[' + utils.xpath_class('fpPrice price jsMainPrice jsProductPrice') + ']/@content').extract_first()
            if price is not None:
                price = utils.string_to_float(price.strip().replace(" ", ""))

            currency = response.xpath('//div[@id="fpBlocPrice"]//meta[@itemprop="priceCurrency"]/@content').extract_first()
            if price is not None:
                currency = currency.strip()

            src = response.xpath('//div[' + utils.xpath_class('fpMainImg') + ']/a[@itemprop="image"]/@href').extract_first().strip()

            rate_path = response.xpath('//div[' + utils.xpath_class('topMainRating') + ']')

            rate = rate_path.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            nb_avis = rate_path.xpath('//span[@itemprop="ratingCount"]/text()').extract_first()
            if nb_avis is not None:
                nb_avis = int(nb_avis.strip())

            item['store'] = self.name
            item['url'] = response.url
            item['main_category'] = main_category
            item['categories'] = categories
            item['brand'] = brand
            item['openssl_hash'] = utils.generate_open_ssl_hash(item['url'])
            item['name'] = name
            item['price_old'] = price_old
            item['price'] = price
            item['currency'] = currency
            item['price_info'] = None
            item["image_urls"] = [src]
            item["image_name"] = item['openssl_hash']
            item["rate"] = rate
            item["max_rate"] = 5
            item["nb_avis"] = nb_avis

            if src == self.src_no_image:
                copyfile("data/default.jpg", "data/" + self.name + "/img/" + item["image_name"] + ".jpg")

            yield item
