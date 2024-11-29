from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By

from models.product import Product


class ProductScraper(ABC):
    def __init__(self, driver):
        self.driver = driver

    def scrape(self, category_link, category_id):
        products = []
        for url in self._get_urls(category_link, category_id):
            self.driver.get(url)
            product = self.__fill(category_id)
            products.append(product)
        return products

    def _get_urls(self, category_link, category_id):
        page_num = 1
        hrefs = []
        while True:
            self.driver.get(f'{category_link}?{self._get_page_query_param()}={page_num}')
            ul = self.driver.find_element(By.XPATH, self._get_breadcrumb_xpath())
            lis = ul.find_elements(By.TAG_NAME, 'li')
            if len(lis) == 0:
                break
            print(f'Elementų skaičius: {len(lis)}')
            for li in lis:
                href = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
                hrefs.append(href)
            page_num += 1
        return hrefs

    def __fill(self, category_id):
        item_page = self._create_item_page()
        self.driver.implicitly_wait(0)
        product = Product(item_page.get_name(),
                          item_page.get_manufacturer(),
                          item_page.get_brand(),
                          item_page.get_price(),
                          item_page.get_size(),
                          item_page.get_unit(),
                          item_page.get_main_property(),
                          category_id)
        self.driver.implicitly_wait(5)
        return product

    @abstractmethod
    def _create_item_page(self):
        pass

    @abstractmethod
    def get_shop_name(self):
        pass

    @abstractmethod
    def _get_breadcrumb_xpath(self):
        pass

    @abstractmethod
    def _get_page_query_param(self):
        pass
