import selenium
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

class webdriver:
    def __init__(self, *args, proxies, **kwargs):
        self.driver = webdriver.Chrome(
            seleniumwire_options= {
                'proxy': proxy_list[0],
    })
        self.proxies = proxies
        self.last_proxy = None

    def get(self, url):
        sel