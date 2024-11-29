from selenium.webdriver.common.by import By

from page_cleaners.page_cleaner import PageCleaner


class RimiPageCleaner(PageCleaner):
    def __init__(self, driver):
        super().__init__(driver, 'https://rimi.lt')

    def _accept_cookies(self):
        button = self.driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        # self.driver.execute_script('arguments[0].scrollIntoView();', button)
        # self.driver.execute_script('arguments[0].click();', button)
        button.send_keys('\n')
