import logging

import scrapy


class ZplusSpider(scrapy.Spider):
    name = 'ZplusSpider'
    allowed_domains = ['www.zeit.de']
    start_urls = [
        'https://www.zeit.de/index',
        'https://www.zeit.de/gesellschaft/index',
        'https://www.zeit.de/wirtschaft/index',
        'https://www.zeit.de/kultur/index',
        'https://www.zeit.de/wissen/index',
        'https://www.zeit.de/digital/index',
        'https://www.zeit.de/campus/index',
        'https://www.zeit.de/zeit-magazin/index'
    ]

    def __init__(self):
        logging.getLogger('scrapy').setLevel(logging.INFO)

    @staticmethod
    def request(url, callback):

        request = scrapy.Request(url=url, callback=callback)
        request.cookies['_sp_enable_dfp_personalized_ads'] = 'true'
        request.cookies['_sp_v1_consent'] = '1!0:-1:-1:-1:-1:-1'
        request.cookies['_sp_v1_data'] = '2:193920:1607156423:0:3:0:3:0:0:_:-1'
        request.cookies['_sp_v1_opt'] = '1:login|true:last_id|11:'
        request.cookies['_sp_v1_lt'] = '1:'
        request.cookies[
            '_sp_v1_ss'] = '1:H4sIAAAAAAAAAItWqo5RKimOUbKKRmbkgRgGtbE6MUqpIGZeaU4OkF0CVlBdi1tCSQduIFRqVNmoMhRlsQCobnp2dAIAAA%3D%3D'
        request.cookies['_sp_v1_uid'] = '1:420:e4a3aa54-378b-4d47-a3fb-5a7de44a701e'
        request.cookies['c1_to_wt'] = '1685225653403745173'
        request.cookies['consentUUID'] = 'e815229f-bb61-4d9d-8872-0a9799f6f468'
        request.cookies['creid'] = '1685225653403745173'
        request.cookies[
            'euconsent-v2'] = 'CO98MywO98MywAGABCDEBDCsAP_AAAAAAAYgGqAR5DpFDWFAAXRZQsFgCIAUUMAEAGQCAACBAiABAAEQIAQAkkACoASABAAAAAAAIBIBAAAEDAAAAAAAAAAEAAAgAAAAAAAIIAAAABEAAAIAAAIIAAAAAAAAAAABAAAAmAAQAgZCACAAAAAAQAAAHBIDoACwAKgAZAA4ACAAEQAKgAaQBEAEUAJgATwAuABvADmAIQAQwApQBhgDVAHsAP0AjgBKQC_AGKAPQAi8BeYDBggAIBKwDIQ0AUAFQAXABDAIvAYwIgCAAqAC4AIYBF4qAKACoAJgAXACOALzGQBQAVABMAC4ARwBeY6BIAAsACoAGQAOAAgABEACoAGkARABFACYAE8ALgAYgA3gBzAEIAIYATAApQBYgDDAGUANEAewA_QCLAEcAJSAXUAvwBigD0AIvAXmAwYBjA4ASABcALoAZACEAEZAMCAeQBKwDISEBAABYAGQARAAqACYAFwAMQAbwBYgDKAI4ASkAvwBigD0ALaIAAQCMkoCQACwAMgAcABEAEQAJgAXAAxACEAEMAKUAZQA1QCOAF1AMUAi8BeZIAIABcAMgBGQErFIDwACwAKgAZAA4ACAAEQAKgAaQBEAEUAJgATwApABcADEAHMAQgAhgBSgCxAGUANEAaoA_QCLAEcAJSAegBF4C8wGMFAAoAFwAyAF1AMUAeQA.YAAAAAAAAAAA'
        request.cookies['wt_fa_s'] = 'start~1|1638693865548#'
        request.cookies['wt_fa'] = 'lv~1607156423987|1622708423987#cv~1|1622708423988#fv~1607156423989|1622708423989#'
        request.cookies['wt_rla'] = '981949533494636%2C11%2C1607156423993'
        request.cookies['zonconsent'] = '2020-12-05T08:41:16.273Z'

        request.headers['User-Agent'] = 'ZPlusScraper'
        return request

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield self.request(url, self.parse_main)

    def parse_main(self, response):
        articles = response.xpath('//article')
        print('article count: ' + str(len(articles)))
        scraped_info = self.extract_infos(articles)
        return scraped_info

    def parse_article(self, response):
        scraped_info = response.meta['article_info']

        # Check if a nav bar node exists
        nav_bar = response.xpath("//ul[@class='article-pager']").get()

        if nav_bar is not None:
            # Use the easier non-paged version of the site
            href = scraped_info['href'] + '/komplettansicht'
            request = self.request(href, self.parse_article)
            request.meta['article_info'] = scraped_info
            return request

        if scraped_info['datazplus'] is None:
            scraped_info['article_html'] = ' '.join(response.xpath('.').get().split())
        else:
            scraped_info['article_html'] = None
        return scraped_info

    def extract_infos(self, articles):
        for article in articles:
            href = article.xpath('./a/@href').get()
            title = article.xpath('./a/@title').get()
            if href is None or title is None:
                continue

            scraped_info = {
                'title': title,
                'datazplus': article.xpath('./@data-zplus').get(),
                'href': href,
            }
            #todo: only load article if datazplus ist null
            request = self.request(href, self.parse_article)
            request.meta['article_info'] = scraped_info
            yield request




