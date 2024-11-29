import re
from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By


class ItemPage(ABC):
    MAIN_PROPERTIES_BY_KEYWORD = {
        'neskrud': '|neskrudintas',
        'ekolog': '|ekologiškas',
    }

    def __init__(self, driver, additional_info_path):
        self.driver = driver
        self.additional_info_path = additional_info_path
        self._title_with_additional_info = None

    def get_main_property(self):
        info = self.title_with_additional_info.lower().replace(' ', '')
        pattern = r'\d+(?:,\d+)?%'
        props = ''

        match = re.search(pattern, info)
        if match:
            props += '|' + match.group()

        for k, v in ItemPage.MAIN_PROPERTIES_BY_KEYWORD.items():
            if k in info:
                props += v
        return props[1:]

    @property
    def title_with_additional_info(self):
        if self._title_with_additional_info is None:
            elements = self.driver.find_elements(By.XPATH, self.additional_info_path)
            if len(elements) > 0:
                self._title_with_additional_info = elements[0].text
            else:
                self._title_with_additional_info = ''
        return self._title_with_additional_info

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_manufacturer(self):
        pass

    @abstractmethod
    def get_brand(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def get_unit(self):
        pass
