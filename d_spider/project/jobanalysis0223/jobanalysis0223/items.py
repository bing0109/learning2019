# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51jobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kw = scrapy.Field()
    url = scrapy.Field()
    job_name = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    district = scrapy.Field()
    experience = scrapy.Field()
    education_req = scrapy.Field()
    require_num = scrapy.Field()
    release_day = scrapy.Field()
    welfare = scrapy.Field()
    job_detail = scrapy.Field()
    job_require = scrapy.Field()
    job_type = scrapy.Field()
    job_kw = scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_industry = scrapy.Field()
    company_addr = scrapy.Field()


