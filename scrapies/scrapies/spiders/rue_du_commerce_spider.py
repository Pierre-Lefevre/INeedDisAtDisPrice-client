import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class RueDuCommerceSpider(scrapy.Spider):
    name = "rue_du_commerce"
    allowed_domains = ["rueducommerce.fr"]
    base_url = "https://www.rueducommerce.fr"
    start_urls = [
        base_url + '/rayon/ordinateurs-64/pc-portable-5875'
    ]
    src_no_image = "src-no-image"
    nb_page = None

    def parse(self, response):

        url_next_page = response.xpath('//div[' + utils.xpath_class('results-header') + ']//a[' + utils.xpath_class('next') + ']/@href').extract_first()
        if url_next_page is not None:
            url_next_page = self.base_url + url_next_page.strip()
            yield Request(url_next_page, callback=self.parse)

        if not response.xpath('//h1/span[@itemprop="name"]/text()').extract():
            urls = response.xpath('//div[' + utils.xpath_class('products list') + ']//article/a/@href').extract()
            for url in urls:
                url = self.base_url + url.strip()
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//ol[' + utils.xpath_class('breadcrumb-chevron') + ']/li[1]//span/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//ol[' + utils.xpath_class('breadcrumb-chevron') + ']/li[position() >= 2 and position() < last()]//span/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            brand = response.xpath('//div[' + utils.xpath_class('productDetails') + ']/h1/span[' + utils.xpath_class('brand') + ']//span/text()').extract_first()
            if brand is not None:
                brand = brand.strip()

            name = re.sub(' +', ' ', ''.join(response.xpath('//div[' + utils.xpath_class('productDetails') + ']/h1//text()').extract()).replace('\n', '').replace('\r', '').strip())
            print(name)

            price_old = response.xpath('//div[' + utils.xpath_class('productBuy') + ']//div[' + utils.xpath_class('discount-prices') + ']//p[' + utils.xpath_class('price') + ']/text()').extract_first()
            if price_old is not None:
                price_old = utils.string_to_float(price_old[:-1].strip().replace(" ", "").replace(" ", ""))

            price = response.xpath('//div[' + utils.xpath_class('productBuy') + ']//div[' + utils.xpath_class('price main') + ']/p/text()').extract_first()
            price_cent = response.xpath('//div[' + utils.xpath_class('productBuy') + ']//div[' + utils.xpath_class('price main') + ']/p/sup/text()').extract_first()

            currency = None
            if price is not None:
                currency = utils.get_currency_code(price_cent[:1])

            if price is not None:
                if price_cent is not None:
                    price = utils.string_to_float((price.strip() + "," + price_cent[1:].strip()).replace(" ", "").replace(" ", ""))
                else:
                    price = utils.string_to_float(price.strip().replace(" ", "").replace(" ", ""))
        #
        #     price_info = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/following::span[' + utils.xpath_class('tax') + '][1]/text()').extract_first()
        #     if price_info is not None:
        #         price_info = price_info.strip()
        #
            src = response.xpath('//div[' + utils.xpath_class('verticalGallery') + ']//li[1]/a/@data-zoom-image').extract_first()
            if src is None:
                src = response.xpath('//div[' + utils.xpath_class('verticalGallery') + ']//li[1]/a/@data-image').extract_first()
            if src is not None:
                src = src.strip()

            rate_path = response.xpath('//div[' + utils.xpath_class('productDetails') + ']/div[' + utils.xpath_class('productRating') + ']')
            rate = rate_path.xpath('//span[' + utils.xpath_class('icon-rating-stars') + ']/@content').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            nb_avis = rate_path.xpath('//span[@itemprop="reviewCount"]/text()').extract_first()
            if nb_avis is not None:
                nb_avis = int(re.sub('\D', ' ', nb_avis.strip()))

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
