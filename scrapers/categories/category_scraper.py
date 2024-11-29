from abc import ABC, abstractmethod


class CategoryScraper(ABC):
    def __init__(self, driver, shop_name, category_urls):
        self.driver = driver
        self.shop_name = shop_name
        self.category_urls = category_urls

    def scrape(self):
        category_groups = {}
        for cat_url in self.category_urls:
            self.driver.get(cat_url)
            category_group = self._scrape_group()
            category_groups.update({category_group[-1]: {'link': cat_url, 'categories': category_group}})
        return {self.shop_name.value: category_groups}

    @abstractmethod
    def _scrape_group(self):
        pass
