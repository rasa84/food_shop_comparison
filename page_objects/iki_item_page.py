import re

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from page_objects.item_page import ItemPage


class IkiItemPage(ItemPage):
    def __init__(self, driver):
        super().__init__(driver,
                         '//*[@id=\'__next\']/span[1]/div/div/span/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/span[2]/span')

    def get_name(self):
        name = self.title_with_additional_info.split(',', 1)[0]
        corrected_name = re.sub(rf'\s*{re.escape(self.get_brand())}\s*', ' ', name, flags=re.IGNORECASE).strip()
        return corrected_name[0].upper() + corrected_name[1:]

    def get_manufacturer(self):
        try:
            return self.description_item('Tiekėjas')
        except NoSuchElementException:
            return ''

    def get_brand(self):
        match = re.search(r'\b[A-ZĄČĘĖĮŠŲŪŽ]+\b', self.title_with_additional_info)
        return match.group(0) if match else ''

    def get_price(self):
        disc_price_elements = self.driver.find_elements(By.XPATH,
                                                        '//*[@id=\'__next\']/span[1]/div/div/span/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div[2]/span/span')
        if len(disc_price_elements) > 0 and disc_price_elements[0] and disc_price_elements[0].text:
            return float(disc_price_elements[0].text.replace('€', '').strip())
        price_elements = self.driver.find_elements(By.XPATH,
                                                   '//*[@id=\'__next\']/span[1]/div/div/span/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/span/span')
        if len(price_elements) > 0 and price_elements[0] and price_elements[0].text:
            return float(price_elements[0].text.replace('€', '').strip())
        return ''

    def get_size(self):
        size = self.title_with_additional_info.rsplit(', ', 1)[1].split(' ')[0]
        try:
            return float(size)
        except ValueError:
            return 0

    def get_unit(self):
        try:
            return self.title_with_additional_info.rsplit(', ', 1)[1].split(' ')[1]
        except IndexError:
            return ''

    def description_item(self, label_text):
        label_element = self.driver.find_element(By.XPATH, '//span[contains(text(), "' + label_text + '")]')
        label_element_parent = label_element.find_element(By.XPATH, './/parent::span')
        value_element = label_element_parent.find_element(By.XPATH, './/following-sibling::span')
        return value_element.text
