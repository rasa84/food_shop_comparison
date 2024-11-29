from repositories.base_repository import BaseRepository
from repositories.repository_exception import RepositoryException


class CategoryRepository(BaseRepository):
    def add(self, category):
        query = 'INSERT INTO categories(name, parent_id, shop_id) VALUES (%s, %s, %s)'
        try:
            cursor = self.execute(query, (category.name, category.parent_id, category.shop_id))
            return cursor.lastrowid
        except Exception:
            raise RepositoryException('Error creating category')

    def add_batch(self, categories):
        query = 'INSERT INTO categories(name, parent_id, shop_id) VALUES (%s, %s, %s)'
        try:
            self.execute_many(query, [(c.name, c.parent_id, c.shop_id) for c in categories])
        except Exception:
            raise RepositoryException('Error creating categories')

    def get(self, category_id):
        query = 'SELECT * FROM categories WHERE id = %s'
        cursor = self.execute(query, (category_id,))
        return cursor.fetchone()

    def get_all(self):
        query = 'SELECT * FROM categories'
        cursor = self.execute(query)
        return cursor.fetchall()

    def delete(self, category_id):
        query = 'DELETE FROM categories WHERE id = %s'
        try:
            self.execute(query, (category_id,))
        except Exception:
            raise RepositoryException('Error deleting category')

    def delete_all(self):
        query = 'DELETE FROM categories WHERE 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error deleting categories')

    def reset_autoincrement(self):
        query = 'ALTER TABLE categories AUTO_INCREMENT = 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error resetting categories auto-increment')

    def count(self):
        query = 'SELECT COUNT(*) FROM categories'
        cursor = self.execute(query)
        return cursor.fetchone()[0]
