import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class BoulangerSpider(scrapy.Spider):
    name = "boulanger"
    allowed_domains = ["boulanger.com"]
    base_url = "https://www.boulanger.com"
    start_urls = [
        base_url + '/c/tous-les-ordinateurs-portables'
    ]
    src_no_image = "src-no-image"

    def parse(self, response):
        url_next_page = response.xpath('//div[' + utils.xpath_class('navigationListe') + ']//span[' + utils.xpath_class('navPage navPage-right') + ']/a/@href').extract_first()
        if url_next_page is not None:
            yield Request(self.base_url + url_next_page, callback=self.parse)

        if not response.xpath('//h1[@itemprop="name"]/text()').extract():
            urls = response.xpath('//div[' + utils.xpath_class('productListe') + ']//div[' + utils.xpath_class('designations') + ']/h2/a/@href').extract()
            for url in urls:
                url = self.base_url + url
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//div[@id="filAriane"]//li[2]//a/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//div[@id="filAriane"]//li[position() >= 3 and position() <= last()]//a/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            name = re.sub(' +', ' ', ''.join(response.xpath('//h1[@itemprop="name"]/text()').extract()).replace('\n', '').replace('\r', '').strip())

            price_old = response.xpath('//div[' + utils.xpath_class('informations') + ']//div[' + utils.xpath_class('price') + ']/span[' + utils.xpath_class('productStrikeoutPrice on') + ']//span[' + utils.xpath_class('exponent') + ']/text()').extract_first()
            price_cent_old = response.xpath('//div[' + utils.xpath_class('informations') + ']//div[' + utils.xpath_class('price') + ']/span[' + utils.xpath_class('productStrikeoutPrice on') + ']//sup/span[' + utils.xpath_class('fraction') + ']/text()').extract_first()

            if price_old is not None:
                if price_cent_old is not None:
                    price_old = utils.string_to_float((price_old.strip() + "," + price_cent_old.strip()).replace(" ", ""))
                else:
                    price_old = utils.string_to_float(price_old.strip().replace(" ", ""))

            price = response.xpath('//div[' + utils.xpath_class('price') + ']/p/span[' + utils.xpath_class('exponent') + ']/text()').extract_first()
            price_cent = response.xpath('//div[' + utils.xpath_class('price') + ']/p/sup/span[' + utils.xpath_class('fraction') + ']/text()').extract_first()

            if price is not None:
                if price_cent is not None:
                    price = utils.string_to_float((price.strip() + "," + price_cent.strip()).replace(" ", ""))
                else:
                    price = utils.string_to_float(price.strip().replace(" ", ""))

            currency = response.xpath('//div[' + utils.xpath_class('price') + ']/p/sup/text()').extract_first()
            if currency is not None:
                currency = utils.get_currency_code(currency.strip())

            src = response.xpath('//span[@itemprop="gtin13"]/text()').extract_first().strip()
            if src is not None:
                src = "https://boulanger.scene7.com/is/image/Boulanger/" + src + "_h_f_l_0"

            item['store'] = self.name
            item['url'] = response.url
            item['main_category'] = main_category
            item['categories'] = categories
            item['brand'] = None
            item['openssl_hash'] = utils.generate_open_ssl_hash(item['url'])
            item['name'] = name
            item['price_old'] = price_old
            item['price'] = price
            item['currency'] = currency
            item['price_info'] = None
            item["image_urls"] = [src]
            item["image_name"] = item['openssl_hash']
            item["rate"] = None
            item["max_rate"] = None
            item["nb_avis"] = None

            if src == self.src_no_image:
                copyfile("data/default.jpg", "data/" + self.name + "/img/" + item["image_name"] + ".jpg")

            yield item
