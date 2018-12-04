# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
	name = 'douban_spider'
	allowed_domains = ['book.douban.com']
	start_urls = ['http://book.douban.com/top250']

	def parse(self, response):
		book_list = response.xpath('//div[@class="article"]/div[@class="indent"]/table')
		for i_item in book_list:
			douban_item = DoubanItem()
			book_name = i_item.xpath('.//div[@class="pl2"]/a/text()').extract_first()
			douban_item["book_name"] = book_name.strip()
			douban_item["introduce"] = i_item.xpath('.//p[@class="pl"]/text()').extract_first()
			douban_item["star"] = i_item.xpath('.//span[@class="rating_nums"]/text()').extract_first()
			evaluate = i_item.xpath('.//span[@class="pl"]/text()').extract_first()
			douban_item["evaluate"] = evaluate.lstrip('(').rstrip(')').strip()
			douban_item["describe"] = i_item.xpath('.//p[@class="quote"]/span/text()').extract_first()
			yield douban_item
		next_link = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
		if next_link:
			next_link = next_link[0]
			yield scrapy.Request(next_link, callback=self.parse)
