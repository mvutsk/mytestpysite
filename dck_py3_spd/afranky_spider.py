import scrapy
import re
#scrapy runspider afranky_spider.py


class AfrankySpider(scrapy.Spider):
    name = 'friends_spider'
    print("Note, please enter correct values, no cover for incorrect ones.")
    surl = input("Enter URL of afranky site (http://127.0.0.1:18080): ")
    # surl = 'http://127.0.0.1:5000'
    # start_urls = [surl + '/all-users/']
    slogin = input("Enter login: ")
    spass = input("Enter pass: ")
    # slogin = 'user2'
    # spass = 'user2pass'

    custom_settings = {
        'SPIDER_MIDDLEWARES': {'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700, },
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': False
    }

    def start_requests(self):
        return [scrapy.FormRequest(self.surl + "/login/",
                                   callback=self.logging_in)]

    def logging_in(self, response):
        CSRF_SELECTOR = 'input[id*=csrf_token]'
        CSRFX_SELECTOR = '@value'
        csrf = response.css(CSRF_SELECTOR).xpath(CSRFX_SELECTOR).extract()
        return [scrapy.FormRequest(self.surl + "/login/",
                                   formdata={'next': '/all-users/', 'csrf_token': csrf[0], 'username': self.slogin, 'password': self.spass},
                                   callback=self.parse)]

    def parse(self, response):
        USER_SELECTOR = '.users'
        for user in response.css(USER_SELECTOR).xpath('li'):
            # NAME_SELECTOR = 'a ::text'
            PROFILE_SELECTOR = 'a ::attr(href)'
            user_profile = user.css(PROFILE_SELECTOR).extract_first()
            if user_profile:
                yield scrapy.Request(
                    response.urljoin(user_profile),
                    callback=self.parse_profile
                )

    def strip_spaces(self, line):
        line = re.sub("^\s+", "", line)
        line = re.sub("\s+\Z", "", line)
        return line

    def parse_profile(self, response):
        PROF_SEL = '.profile'
        NAME_SEL = './/p[text() = "Name: "]/strong/text()'
        USERNAME_SEL = './/head/title/text()'
        EMAIL_SEL = './/p[text() = "E-Mail: "]/strong/text()'
        LASTV_SEL = './/p[text() = "Last visit: "]/strong/text()'
        VISITS_SEL = './/p[text() = "Visits: "]/strong/text()'
        FRS_SEL = '.friends'
        FRD_SEL = './/p/strong/a/text()'
        prof_name = str(response.xpath(USERNAME_SEL).extract_first())
        prof_name = re.sub("^(\s+)(.+)(:)(\s+)", "", prof_name)
        prof_name = re.sub("\s+.*\Z", "", prof_name)

        yield {
            'username': prof_name,
            'name': response.css(PROF_SEL).xpath(NAME_SEL).extract_first(),
            'email': self.strip_spaces(str(response.css(PROF_SEL).xpath(EMAIL_SEL).extract_first())),
            'last visit': self.strip_spaces(str(response.css(PROF_SEL).xpath(LASTV_SEL).extract_first())),
            'visit count': self.strip_spaces(str(response.css(PROF_SEL).xpath(VISITS_SEL).extract_first())),
            'friends': response.css(PROF_SEL).css(FRS_SEL).xpath(FRD_SEL).extract(),
        }
