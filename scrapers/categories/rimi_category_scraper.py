from selenium.webdriver.common.by import By

from scrapers.categories.category_scraper import CategoryScraper
from models.shop_name import ShopName


class RimiCategoryScraper(CategoryScraper):
    RIMI_CATEGORY_URLS = {
        'https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/kruopos/grikiai/c/SH-2-6-36',
        'https://www.rimi.lt/e-parduotuve/lt/produktai/pieno-produktai-kiausiniai-ir-suris/pienas-ir-augaliniai-pieno-pakaitalai/pasterizuotas-pienas/c/SH-11-8-17'
    }

    def __init__(self, driver):
        super().__init__(driver, ShopName.RIMI, RimiCategoryScraper.RIMI_CATEGORY_URLS)

    def _scrape_group(self):
        cats = []
        div = self.driver.find_element(By.CLASS_NAME, 'section-header__container')
        links = div.find_elements(By.TAG_NAME, 'a')
        for c in links:
            cats.append(c.text)
        return cats
