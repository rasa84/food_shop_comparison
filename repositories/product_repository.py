from repositories.base_repository import BaseRepository
from repositories.repository_exception import RepositoryException


class ProductRepository(BaseRepository):
    def add(self, product):
        query = 'INSERT INTO products(name, manufacturer, brand, price, size, unit, main_property, category_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            self.execute(query, (
                product.name, product.manufacturer, product.brand, product.price, product.size, product.unit,
                product.main_property, product.category_id))
        except Exception as e:
            print(f'Error creating product: {e}')
            raise RepositoryException('Error creating product')

    def add_batch(self, products):
        query = 'INSERT INTO products(name, manufacturer, brand, price, size, unit, main_property, category_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            self.execute_many(query, [
                (p.name, p.manufacturer, p.brand, p.price, p.size, p.unit, p.main_property, p.category_id)
                for p in products])
        except Exception as e:
            print(f'Error creating products: {e}')
            raise RepositoryException('Error creating products')

    def get(self, product_id):
        query = 'SELECT * FROM products WHERE id = %s'
        cursor = self.execute(query, (product_id,))
        return cursor.fetchone()

    def get_all(self):
        query = 'SELECT * FROM products'
        cursor = self.execute(query)
        return cursor.fetchall()

    def delete(self, product_id):
        query = 'DELETE FROM products WHERE id = %s'
        try:
            self.execute(query, (product_id,))
        except Exception:
            raise RepositoryException('Error deleting product')

    def delete_all(self):
        query = 'DELETE FROM products WHERE 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error deleting products')

    def reset_autoincrement(self):
        query = 'ALTER TABLE products AUTO_INCREMENT = 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error resetting products auto-increment')

    def count(self):
        query = 'SELECT COUNT(*) FROM products'
        cursor = self.execute(query)
        return cursor.fetchone()[0]
