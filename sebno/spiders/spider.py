import scrapy

from scrapy.loader import ItemLoader
from ..items import SebnoItem
from itemloaders.processors import TakeFirst


class SebnoSpider(scrapy.Spider):
	name = 'sebno'
	start_urls = ['https://seb.no/om-seb/presse-och-nyheter/nyheter/seb-i-norge']

	def parse(self, response):
		post_links = response.xpath('//div[@class="tabs articlelist"]/div/div/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col col-2 span6"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date"]/text()').get()

		item = ItemLoader(item=SebnoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
