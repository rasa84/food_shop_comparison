class PageCleaner:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def clean(self):
        self._open_page()
        self._accept_cookies()
        self._close_ad_windows()
        self._age_consent()

    def _open_page(self):
        self.driver.get(self.url)

    def _accept_cookies(self):
        pass

    def _close_ad_windows(self):
        pass

    def _age_consent(self):
        pass
