import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class AuchanSpider(scrapy.Spider):
    name = "auchan"
    allowed_domains = ["auchan.fr"]
    base_url = "https://www.auchan.fr"
    start_urls = [
        base_url + '/informatique/ordinateur-portable/c-7638110'
    ]
    src_no_image = "src-no-image"
    nb_page = None

    def parse(self, response):

        url_next_page = response.xpath('//nav[' + utils.xpath_class('ui-pagination') + ']//a[' + utils.xpath_class('ui-pagination--next') + ']/@href').extract_first()
        if url_next_page is not None:
            url_next_page = self.base_url + url_next_page.strip()
            yield Request(url_next_page, callback=self.parse)

        if not response.xpath('//h1[' + utils.xpath_class('product-detail--title') + ']/text()').extract():
            urls = response.xpath('//div[' + utils.xpath_class('product-list--container') + ']//div[' + utils.xpath_class('product-item--wrapper') + ']/a/@href').extract()
            for url in urls:
                url = self.base_url + url.strip()
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//div[' + utils.xpath_class('ui-breadcrumb--scroller') + ']/nav/span[2]/meta[@itemprop="name"]/@content').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//div[' + utils.xpath_class('ui-breadcrumb--scroller') + ']/nav/span[position() >= 3 and position() < last()]/meta[@itemprop="name"]/@content').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            brand = response.xpath('//div[' + utils.xpath_class('product-detail--wrapper') + ']/meta[@itemprop="brand"]/@content').extract_first()
            if brand is not None:
                brand = brand.strip()

            name = response.xpath('//div[' + utils.xpath_class('product-detail--wrapper') + ']/h1[' + utils.xpath_class('product-detail--title') + ']/text()').extract_first().replace('\n', '').replace('\r', '').strip()

            price_old = response.xpath('//div[' + utils.xpath_class('pricesBlock') + ']//del[' + utils.xpath_class('product-price--oldPrice') + ']/text()').extract_first()
            if price_old is not None:
                price_old = utils.string_to_float(re.sub(' [^ ]*$', '', price_old.strip()).replace(" ", "").replace(" ", ""))

            price = response.xpath('//div[' + utils.xpath_class('pricesBlock') + ']//meta[@itemprop="price"]/@content').extract_first()
            if price is not None:
                price = utils.string_to_float(price.strip())

            currency = response.xpath('//div[' + utils.xpath_class('pricesBlock') + ']//meta[@itemprop="priceCurrency"]/@content').extract_first()
            if currency is not None:
                currency = currency.strip()
        # #
        # #     price_info = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/following::span[' + utils.xpath_class('tax') + '][1]/text()').extract_first()
        # #     if price_info is not None:
        # #         price_info = price_info.strip()
        # #
            src = response.xpath('//div[' + utils.xpath_class('x-scroller') + ']/label[1]//img/@src').extract_first()
            if src is not None:
                src = src.strip()

            rate_path = response.xpath('//div[' + utils.xpath_class('product-detail--rating') + ']')
            rate = rate_path.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            nb_avis = rate_path.xpath('//meta[@itemprop="reviewCount"]/@content').extract_first()
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
