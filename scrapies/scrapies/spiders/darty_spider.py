import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class DartySpider(scrapy.Spider):
    name = "darty"
    allowed_domains = ["darty.com"]
    base_url = "https://www.darty.com"
    start_urls = [
        base_url + '/nav/extra/list?p=200&s=topa&cat=26055'
    ]
    src_no_image = "src-no-image"
    nb_page = None

    def parse(self, response):

        url_next_page = response.xpath('//div[@id="main_pagination_top"]/div[' + utils.xpath_class('darty_product_list_pages_list') + ']/a[text()="\xa0Page suivante"][last()]/@href').extract_first()
        if url_next_page is not None:
            url_next_page = self.base_url + url_next_page.strip()
            yield Request(url_next_page, callback=self.parse)

        if not response.xpath('//h1[' + utils.xpath_class('product_head') + ']//div[' + utils.xpath_class('product_name') + ']/span/text()').extract():
            urls = response.xpath('//div[@id="main_products_list"]//div[' + utils.xpath_class('infos_container') + ']/h2/a/@href').extract()
            for url in urls:
                url = self.base_url + url.strip()
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//ul[@id="dartyCom_fil_ariane"]/li[2]/a/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//ul[@id="dartyCom_fil_ariane"]/li[position() >= 3 and position() < last()]/a/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            brand = response.xpath('//a[@id="darty_product_brand"]/text()').extract_first()
            if brand is not None:
                brand = brand.strip()

            name = re.sub(' +', ' ', ''.join(response.xpath('//h1[' + utils.xpath_class('product_head') + ']//div[' + utils.xpath_class('product_name') + ']/span//text()').extract()).replace('\n', '').replace('\r', '').strip())


            price_old = response.xpath('//div[' + utils.xpath_class('product_infos') + ']//span[' + utils.xpath_class('darty_prix_barre_cont') + ']/span[' + utils.xpath_class('darty_prix_barre') + ']/text()').extract_first()
            price_old_cent = response.xpath('//div[' + utils.xpath_class('product_infos') + ']//span[' + utils.xpath_class('darty_prix_barre_cont') + ']/span[' + utils.xpath_class('darty_cents darty_prix_barre') + ']/text()').extract_first()

            if price_old is not None:
                if price_old_cent is not None:
                    price_old = utils.string_to_float((re.sub('\D', ' ', price_old.strip()) + "," + re.sub('\D', ' ', price_old_cent.strip())).replace(" ", ""))
                else:
                    price_old = utils.string_to_float(re.sub('\D', ' ', price_old.strip()).replace(" ", ""))

            price = response.xpath('//div[' + utils.xpath_class('product_infos') + ']//meta[@itemprop="price"]/@content').extract_first()
            if price is not None:
                price = utils.string_to_float(price.strip())

            currency = response.xpath('//div[' + utils.xpath_class('product_infos') + ']//meta[@itemprop="priceCurrency"]/@content').extract_first()
            if currency is not None:
                currency = currency.strip()

        # #
        # #     price_info = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/following::span[' + utils.xpath_class('tax') + '][1]/text()').extract_first()
        # #     if price_info is not None:
        # #         price_info = price_info.strip()
        # #
            src = response.xpath('//div[' + utils.xpath_class('darty_product_picture_main_pic_container') + ']/div[1]//img/@src').extract_first()
            if src is not None:
                src = src.strip()

            rate_path = response.xpath('//div[' + utils.xpath_class('bloc_reviews_resume') + ']')
            rate = rate_path.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            max_rate = rate_path.xpath('//div[' + utils.xpath_class('bloc_reviews_note') + ']/sub/text()').extract_first()
            if max_rate is not None:
                max_rate = int(re.sub('\D', ' ', max_rate.strip()))

            nb_avis = rate_path.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
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
            item["max_rate"] = max_rate
            item["nb_avis"] = nb_avis

            if src == self.src_no_image:
                copyfile("data/default.jpg", "data/" + self.name + "/img/" + item["image_name"] + ".jpg")

            yield item
