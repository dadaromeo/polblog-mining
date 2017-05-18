# -*- coding: utf-8 -*-
import re
import scrapy


class PolblogSpider(scrapy.Spider):
    name = "polblog"
    start_urls = ['http://journalducameroun.com/en/category/politics/']

    def parse(self, response):
        
        for href in response.xpath("//ul[@class='list-post list-full ']//article/a/@href").extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_post)
        
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)
    
    def parse_post(self, response):
        post = scrapy.Item()
        
        text = " ".join(response.xpath("//article[@class='post-full']//div[@class='post-content']//p/text()").extract())
        info = response.xpath("//article[@class='post-full']//p/text()").extract_first()
        h = re.search("\d+h\d+", info).group(0).replace("h", ":")
        d,m,y = re.search("\d+.\d+.\d+", info).group(0).split(".")
        date = y + "-" + m + "-" + d + " " + h
        
        post["url"] = response.url
        post["title"] = response.xpath("//article[@class='post-full']/h1/text()").extract_first()
        post["text"] = " ".join(map(str.strip, text.split(" ")))
        post["author"] = " ".join(re.findall("\w+", info.split("by")[1]))
        post["published"] = date
        
        yield post
