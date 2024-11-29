from models.shop_name import ShopName
from page_objects.rimi_item_page import RimiItemPage
from scrapers.products.product_scraper import ProductScraper


class RimiProductScraper(ProductScraper):
    def __init__(self, driver):
        self.driver = driver
        super().__init__(driver)

    def _create_item_page(self):
        return RimiItemPage(self.driver)

    def get_shop_name(self):
        return ShopName.RIMI.value

    def _get_breadcrumb_xpath(self):
        return '//*[@id=\'main\']/section/div[1]/div/div[2]/div[1]/div/div[2]/ul'

    def _get_page_query_param(self):
        return 'currentPage'
