import re
from scrapy.commands import ScrapyCommand
import urllib
import urllib.request as urllib2
# import urllib2
from scrapy import logformatter as log
from scrapy import spiderloader
from scrapy.utils import project
import logging


from scrapy.commands.crawl import Command
from scrapy.exceptions import UsageError


class AllCrawlCommand(ScrapyCommand):

    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def short_desc(self):
        return "Schedule a run for all available spiders"

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError(
                "running 'scrapy crawl' with more than one spider is no longer supported")

        url = 'http://localhost:6800/schedule.json'
        settings = project.get_project_settings()

        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        spiders = spider_loader.list()
        count = 1
        for s in spiders:

            if s is not '':
                values = {'project': 'default', 'spider': s, 'part': count}
                count += 1
                data = urllib.parse.urlencode(values).encode("utf-8")
                req = urllib2.Request(url, data)

                print(data)
                response = urllib2.urlopen(req)
                # log.msg(response)
                # logging.warning(response)
