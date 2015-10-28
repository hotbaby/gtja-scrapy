
# -*- coding: UTF-8 -*-

import time

from scrapy import log
from scrapy.contrib.spiders  import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

from gtja.items import GtjaItem
from _cffi_backend import callback


class GtjaSpider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = "gtja"
    allowed_domains = ["gtja.com"]
    start_urls = [
        #"http://www.gtja.com/fyInfo/contentForJunhong.jsp?id=692190", #Test case
        
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=8", #Strategy research
        "http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=1&keyWord=", 
        
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=7", #Bond research
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=6", #Financial engineering
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=5", #Company research
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=4", #Industry research
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=3", #Macro research
        #"http://www.gtja.com/fyInfo/uplusReportsList.jsp?catType=1", #Latest report

    ]
    rules = [
        Rule(LinkExtractor(allow=[r"/fyInfo/contentForJunhong.jsp"]), callback="parse_report"), # report abstract
        #TODO next page
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            #yield Request(url, cookies=settings["COOKIE"], callback=self.parse_report)
            yield Request(url, cookies=settings["COOKIE"])
        
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
