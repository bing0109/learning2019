# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from scrapy.http import HtmlResponse

class SeleniumDownloaderMiddleware(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)#调试logger
        self.browser = webdriver.Chrome()#声明浏览器
        self.wait = WebDriverWait(self.browser,10)#显式等待

    def __del__(self):
        self.browser.close()#关闭浏览器

    def process_request(self, request, spider):
        self.logger.info('用selenium获取响应')
        self.browser.get(request.url)#访问网址
        page = request.meta['page']#获取准备跳转的页面
        #如果page大于1，则进行页面调转
        # if page>1:
        #     time.sleep(1)
        #     self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        #     time.sleep(1)
        #     input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input')))
        #     button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
        #     input.clear()
        #     input.send_keys(page)
        #     button.click()
        time.sleep(1)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList .gl-item')))
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.curr'),str(page)))
        #返回response对象
        return HtmlResponse(url=request.url,request=request,body=self.browser.page_source,status=200,encoding='utf-8')


