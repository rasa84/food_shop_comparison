import re

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from page_objects.item_page import ItemPage


class BarboraItemPage(ItemPage):

    def __init__(self, driver):
        super().__init__(driver, '/html/body/div[2]/div/div[3]/div/div[3]/div/div[2]/div[1]/div/div[2]/h1')
        self._description_list_element = None

    def get_name(self):
        name = self.title_with_additional_info.split(',', 1)[0]
        corrected_name = re.sub(rf'\s*{re.escape(self.get_brand())}\s*', ' ', name, flags=re.IGNORECASE).strip()
        return corrected_name[0].upper() + corrected_name[1:]

    def get_manufacturer(self):
        manufacturer = self.description_item('Tiekėjo kontaktai:')
        if manufacturer == '':
            return 'MAXIMA'
        return manufacturer

    def get_brand(self):
        return self.description_item('Prekės ženklas:')

    def get_price(self):
        try:
            div = self.driver.find_element(By.XPATH, '//*[@id=\'fti-product-price--0\']/div[1]/div[1]')
            if div and div.get_attribute('data-testid') and div.get_attribute('data-testid') == 'promoColouredContainer':
                eur = self.driver.find_element(By.XPATH,
                                               '//*[@id=\'fti-product-price--0\']/div[1]/div[1]/div[1]/span[1]').text
                cents = self.driver.find_element(By.XPATH,
                                                 '//*[@id=\'fti-product-price--0\']/div[1]/div[1]/div[1]/span[3]').text
                return float(eur + '.' + cents)
            eur = self.driver.find_element(By.XPATH, '//*[@id=\'fti-product-price--0\']/div[1]/div[1]/span[1]').text
            cents = self.driver.find_element(By.XPATH, '//*[@id=\'fti-product-price--0\']/div[1]/div[1]/span[3]').text
            return float(eur + '.' + cents)
        except NoSuchElementException or ValueError:
            return 0

    def get_size(self):
        size = self.title_with_additional_info.rsplit(', ', 1)[1].split(' ')[0]
        try:
            return float(size)
        except ValueError:
            return 0

    def get_unit(self):
        return self.title_with_additional_info.rsplit(', ', 1)[1].split(' ')[1]

    def description_item(self, label_text):
        try:
            dts = self.description_list_element.find_elements(By.TAG_NAME, 'dt')
            for dt in dts:
                if dt.text == label_text:
                    return dt.find_element(By.XPATH, './/following-sibling::dd').text
            return ''
        except StaleElementReferenceException:
            return ''

    @property
    def description_list_element(self):
        if self._description_list_element is None:
            description_list_elements = self.driver.find_elements(By.CSS_SELECTOR, '.b-product-info--info1')
            if len(description_list_elements) > 0:
                self._description_list_element = description_list_elements[0]
        return self._description_list_element
