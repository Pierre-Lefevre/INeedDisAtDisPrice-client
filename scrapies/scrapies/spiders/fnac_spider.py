import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class FnacSpider(scrapy.Spider):
    name = "fnac"
    allowed_domains = ["fnac.com"]
    base_url = "https://www.fnac.com"
    start_urls = [
        base_url + '/Tous-les-ordinateurs-portables/Ordinateurs-portables/nsh154425/w-4?PageIndex=1',
        base_url + '/Tous-les-PC-de-bureau/Ordinateur-de-bureau/nsh51426/w-4?PageIndex=1',
        base_url + '/Toutes-les-tablettes/Toutes-les-tablettes/nsh227099/w-4?PageIndex=1',
        base_url + '/Tous-les-disques-durs/Disque-Dur/nsh119663/w-4?PageIndex=1',
        base_url + '/SearchResult/ResultList.aspx?SCat=8!1%2c8136!2&Search=ramPageIndex=1',
    ]
    srcNoImage = "https://www4-fr.fnac-static.com/Nav/Images/Noscan/noscan_340x340.gif"

    def parse(self, response):
        url_next_page = response.xpath('//ul[' + utils.xpath_class('bottom-toolbar') + ']//a[' + utils.xpath_class('prevnext actionNext') + ']/@href').extract_first()
        if url_next_page:
            yield Request(url_next_page, callback=self.parse)

        if not response.xpath('//h1[' + utils.xpath_class('f-productHeader-Title') + ']/text()').extract():
            urls = response.xpath('//p[' + utils.xpath_class('Article-desc') + ']/a/@href').extract()
            for url in urls:
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        else:
            item = Product()

            main_category = response.xpath('//ul[' + utils.xpath_class('f-breadcrumb') + ']/li[2]/a/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = response.xpath('//ul[' + utils.xpath_class('f-breadcrumb') + ']/li[position() >= 3]/a/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()

            name = response.xpath('//h1[' + utils.xpath_class('f-productHeader-Title') + ']/text()').extract_first().strip()
            price_old = response.xpath('(//span[' + utils.xpath_class('f-priceBox-price f-priceBox-price--old') + '])[1]/text()').extract_first()
            price_cent_old = response.xpath('(//span[' + utils.xpath_class('f-priceBox-price f-priceBox-price--old') + '])[1]/sup/text()').extract_first()
            if price_old is not None:
                if price_cent_old is not None:
                    price_old = utils.string_to_float((price_old + "," + price_cent_old[1:].strip()).replace(" ", ""))
                else:
                    price_old = utils.string_to_float(price_old[:-1].strip().replace(" ", ""))

            price = response.xpath('(//span[' + utils.xpath_class('f-priceBox-price f-priceBox-price--reco') + '])[1]/text()').extract_first()
            price_cent = response.xpath('(//span[' + utils.xpath_class('f-priceBox-price f-priceBox-price--reco') + '])[1]/sup/text()').extract_first()

            currency = None
            if price_cent is not None:
                currency = utils.get_currency_code(price_cent[:1])
            elif price is not None:
                currency = utils.get_currency_code(price[-1:])

            if price is not None:
                if price_cent is not None:
                    price = utils.string_to_float((price + "," + price_cent[1:].strip()).replace(" ", ""))
                else:
                    price = utils.string_to_float(price[:-1].strip().replace(" ", ""))

            src = response.xpath('//img[' + utils.xpath_class('f-productVisuals-mainMedia') + ']/@src').extract_first().strip()
            rate = response.xpath('//div[' + utils.xpath_class('f-review-header') + ']//div[' + utils.xpath_class('f-review-headerRate') + ']/text()').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())
            max_rate = response.xpath('//div[' + utils.xpath_class('f-review-header') + ']//span[' + utils.xpath_class('f-review-headerRateTotal') + ']/text()').extract_first()
            if max_rate is not None:
                max_rate = utils.string_to_float(max_rate.strip().replace("/", ""))
            nb_avis = response.xpath('//div[' + utils.xpath_class('f-productHeader-review') + ']//span[' + utils.xpath_class('f-productHeader-reviewLabel') + ']/text()').extract_first()
            if nb_avis is not None:
                nb_avis = utils.string_to_float(re.sub("\D", "", nb_avis.strip()))

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
            item["rate"] = rate
            item["max_rate"] = max_rate
            item["nb_avis"] = nb_avis

            if src == self.srcNoImage:
                copyfile("data/default.jpg", "data/" + self.name + "/img/" + item["image_name"] + ".jpg")

            yield item
