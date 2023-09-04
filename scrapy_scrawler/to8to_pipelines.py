# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class To8toScrapyScrawlerPipeline:
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        mydb = myclient['to8to']
        self.mycollection = mydb['c_to8to']
    
    def process_item(self, item, spider):
        # print("To8toScrapyScrawlerPipeline")
        # print(item)
        data = dict(item)
        self.mycollection.insert_one(data)
        return item


class To8toImagePipeline(ImagesPipeline):
    
    # 根据images_urls中指定的url进行爬取
    def get_media_requests(self, item, info):
        print('To8toImagePipeline')
        print(item)
        try:
            if len(item['img_list']) > 0:
                for src in item['img_list']:
                    yield scrapy.Request(src)
            else:
                pass
        except:
            pass
    
    def item_completed(self, results, item, info):
        # (isSuccess, image_info or failure)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("item contains no images")
        return item
    
    def file_path(self, request, response=None, info=None, *, item=None):
        # 用于下载图片设置图片名称
        file_name = request.url.split("/")[-1]
        return file_name
