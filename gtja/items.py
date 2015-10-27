
from scrapy.item import Item, Field

class GtjaItem(Item):
    url = Field()
    title = Field()
    date = Field()
    abstract = Field()
    
    