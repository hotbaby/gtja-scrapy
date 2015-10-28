
from pymongo import Connection

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MongoDBStorage(object):

    def __init__(self, *args, **kwargs):
        connection = Connection(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        db = connection[settings["MONGODB_DB"]]
        self.collectoin = db[settings["MONGODB_COLLECTION"]]
   
    def process_item(self, item, spider):
        
        if not item["title"]:
            raise DropItem("Missing title of object from %s." % item["title"])
        else:
            self.collectoin.insert(item)
        return item