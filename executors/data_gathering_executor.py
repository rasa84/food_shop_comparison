import logging

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from models.category import Category
from models.shop_name import ShopName
from page_cleaners.barbora_page_cleaner import BarboraPageCleaner
from page_cleaners.iki_page_cleaner import IkiPageCleaner
from page_cleaners.rimi_page_cleaner import RimiPageCleaner
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from repositories.shop_repository import ShopRepository
from scrapers.categories.barbora_category_scraper import BarboraCategoryScraper
from scrapers.categories.iki_category_scraper import IkiCategoryScraper
from scrapers.categories.rimi_category_scraper import RimiCategoryScraper
from scrapers.products.barbora_product_scraper import BarboraProductScraper
from scrapers.products.iki_product_scraper import IkiProductScraper
from scrapers.products.rimi_product_scraper import RimiProductScraper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


class DataGatheringExecutor:
    @classmethod
    def execute(cls):
        try:
            logger.info('Starting data gathering.')

            cls.__delete_all_data()
            shops_mapping = cls.__save_shops()
            driver, wait = cls.__init_driver()
            cls.__clean_pages(driver)
            categories_by_shop_name = cls.__scrape_and_save_categories(shops_mapping, driver)
            cls.__scrape_and_save_products(driver, categories_by_shop_name)

            logger.info('Scraping completed successfully.')
        except Exception as e:
            logger.error(f'Execution failed: {e}')
            raise

    @classmethod
    def __delete_all_data(cls):
        repositories = [ProductRepository, CategoryRepository, ShopRepository]
        for repo_class in repositories:
            with repo_class() as repo:
                repo.delete_all()
                repo.reset_autoincrement()
                repo.complete()

    @classmethod
    def __save_shops(cls):
        with ShopRepository() as shop_repo:
            shop_repo.add_batch([shop.value for shop in ShopName])
            shop_repo.complete()
        with ShopRepository() as shop_repo:
            shops = shop_repo.get_all()
        shop_mapping = {shop[1]: shop[0] for shop in shops}  # e.g., {{'Barbora': 1}, {'Rimi': 2}, ... }
        logger.info(f'Shop mapping: {shop_mapping}')
        return shop_mapping

    @classmethod
    def __init_driver(cls):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(5)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    @classmethod
    def __clean_pages(cls, driver):
        page_cleaners = [BarboraPageCleaner(driver), RimiPageCleaner(driver), IkiPageCleaner(driver)]
        for p_cleaner in page_cleaners:
            p_cleaner.clean()

    @classmethod
    def __scrape_and_save_categories(cls, shop_mapping, driver):
        categories = cls.__scrape_categories(driver)
        return cls.__save_categories(categories, shop_mapping)

    # example of return
    # {'Barbora': {'Grikiai':
    #                  {'link': 'https://barbora.lt/bakaleja/kruopos/grikiai',
    #                   'categories': ['Bakalėja', 'Kruopos', 'Grikiai']},
    #              'Pasterizuotas pienas':
    #                  {'link': 'https://barbora.lt/pieno-gaminiai-ir-kiausiniai/pienas/pasterizuotas-pienas',
    #                   'categories': ['Pieno gaminiai ir kiaušiniai', 'Pienas', 'Pasterizuotas pienas']}},
    #  'Rimi': {...}
    #
    #  }
    @classmethod
    def __scrape_categories(cls, driver):
        shop_category_data = {}
        scrapers = [BarboraCategoryScraper(driver), RimiCategoryScraper(driver), IkiCategoryScraper(driver)]
        for scraper in scrapers:
            shop_cats = scraper.scrape()
            shop_category_data.update(shop_cats)
        return shop_category_data

    @classmethod
    def __save_categories(cls, shop_category_data, shop_mapping):
        category_mappings_by_shop = {}
        for shop_name, shop_category_data in shop_category_data.items():
            shop_id = shop_mapping[shop_name]
            cat_id_to_link_list = cls.__save_category_hierarchies(shop_category_data.values(), shop_id)
            category_mappings_by_shop.update({shop_name: cat_id_to_link_list})
        logger.info(f'Categories mapping: {category_mappings_by_shop}')
        return category_mappings_by_shop

    @classmethod
    def __save_category_hierarchies(cls, link_to_categories_list, shop_id):
        cat_id_to_link_list = []
        with CategoryRepository() as repo:
            for link_to_categories in link_to_categories_list:
                cat_id_to_link_list.append(cls.__save_category_hierarchy(link_to_categories, repo, shop_id))
            repo.complete()
        return cat_id_to_link_list

    @classmethod
    def __save_category_hierarchy(cls, link_to_categories, repo, shop_id):
        cat_names = link_to_categories['categories']
        cat_parent_node = Category(cat_names[0], shop_id)
        cat_id = repo.add(cat_parent_node)
        for i in range(1, len(cat_names)):
            parent_id = cat_id
            cat_node = Category(cat_names[i], shop_id, parent_id)
            cat_id = repo.add(cat_node)
        return {'category_id': cat_id, 'link': link_to_categories['link']}

    @classmethod
    def __scrape_and_save_products(cls, driver, category_mappings_by_shop):
        scrapers = [BarboraProductScraper(driver), RimiProductScraper(driver), IkiProductScraper(driver)]
        for scraper in scrapers:
            cls.__process_by_shop(category_mappings_by_shop, scraper)

    @classmethod
    def __process_by_shop(cls, category_mappings_by_shop, scraper):
        category_mappings = category_mappings_by_shop[scraper.get_shop_name()]
        for cat_mapping in category_mappings:
            cls.__process_by_category(cat_mapping, scraper)

    @classmethod
    def __process_by_category(cls, category_mapping, scraper):
        cat_products = scraper.scrape(category_mapping['link'], category_mapping['category_id'])
        cls.__save_category_products(cat_products)

    @classmethod
    def __save_category_products(cls, products):
        with ProductRepository() as product_repo:
            product_repo.add_batch(products)
            product_repo.complete()
