from selenium.webdriver.common.by import By

from page_cleaners.page_cleaner import PageCleaner


class BarboraPageCleaner(PageCleaner):
    def __init__(self, driver):
        super().__init__(driver, 'https://barbora.lt')

    def _accept_cookies(self):
        self.driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll').click()

    def _age_consent(self):
        is_age_20 = len(self.driver.find_elements(By.ID, 'fti-modal-option-1')) != 0
        if is_age_20:
            self.driver.find_element(By.ID, 'fti-modal-option-1').click()
