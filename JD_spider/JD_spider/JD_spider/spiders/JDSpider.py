# -*- coding: utf-8 -*-
import scrapy
from ..items import JdSpiderItem
from scrapy_redis.spiders import RedisSpider
import json
from jsonpath import jsonpath
keyword = '笔记本'
class JdspiderSpider(scrapy.Spider):
    name = 'JDSpider'
    # allowed_domains = ['jd.com']
    redis_key = 'JDSpider:start_urls'
    # start_urls = ['https://search.jd.com/Search?keyword=笔记本&enc=utf-8&wq=笔记本&page=1']

    def start_requests(self):
        starts = [
            'https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&wq=' + keyword + '&page=' + str(page) for
            page in range(1, 201)]
        for url in starts:
            yield self.make_requests_from_url(url)
    def parse(self, response):
        first_node_list = response.xpath("//div[@id='J_goodsList']/ul/li")
        for first_node in first_node_list:
            item = JdSpiderItem()
            item['item_id'] = first_node.xpath('./@data-sku').extract_first()
            item['title'] = first_node.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").extract_first()
            item['url'] = first_node.xpath(".//div[@class='p-name p-name-type-2']/a/@href").extract_first()
            item['price_wap'] = first_node.xpath(".//div[@class='p-price']/strong/i/text()").extract_first()
            item['buy_num'] = first_node.xpath(".//div[@class='p-commit']/strong/a/text()").extract_first()
            item['count'] = 0
            item['rate']=[]
            base_url = "https://sclub.jd.com/comment/productPageComments.action?&productId="
            url_end = "&pageSize=10&sortType=5&score=0"
            for page in range(0, 100):
                url = base_url + item['item_id'] + "&page="+ str(page) +url_end
                yield scrapy.Request(url,callback=self.parse_rate,meta={'item':item},dont_filter=True)

    def parse_rate(self,response):
        item=response.meta['item']
        res = response.body.decode('gbk','ignore')
        html = json.loads(res)
        rate_list = jsonpath(html,'$..comments')[0]
        for rate in rate_list:
            if not rate['content']:
                pass
            else:
                if not '此用户未' in rate['content']:
                    item['rate'].append(rate['content'])
        item['count'] += 1
        # print(item['rate'])
        yield item
