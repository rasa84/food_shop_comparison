from scrapers.products.product_scraper import ProductScraper
from models.shop_name import ShopName
from page_objects.barbora_item_page import BarboraItemPage


class BarboraProductScraper(ProductScraper):
    def __init__(self, driver):
        self.driver = driver
        super().__init__(driver)

    def get_shop_name(self):
        return ShopName.BARBORA.value

    def _create_item_page(self):
        return BarboraItemPage(self.driver)

    def _get_breadcrumb_xpath(self):
        return '//*[@id=\'category-page-results-placeholder\']/div/ul'

    def _get_page_query_param(self):
        return 'page'
