import scrapy

import glob
import re
import scrapies.utils as utils
from scrapy.http import Request
from shutil import copyfile
from scrapies.items import Product


class LdlcSpider(scrapy.Spider):
    name = "ldlc"
    allowed_domains = ["ldlc.com"]
    base_url = "https://www.ldlc.com"
    # Only full list pages.
    start_urls = [
        base_url + '/informatique/ordinateur-portable/pc-portable/c4265/'
    ]

    def parse(self, response):

        # Yield product pages.
        x_list = response.xpath('//div[' + utils.xpath_class('productListing') + ']')
        if x_list:
            urls = x_list.xpath('.//a[' + utils.xpath_class('nom') + ']/@href').extract()
            for url in urls:
                url = url.strip()
                open_ssl_hash = utils.generate_open_ssl_hash(url)
                if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
                    yield Request(url, callback=self.parse)

        # Yield product.
        x_product = response.xpath('//div[' + utils.xpath_class('product') + ']')
        if x_product:
            item = Product()


            # Categories
            x_categories = response.xpath('//ul[' + utils.xpath_class('cheminDeFer') + ']')

            main_category = x_categories.xpath('./li[2]/div/a/span/text()').extract_first()
            if main_category is not None:
                main_category = main_category.strip()

            categories = x_categories.xpath('./li[position() >= 3 and position() <= last()]/div/a/span/text()').extract()
            if categories:
                for i, category in enumerate(categories):
                    categories[i] = category.strip()


            # Brand
            brand = response.xpath('//table[@id="productParametersList"]//div[text()="Marque"]/following::div[1]/a/text()').extract_first()
            if brand is not None:
                brand = brand.strip()


            # Name
            name = re.sub(' +', ' ', response.xpath('//h1/span[' + utils.xpath_class('fn designation_courte') + ']/text()').extract_first().strip())


            # Price
            x_price = response.xpath('//span[' + utils.xpath_class('blocprix') + ']')

            price_old = x_price.xpath('.//span[' + utils.xpath_class('refPrice') + ']/text()').extract_first()
            if price_old is not None:
                price_old = utils.string_to_float(price_old[:-1].strip().replace(" ", "").replace(" ", ""))

            price = x_price.xpath('.//span[' + utils.xpath_class('price') + ']/text()').extract_first()
            price_cent = x_price.xpath('.//span[' + utils.xpath_class('price') + ']/sup/text()').extract_first()

            currency = None
            if price is not None:
                currency = utils.get_currency_code(price[-1:])

            if price is not None:
                if price_cent is not None:
                    price = utils.string_to_float((price[:-1].strip() + "," + price_cent.strip()).replace(" ", "").replace(" ", ""))
                else:
                    price = utils.string_to_float(price[:-1].strip().replace(" ", "").replace(" ", ""))


            # Image
            src = response.xpath('//img[@id="ctl00_cphMainContent_ImgProduct"]/@src').extract_first().strip()


            # Avis
            x_avis = response.xpath('//div[@id="productinfos"]//span[' + utils.xpath_class('rating') + ']')

            rate = x_avis.xpath('./span[' + utils.xpath_class('average') + ']/text()').extract_first()
            if rate is not None:
                rate = utils.string_to_float(rate.strip())

            nb_avis = x_avis.xpath('./span[' + utils.xpath_class('votes') + ']/text()').extract_first()
            if nb_avis is not None:
                nb_avis = int(nb_avis.strip())

            max_rate = x_avis.xpath('./span[' + utils.xpath_class('best') + ']/text()').extract_first()
            if max_rate is not None:
                max_rate = int(max_rate.strip())


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
            item["image_urls"] = [src]
            item["image_name"] = item['openssl_hash']
            item["rate"] = rate
            item["max_rate"] = max_rate
            item["nb_avis"] = nb_avis


            yield item
