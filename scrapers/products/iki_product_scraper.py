from selenium.common import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

from models.shop_name import ShopName
from page_objects.iki_item_page import IkiItemPage
from scrapers.products.product_scraper import ProductScraper


class IkiProductScraper(ProductScraper):
    def _get_urls(self, category_link, category_id):
        self.driver.get(category_link)
        breadcrumb_xpath = self._get_breadcrumb_xpath()
        while True:
            try:
                outer_div = self.driver.find_element(By.XPATH, breadcrumb_xpath)
                last_div = outer_div.find_elements(By.TAG_NAME, 'div')[-1]
                button = last_div.find_element(By.TAG_NAME, 'button')
                button.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                break
        div = self.driver.find_element(By.XPATH, breadcrumb_xpath)
        links = div.find_elements(By.TAG_NAME, 'a')
        print(f'Elementų skaičius: {len(links)}')
        hrefs = []
        for link in links:
            hrefs.append(link.get_attribute('href'))
        return hrefs

    def _create_item_page(self):
        return IkiItemPage(self.driver)

    def get_shop_name(self):
        return ShopName.IKI.value

    def _get_breadcrumb_xpath(self):
        return '//*[@id=\'__next\']/span[1]/div/div/span/div/div[2]/span[1]/div/div[2]'

    def _get_page_query_param(self):
        return ''
