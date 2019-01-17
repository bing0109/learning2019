# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from scrapy.http import HtmlResponse, Response
import time
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='/home/zelin/data/jd_nianhuo/jdnianhuo.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)


class MyscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HttpbinDownloaderMiddleware(object):
    def process_request(self, request, spider):
        """
        了解process_request的用法，利用downloader中间件设置代理
        :param request:
        :param spider:
        :return:
        """
        print('start proxy  -----------')
        request.meta['proxy'] = 'http://119.101.116.36:9999'
        return None

    def process_response(self, request, response, spider):
        """
        了解process_response的用法，利用downloader中间件改变 返回后的状态码
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if response.status == 200:
            response.status = 201       # 设置成401后，scrapy后面的不会再处理

        return response

    def process_exception(self, request, exception, response):
        return None


class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.wait = WebDriverWait(self.browser, 30)
        self.logger = logging.getLogger(__name__)

    def __del__(self, instance):
        self.browser.close()
        logging.info('close browser')

    def process_request(self, request, spider):
        # print(request.meta,'---request-meta-------------------')
        if 'type' in request.meta:  #'type' in request.meta.keys()
            # 爬取图片
            print(request.url,'-----img-request-url-----')
            res = requests.get(request.url).content
            logging.info('get img response,pgid:'+str(request.meta['pg']))
            return Response(url=request.url, request=request, status=200, body=res)

        else:
            # 搜索和翻页，并返回结果
            # self.logger.info('----------')
            self.browser.get(request.url)
            time.sleep(1)
            # 获取准备跳转的页面
            pg = request.meta['pg']
            if int(pg) > 1:
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#J_goodsList > ul > li:nth-of-type(60)')))  # 等待每页最后一条记录显示出来，最后一页可能得另外处理一下

                pg_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))    # 获取页面输入框
                pg_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))          # 获取确定跳转按钮
                pg_input.clear()
                pg_input.send_keys(str(int(pg)+1))
                pg_btn.click()

            time.sleep(3)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li:nth-of-type(60)')))  # 等待每页最后一条记录显示出来，最后一页可能得另外处理一下
            # self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(pg)))   # 等待底下翻页栏，当前页面数显示位跳转后的页面
            # self.browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > em:nth-of-type(1) > b'))text  # 总页数
            # pg = self.browser.find_element_by_css_selector('#J_bottomPage > span.p-num > a.curr').text  # 获取当前页数

            res = self.browser.page_source

            # print(res, '-------res-----process-request---------')
            # 直接返回Response会报错编码错误，body必须是byte类型
            # return Response(url=request.url, request=request, status=200, body=res)
            # 把url带上是传给spider时，让其知晓响应是哪个request发出的
            logging.info('get search and go to the specified page, pgid:' + str(int(pg)+1))
            return HtmlResponse(url=request.url, request=request, status=200, encoding='utf-8', body=res)

    def process_exception(self, request, exception, spider):
        # print('出现错误,jdnianhuo')
        logging.error('error occur \n'+ str(exception))
        self.browser.close()


class GoogleDownloaderMiddleware(object):
    def process_exception(self, request, exception, spider):
        print('出现错误,google')
        # return None
        return request