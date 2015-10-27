
# -*- coding: UTF-8 -*-

import time

from scrapy import log
from scrapy.contrib.spiders  import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

from gtja.items import GtjaItem


class GtjaSpider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = "gtja"
    start_urls = [
        #"http://www.cnblogs.com/hotbaby/",
        #"http://www.cnblogs.com/hxsyl/",
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=1", # latest reports
        "http://www.gtja.com/fyInfo/contentForJunhong.jsp?id=692190", # test url
        "http://www.gtja.com/fyInfo/contentForJunhong.jsp?id=692040",
        "http://www.gtja.com/fyInfo/contentForJunhong.jsp?id=692060",
        
    ]
    rules = [
        #Rule(SgmlLinkExtractor(allow=[r'/default.html']), follow=True),
        #Rule(SgmlLinkExtractor(allow=[r'/p/\w+.html']), callback="parse_report"),
        #Rule(SgmlLinkExtractor(allow=[r''], callback="parse_report")),
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=settings["COOKIE"], callback=self.parse_report)
        
    def parse_report(self, response):
        """ Extract data from html. """
        
        hxs = HtmlXPathSelector(response)
        item = GtjaItem()

        item["url"] = response.url
        item["title"] = hxs.select("//td[@class='f20blue tdc']/text()").extract()[0]
        item["date"] = hxs.select("//div[@class='f_black f_14']/text()").extract()[0]
        item["abstract"] = hxs.select("//table[@class='f_black f_14']//td").extract()[0]
        #TODO regular matching the abstract content
        
        return item
