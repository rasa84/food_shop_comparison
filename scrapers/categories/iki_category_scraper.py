from selenium.webdriver.common.by import By

from models.shop_name import ShopName
from scrapers.categories.category_scraper import CategoryScraper


class IkiCategoryScraper(CategoryScraper):
    IKI_CATEGORY_URLS = {
        'https://eparduotuve.iki.lt/chain/category/IKI/Grikiai',
        'https://eparduotuve.iki.lt/chain/category/IKI/Augalinis-pienas-BAUzlFdi73V44CgWeQ9T'
    }

    def __init__(self, driver):
        super().__init__(driver, ShopName.IKI, IkiCategoryScraper.IKI_CATEGORY_URLS)

    def _scrape_group(self):
        cats = []
        div = self.driver.find_element(By.XPATH, '//*[@id=\'__next\']/span[1]/div/div/span/div/div[2]/div')
        links = div.find_elements(By.TAG_NAME, 'a')
        for i in range(2, len(links)):
            cats.append(links[i].text)
        return cats
