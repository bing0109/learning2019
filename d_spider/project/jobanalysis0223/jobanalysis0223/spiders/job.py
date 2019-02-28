# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import random
import time
import re
from jobanalysis0223.items import Job51jobItem
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='/home/zelin/data/joblist/job_analysis.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['www.51job.com']
    start_urls = ['http://www.51job.com/']

    def start_requests(self):
        '''
        https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
        https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,2.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
        '''
        keyword = 'python'
        url_first = 'https://search.51job.com/list/040000%252C020000%252C010000%252C180200%252C030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        url_l = [url_first]
        for url in url_l:
            yield scrapy.Request(url=url,callback=self.page_list, dont_filter=True, meta={'kw': keyword})

    def page_list(self, response):
        res = response.css('#resultList > div.dw_tlc > div:nth-of-type(5)').extract()
        res = BeautifulSoup(res[0], 'html.parser')
        total_page = int(res.get_text().split('/')[1].strip())

        keyword = response.meta['kw']
        for i in range(1, 3):
            url = 'https://search.51job.com/list/040000%252C020000%252C010000%252C180200%252C030200,000000,0000,00,9,99,python,2,'+str(i)+'.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
            # yield url
            time.sleep(random.random()*5+1)
            yield scrapy.Request(url=url, callback=self.parse_joblist, meta={'page': i, 'kw': keyword}, dont_filter=True)

    def parse_joblist(self, response):
        data_list = response.css('#resultList > div.el').extract()
        print(len(data_list[1:]), '+++++++++++++++++-')
        for div in data_list[1:]:
            div = BeautifulSoup(div, 'html.parser')
            page_url = div.select('p > span > a')[0].attrs['href']
            time.sleep(abs(random.normalvariate(0,4))+1)
            # print(page_url,'-----------------------------')
            yield scrapy.Request(url=page_url, callback=self.parse_job,meta={'kw':response.meta['kw']})

    def parse_job(self, response):
        res_temp = response.css('body > div.tCompanyPage > div.tCompany_center.clearfix').extract()
        # print(res_temp, '=====================')
        res = BeautifulSoup(res_temp[0], 'lxml')
        kw = response.meta['kw']
        url = response.url
        job_name = res.select('div.tHeader.tHjob > div > div.cn > h1')[0].get_text().strip()
        company = res.select('div.tHeader.tHjob > div > div.cn > p.cname > a.catn')[0].get_text().strip()
        salary = res.select('div.tHeader.tHjob > div > div.cn > strong')[0].get_text().strip()

        job_tag = res.select('div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0].get_text().split('|')
        district = job_tag[0].strip()

        def check_tag(kw):
            for tag in job_tag:
                tag = tag.strip()
                if kw in tag:
                    result = tag
                    break
                else:
                    result = ''
            return result

        experience = check_tag('经验')
        require_num = check_tag('招')
        release_day = check_tag('发布')
        edu_li = ['初中', '高中', '中技', '中专', '大专', '本科', '硕士', '博士']
        for edu in edu_li:
            if check_tag(edu) != '':
                education_req = check_tag(edu)
                break
            else:
                education_req = ''

        # experience = res.select('div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0].get_text().split('|')[1].strip()
        # education_req = res.select('div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0].get_text().split('|')[2].strip()
        # require_num = res.select('div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0].get_text().split('|')[4].strip()
        # release_day = res.select('div.tHeader.tHjob > div > div.cn > p.msg.ltype')[0].get_text().split('|')[-1].strip()

        welfare = res.select('div.tHeader.tHjob > div > div.cn > div > div.t1')[0].get_text()
        job_detail = res.select('div.tCompany_main > div.tBorderTop_box')[0].get_text().strip()

        job_require = ''
        job_type = ''
        job_kw = ''

        def proc_job_detail(kw_list,string,keyword):
            kw_in_str=[]
            for kw in kw_list:
                if kw in string:
                    kw_in_str.append(kw)

            detail_list = re.split('|'.join(kw_in_str),string)
            if keyword in kw_in_str:
                job_keyword = detail_list[kw_in_str.index(keyword) + 1].strip()
            else:
                job_keyword = ''
            return job_keyword

        kw_list = ['职位信息', '任职要求', '职能类别：', '关键字：', '微信分享']

        job_require = proc_job_detail(kw_list,job_detail,'任职要求')
        job_type = proc_job_detail(kw_list,job_detail,'职能类别：')
        job_kw = proc_job_detail(kw_list,job_detail,'关键字：')

        company_type = res.select('div.tCompany_sidebar > div:nth-of-type(1) > div.com_tag > p:nth-of-type(1)')[0].get_text().strip()
        company_size = res.select('div.tCompany_sidebar > div:nth-of-type(1) > div.com_tag > p:nth-of-type(2)')[0].get_text().strip()
        company_industry = res.select('div.tCompany_sidebar > div:nth-of-type(1) > div.com_tag > p:nth-of-type(3) > a')[0].get_text().strip()
        company_addr = res.select('div.tCompany_main > div:nth-of-type(2) > div > p')[0].get_text().strip()


        '''
        body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype
        '''
        data_list = {'kw': kw,
                     'url': url,
                     'job_name': job_name,
                     'salary': salary,
                     'company': company,
                     'district': district,
                     'experience': experience,
                     'education_req': education_req,
                     'require_num': require_num,
                     'release_day': release_day,
                     'welfare': welfare,
                     'job_detail': job_detail,
                     'job_require': job_require,
                     'job_type': job_type,
                     'job_kw': job_kw,
                     'company_type': company_type,
                     'company_size': company_size,
                     'company_industry': company_industry,
                     'company_addr': company_addr
                     }
        # print(data_list,'++++++++++++++++++++=')

        item = Job51jobItem()
        item['kw'] = data_list['kw']
        item['url'] = data_list['url']
        item['job_name'] = data_list['job_name']
        item['salary'] = data_list['salary']
        item['company'] = data_list['company']
        item['district'] = data_list['district']
        item['experience'] = data_list['experience']
        item['education_req'] = data_list['education_req']
        item['require_num'] = data_list['require_num']
        item['release_day'] = data_list['release_day']
        item['welfare'] = data_list['welfare']
        item['job_detail'] = data_list['job_detail']
        item['job_require'] = data_list['job_require']
        item['job_type'] = data_list['job_type']
        item['job_kw'] = data_list['job_kw']
        item['company_type'] = data_list['company_type']
        item['company_size'] = data_list['company_size']
        item['company_industry'] = data_list['company_industry']
        item['company_addr'] = data_list['company_addr']

        return item


'''
scrapy crawl job -s JOBDIR='/home/zelin/data/joblist/'
'''