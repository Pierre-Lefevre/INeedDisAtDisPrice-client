import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class MaterielNetSpider(scrapy.Spider):
    name = "materiel_net"
    allowed_domains = ["materiel.net"]
    base_url = "https://www.materiel.net"
    start_urls = [
        base_url + '/pc-portable/?p=1'
    ]
    src_no_image = "src-no-image"

    def parse(self, response):
        url_next_page = response.xpath('//ul[' + utils.xpath_class('pagination pagination-sm') + ']/li[position() = last()]/a/@href').extract_first()
        if url_next_page is None:
            url_next_page = response.xpath('//ul[' + utils.xpath_class('pagination pagination-sm') + ']/li[position() = (last() - 1)]/a/@href').extract_first()
        if url_next_page is not None:
            yield Request(self.base_url + url_next_page, callback=self.parse)

        if not response.xpath('//h1[@id="ProdTitle"]/text()').extract():
            urls = response.xpath('//table[' + utils.xpath_class('ProdList') + ']//td[' + utils.xpath_class('Photo') + ']/span/@data-href').extract()
            for url in urls:
                url = self.base_url + url
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/materiel_net/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/materiel_net/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            name = re.sub(' +', ' ', ''.join(response.xpath('//h1[@id="ProdTitle"]//text()').extract()).replace('\n', '').replace('\r', '').strip())

            price_old = response.xpath('//div[@id="ProdInfoPrice"]/div[' + utils.xpath_class('prixReference') + ']/text()').extract_first()
            if price_old is not None:
                price_old = utils.string_to_float(re.sub(' \D*$', '', price_old.strip()).replace(" ", ""))

            price = response.xpath('//div[@id="ProdInfoPrice"]/span[' + utils.xpath_class('hidden') + ']/text()').extract_first()

            currency = None
            price_info = None
            if price is not None:
                currency = utils.get_currency_code(re.sub('^.*\d | [^ ]*$', '', price.strip()))
                price_info = re.sub('^.* ', '', price.strip())

            if price is not None:
                price = utils.string_to_float(re.sub(' \D*$', '', price.strip()).replace(" ", ""))

            src = response.xpath('//div[' + utils.xpath_class('swiper-wrapper') + ']//a/@data-zoom-image').extract_first().strip()

            rate_path = response.xpath('//div[' + utils.xpath_class('headerAvisClients') + ']//span[' + utils.xpath_class('noteUser') + ']')

            rate = rate_path.xpath('text()').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            max_rate = rate_path.xpath('following-sibling::span[1]/text()').extract_first()
            if max_rate is not None:
                max_rate = utils.string_to_float(max_rate.strip())

            nb_avis = response.xpath('//span[@id="avisCount"]/span/text()').extract_first()
            if nb_avis is not None:
                nb_avis = utils.string_to_float(nb_avis.strip())

            item['store'] = self.name
            item['url'] = response.url
            item['openssl_hash'] = utils.generate_open_ssl_hash(item['url'])
            item['name'] = name
            item['price_old'] = price_old
            item['price'] = price
            item['currency'] = currency
            item['price_info'] = price_info
            item["image_urls"] = [src]
            item["image_name"] = item['openssl_hash']
            item["rate"] = rate
            item["max_rate"] = max_rate
            item["nb_avis"] = nb_avis

            if src == self.src_no_image:
                copyfile("data/default.jpg", "data/materiel_net/img/" + item["image_name"] + ".jpg")

            yield item
