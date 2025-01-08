from typing import List
from seleniumwire.webdriver import Firefox


class WebDriver(Firefox):
    def __init__(self, *args, proxies=None, **kwargs):
        if proxies is None:
            proxies = []
        self.proxies = set(proxies) if proxies else set()
        self.proxy_cycle = set()
        self.current_proxy = None

        options: dict = {}

        if "seleniumwire_options" in kwargs.keys() and isinstance(kwargs["seleniumwire_options"], dict):
            options = kwargs.pop("seleniumwire_options")
            if "proxy" not in options.keys():
                if proxies and len(proxies):
                    proxy_dict = {
                        "http": proxies[0],
                        "https": proxies[0]
                    }
                    self.current_proxy = proxies[0]
                    options["proxy"] = proxy_dict
        else:
            if len(proxies):
                options["proxy"] = {
                    "http": proxies[0],
                    "https": proxies[0]
                }
                self.current_proxy = proxies[0]

        super().__init__(*args, **kwargs, seleniumwire_options=options)

    def cycle_proxies(self):
        if len(self.proxies) == 0:
            raise AttributeError("No proxies supplied. Cannot cycle.")
        if len(self.proxies) == 1:
            self.current_proxy = self.proxies.pop()
            self.proxies.add(self.current_proxy)

        if self.proxy_cycle == self.proxies:
            self.proxy_cycle = set()
            self.current_proxy = None
            for proxy in self.proxies:
                if proxy != self.current_proxy:
                    self.current_proxy = proxy
        else:
            for proxy in self.proxies:
                if proxy not in self.proxy_cycle:
                    self.current_proxy = proxy

        self._update_driver_proxy(self.current_proxy)

    def add_proxy(self, proxy: str):
        self.proxies.add(proxy)

    def _update_driver_proxy(self, proxy: str):
        self.proxy = {
            "http": proxy,
            "https": proxy,
        }
        self.proxy_cycle.add(proxy)
