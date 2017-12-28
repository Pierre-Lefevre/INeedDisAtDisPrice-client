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

        # url_next_page = response.xpath('//ul[' + utils.xpath_class('pagerItems') + ']//span[' + utils.xpath_class('pagerSelectedItem') + ']/following::a[1]/@href').extract_first()
        # if url_next_page is not None:
        #     url_next_page = url_next_page.strip()
        #     yield Request(url_next_page, callback=self.parse)
        #
        # print(response.xpath('//div[' + utils.xpath_class('pagerWrapper') + ']//a[' + utils.xpath_class('pagerWrapper') + ']/@href').extract_first())
        # print(response.xpath('//ul[' + utils.xpath_class('pagerItems') + ']//span[' + utils.xpath_class('pagerSelectedItem') + ']/following::a[1]/@href').extract_first())
        #
        # if self.nb_page is None:
        #     self.nb_page = response.xpath('//ul[@id="PaginationForm_ul"]/li[last()]/a/text()').extract_first()
        #     if self.nb_page is not None:
        #         self.nb_page = self.nb_page.strip()
        #         for x in range(1, int(self.nb_page)):
        #             yield Request(self.base_url + "/informatique/ordinateurs-pc-portables/pc-portables/l-1070992-" + str(x) + ".html", callback=self.parse)
        #
        # if not response.xpath('//h1/span[' + utils.xpath_class('fn designation_courte') + ']/text()').extract():
        #     urls = response.xpath('//div[' + utils.xpath_class('productListing') + ']//a[' + utils.xpath_class('nom') + ']/@href').extract()
        #     for url in urls:
        #         url = url.strip()
        #         open_ssl_hash = utils.generate_open_ssl_hash(url)
        #         if len(glob.glob("data/" + self.name + "/json/" + open_ssl_hash + '.json')) != 1 or len(glob.glob("data/" + self.name + "/img/" + open_ssl_hash + '.jpg')) != 1:
        #             yield Request(url, callback=self.parse)
        #
        # else:
        #     item = Product()
        #
        #     main_category = response.xpath('//ul[' + utils.xpath_class('cheminDeFer') + ']/li[2]/div/a/span/text()').extract_first()
        #     if main_category is not None:
        #         main_category = main_category.strip()
        #
        #     categories = response.xpath('//ul[' + utils.xpath_class('cheminDeFer') + ']/li[position() >= 3 and position() <= last()]/div/a/span/text()').extract()
        #     if categories:
        #         for i, category in enumerate(categories):
        #             categories[i] = category.strip()
        #
        #     brand = response.xpath('//table[@id="productParametersList"]//div[text()="Marque"]/following::div[1]/a/text()').extract_first()
        #     if brand is not None:
        #         brand = brand.strip()
        #
        #     name = re.sub(' +', ' ', response.xpath('//h1/span[' + utils.xpath_class('fn designation_courte') + ']/text()').extract_first().strip())
        #
        #     price_old = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('refPrice') + ']/text()').extract_first()
        #     if price_old is not None:
        #         price_old = utils.string_to_float(price_old[:-1].strip().replace(" ", "").replace(" ", ""))
        #
        #     price = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/text()').extract_first()
        #     price_cent = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/sup/text()').extract_first()
        #
        #     currency = None
        #     if price is not None:
        #         currency = utils.get_currency_code(price[-1:])
        #
        #     if price is not None:
        #         if price_cent is not None:
        #             price = utils.string_to_float((price[:-1].strip() + "," + price_cent.strip()).replace(" ", "").replace(" ", ""))
        #         else:
        #             price = utils.string_to_float(price[:-1].strip().replace(" ", "").replace(" ", ""))
        #
        #     price_info = response.xpath('//span[' + utils.xpath_class('blocprix') + ']//span[' + utils.xpath_class('price') + ']/following::span[' + utils.xpath_class('tax') + '][1]/text()').extract_first()
        #     if price_info is not None:
        #         price_info = price_info.strip()
        #
        #     src = response.xpath('//img[@id="ctl00_cphMainContent_ImgProduct"]/@src').extract_first().strip()
        #
        #     rate_path = response.xpath('//span[' + utils.xpath_class('noteliens clearfix') + ']')
        #     rate = rate_path.xpath('meta/@content').extract_first()
        #     if rate is not None:
        #         rate = utils.string_to_float(rate.strip())
        #
        #     nb_avis = rate_path.xpath('a[not(@class)]/span/text()').extract_first()
        #     if nb_avis is not None:
        #         nb_avis = int(nb_avis.strip())
        #
        #     item['store'] = self.name
        #     item['url'] = response.url
        #     item['main_category'] = main_category
        #     item['categories'] = categories
        #     item['brand'] = brand
        #     item['openssl_hash'] = utils.generate_open_ssl_hash(item['url'])
        #     item['name'] = name
        #     item['price_old'] = price_old
        #     item['price'] = price
        #     item['currency'] = currency
        #     item['price_info'] = price_info
        #     item["image_urls"] = [src]
        #     item["image_name"] = item['openssl_hash']
        #     item["rate"] = rate
        #     item["max_rate"] = 5
        #     item["nb_avis"] = nb_avis
        #
        #     if src == self.src_no_image:
        #         copyfile("data/default.jpg", "data/" + self.name + "/img/" + item["image_name"] + ".jpg")
        #
        #     yield item
