# -*- coding: utf-8 -*-

# Scrapy settings for guoshucj project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'guoshucj'

SPIDER_MODULES = ['guoshucj.spiders']
NEWSPIDER_MODULE = 'guoshucj.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'guoshucj (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'guoshucj.pipelines.GuoshucjPipeline': 300
    # 'guoshucj.pipelines.JsonWithEncodingTencentPipeline': 300
}