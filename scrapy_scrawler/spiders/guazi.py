import re

import scrapy
import json

from scrapy_scrawler.items import GuaziItem
from urllib.parse import urlparse, parse_qsl,urlunparse, unquote, urlencode

brand_info_list = ['brand_name', "brand_value"]
car_info_list = ['car_id', "car_name", "road_haul", "first_pay", "license_date", "price"]


class GuaziSpider(scrapy.Spider):
    name = "guazi"
    allowed_domains = ["guazi.com"]
    DOWNLOADER_MIDDLEWARES = {
    
    }
    
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("DOWNLOADER_MIDDLEWARES", {
            "scrapy_scrawler.middlewares.MyUserAgentMiddleware": 1,
            "scrapy_scrawler.middlewares.HandleGuaziDetail": 2,
        }, priority="spider")
        
    # 发送品牌请求
    def start_requests(self):
        headers = {
            "Verify-Token": "135dd3b0a66b76222ce0bba6f6b6665f",
            "Client-Time": 1693884200,
            "Client-Timestamp": 1693882826,
        }
        brands_list = json.load(open("assets/guazi_brands.json", 'r', encoding="utf-8"))
        for brand in brands_list:
            # 第一页page=1，最新发布order=7
            url = f"https://mapi.guazi.com/car-source/carList/pcList?versionId=0.0.0.0&sourceFrom=wap&deviceId=94580ac2-4dc1-49a9-a176-b10a427ba160&osv=IOS&minor={brand.get('value')}&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=7&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page=1&pageSize=20&city_filter=308&city=308&guazi_city=308&qpres=712085534817648640&platfromSource=wap"
            yield scrapy.Request(url, callback=self.parse, meta=brand)
            break
        
        # for url in self.start_urls:
        #     yield scrapy.Request(url, dont_filter=True, headers=headers)
    
    def parse(self, response):
        data = response.json()
        # print("parse data", data)
        guazi_items = data.get("data").get("postList")
        print("guazi_items", guazi_items)
        for item in guazi_items:
            # https://www.guazi.com/Detail?clueId=128228724
            url = f"https://www.guazi.com/Detail?clueId={item.get('clue_id')}"
            meta = response.request.meta
            for k in car_info_list:
                meta[k] = item.get(k)
            meta['brand_name'] = meta.get("name")
            meta['brand_value'] = meta.get("value")
            meta['car_id'] = item.get("clue_id")
            meta['car_name'] = item.get("title")

            yield scrapy.Request(url, callback=self.parse_detail, meta=meta)
        now_page = data.get("page")
        total_page = data.get("totalPage")
        if total_page > 1 and now_page == 1:
            for page in range(2, total_page + 1):
                url = f"https://mapi.guazi.com/car-source/carList/pcList?versionId=0.0.0.0&sourceFrom=wap&deviceId=94580ac2-4dc1-49a9-a176-b10a427ba160&osv=IOS&minor={meta.get('value')}&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=7&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page={page}&pageSize=20&city_filter=308&city=308&guazi_city=308&qpres=712085534817648640&platfromSource=wap"
    
    def parse_detail(self, response):
        meta = response.request.meta
        car_info = GuaziItem()
        pattern = re.compile(
            r'window.__NUXT__=(?P<script>.*?)</script>',
            re.S,
        )
        scripts = pattern.finditer(response.text)
        # print(scripts)
        script = ""
        for s in scripts:
            script = s.group("script")
        print("script", script)
        car_info_list.extend(brand_info_list)
        for k in car_info_list:
            car_info[k] = meta.get(k)
            car_info[k] = meta.get(k)
        car_info["displacement"] = response.xpath('//*[@id="pageWrapper"]/div[1]/div[3]/div[4]/div[2]/ul/li[3]/span/text()').extract_first()
        car_info["transmission"] = response.xpath('//*[@id="pageWrapper"]/div[1]/div[3]/div[4]/div[2]/ul/li[4]/span/text()').extract_first()

        yield car_info


"""
https://mapi.guazi.com/car-source/option/list?versionId=0.0.0.0&sourceFrom=wap&deviceId=94580ac2-4dc1-49a9-a176-b10a427ba160&osv=IOS&platfromSource=wap
versionId: 0.0.0.0
sourceFrom: wap
deviceId: 94580ac2-4dc1-49a9-a176-b10a427ba160
osv: IOS
platfromSource: wap


headers:
    User-Agent:
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62
    Verify-Token:
    965582e0a5b55a458d946fdbb5634091
    Client-Time:
    1693882828
    Client-Timestamp:
    1693882826
"""

"""
https://mapi.guazi.com/car-source/carList/pcList?versionId=0.0.0.0&sourceFrom=wap&deviceId=0fa0f3cc-efbd-4c59-a50d-b77a810efaa6&osv=IOS&minor=&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=7&priceRange=0,-1&tag_types=&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page=1&pageSize=20&city_filter=308&city=308&guazi_city=308&qpres=712074142081351680&platfromSource=wap

versionId: 0.0.0.0
sourceFrom: wap
deviceId: 0fa0f3cc-efbd-4c59-a50d-b77a810efaa6
osv: IOS
minor:
sourceType:
ec_buy_car_list_ab:
location_city:
district_id:
tag: -1
license_date:
auto_type:
driving_type:
gearbox:
road_haul:
air_displacement:
emission:
car_color:
guobie:
bright_spot_config:
seat:
fuel_type:
order: 7
priceRange: 0,-1
tag_types:
diff_city:
intention_options:
initialPriceRange:
monthlyPriceRange:
transfer_num:
car_year:
carid_qigangshu:
carid_jinqixingshi:
cheliangjibie:
page: 1
pageSize: 20
city_filter: 308
city: 308
guazi_city: 308
qpres: 712074142081351680
platfromSource: wap

"""