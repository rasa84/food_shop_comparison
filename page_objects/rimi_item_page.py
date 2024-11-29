import re

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from page_objects.item_page import ItemPage


class RimiItemPage(ItemPage):
    def __init__(self, driver):
        super().__init__(driver, '//*[@id=\'main\']/section/div[1]/div/div[2]/section/div/div/div[2]/h1')
        self._description_list_element = None

    def get_name(self):
        name = self.title_with_additional_info.split(',', 1)[0]
        corrected_name = re.sub(rf'\s*{re.escape(self.get_brand())}\s*', ' ', name, flags=re.IGNORECASE).strip()
        return corrected_name[0].upper() + corrected_name[1:]

    def get_manufacturer(self):
        manufacturer = self.description_item('Gamintojas')
        if manufacturer == '':
            return 'RIMI' if 'rimi' in self.get_brand().lower() else ''
        return manufacturer

    def get_brand(self):
        return self.description_item('Prekės ženklas')

    def get_price(self):
        try:
            eur = self.driver.find_element(By.XPATH,
                                           '//*[@id=\'main\']/section/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div[1]/span').text
            cents = self.driver.find_element(By.XPATH,
                                             '//*[@id=\'main\']/section/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div[1]/div/sup').text
            return float(eur + '.' + cents)
        except NoSuchElementException or ValueError:
            return 0

    def get_size(self):
        size = self.description_item('Grynasis kiekis').split(' ')[0]
        try:
            return float(size)
        except ValueError:
            return 0

    def get_unit(self):
        return self.description_item('Grynasis kiekis').split(' ')[1]

    def description_item(self, label_text):
        lis = self.description_list_element.find_elements(By.TAG_NAME, 'li')
        for li in lis:
            span = li.find_element(By.TAG_NAME, 'span')
            if span.text == label_text:
                return li.find_element(By.TAG_NAME, 'p').text
        return ''

    @property
    def description_list_element(self):
        if self._description_list_element is None:
            description_list_elements = self.driver.find_elements(By.CSS_SELECTOR, '.product__list-wrapper')
            if len(description_list_elements) > 0:
                self._description_list_element = description_list_elements[0]
        return self._description_list_element
