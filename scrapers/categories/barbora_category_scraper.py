from selenium.webdriver.common.by import By

from models.shop_name import ShopName
from scrapers.categories.category_scraper import CategoryScraper


class BarboraCategoryScraper(CategoryScraper):
    BARBORA_CATEGORY_URLS = [
        'https://barbora.lt/bakaleja/kruopos/grikiai',
        'https://barbora.lt/pieno-gaminiai-ir-kiausiniai/pienas/pasterizuotas-pienas'
    ]

    def __init__(self, driver):
        super().__init__(driver, ShopName.BARBORA, BarboraCategoryScraper.BARBORA_CATEGORY_URLS)

    def _scrape_group(self):
        cats = []
        ol = self.driver.find_element(By.CLASS_NAME, 'breadcrumb')
        lis = ol.find_elements(By.TAG_NAME, 'li')
        for i in range(1, len(lis)):
            a = lis[i].find_element(By.TAG_NAME, 'a').text
            cats.append(a)
        return cats
