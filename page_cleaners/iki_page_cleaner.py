from selenium.webdriver.common.by import By

from page_cleaners.page_cleaner import PageCleaner


class IkiPageCleaner(PageCleaner):
    def __init__(self, driver):
        super().__init__(driver, 'https://eparduotuve.iki.lt')

    def clean(self):
        self._open_page()
        self._age_consent()
        self._accept_cookies()

    def _age_consent(self):
        is_age_20 = len(self.driver.find_elements(By.XPATH,
                                                  '//*[@id=\'content-:Ragkmq6:\']/div[3]/span/div/span[3]/span/button')) != 0
        if is_age_20:
            self.driver.find_element(By.XPATH,
                                     '//*[@id=\'content-:Ragkmq6:\']/div[3]/span/div/span[3]/span/button').click()

    def _accept_cookies(self):
        button = self.driver.find_element(By.XPATH,
                                          '//*[@id=\'__next\']/span[7]/div/span/div/div/div[2]/span[1]/span/button')
        button.send_keys('\n')
