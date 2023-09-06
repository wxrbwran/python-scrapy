import re
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_scrawler.items import To8toItem

class To8toSpider(RedisSpider):
    name = "to8to_redis"
    # allowed_domains = ["xiaoguotu.to8to.com"]
    # start_urls = ["https://xiaoguotu.to8to.com/tuce_sort1?page=1"]
    # redis-cli lpush myspider '{"url": "https://exaple.com", "meta": {"job-id":"123xsd", "start-date":"dd/mm/yy"}, "url_cookie_key":"fertxsas" }'
    redis_key = "to8to:start_urls"
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("ITEM_PIPELINES", {
            "scrapy_scrawler.to8to_pipelines.To8toMongoPipeline": 300,
            "scrapy_scrawler.to8to_pipelines.To8toImagePipeline": 301,
        }, priority="spider")
        
    def parse(self, response):
      
        pic_list = response.xpath("//div[@class='item']")
        del pic_list[0]
     
        content_id_search = re.compile(r"(\d+)\.html")
        for item in pic_list:
            info = {}
            # 项目名称
            info['content_name'] = item.xpath(".//div/a/text()").extract_first()
            # 项目url
            info['content_url'] = f'https:{item.xpath(".//div/a/@href").extract_first()}'
            info['content_id'] = content_id_search.search(info['content_url']).group(1)
            # break
            yield scrapy.Request(url=info['content_url'], callback=self.handle_pic_parse, meta=info)
        # 如果存在下一页
        if response.xpath('//*[@id="nextpageid"]'):
            now_page = int(response.xpath('/html/body/div[3]/div[6]/div/strong/text()').extract_first())
            # 测试，只爬取1页
            if now_page <= -2:
                next_url = f"https://xiaoguotu.to8to.com/tuce_sort1?page={now_page + 1}"
                
                yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=False)
                
    def handle_pic_parse(self, response):
        #
        img_tab_list_with_xpath = response.xpath("/html/body/div[5]/div/div[2]/div[2]/div/div/ul/li")
        img_list = []
        for i in img_tab_list_with_xpath:
            thumb_img_url = i.xpath("./div/img/@src").extract_first()
            full_img_url = thumb_img_url.split("_284.jpg")[0] + ".jpg!750.webp"
            img_list.append(full_img_url)
            # 测试，只存一张
            break
        to8to_info = To8toItem()
        meta = response.request.meta
        to8to_info['content_name'] = meta['content_name']
        to8to_info['content_id'] = meta['content_id']
        to8to_info['content_url'] = meta['content_url']
        to8to_info['img_list'] = img_list
        yield to8to_info
        # print(to8to_info)
