from repositories.base_repository import BaseRepository
from repositories.repository_exception import RepositoryException


class ShopRepository(BaseRepository):
    def add(self, shop):
        query = 'INSERT INTO shops (name) VALUES (%s)'
        try:
            self.execute(query, (shop.name,))
        except Exception:
            raise RepositoryException('Error creating shop')

    def add_batch(self, shop_names):
        query = 'INSERT INTO shops (name) VALUES (%s)'
        try:
            self.execute_many(query, [(s,) for s in shop_names])
        except Exception:
            raise RepositoryException('Error creating shops')

    def get(self, shop_id):
        query = 'SELECT * FROM shops WHERE id = %s'
        cursor = self.execute(query, (shop_id,))
        return cursor.fetchone()

    def get_all(self):
        query = 'SELECT * FROM shops'
        cursor = self.execute(query)
        return cursor.fetchall()

    def delete(self, shop_id):
        query = 'DELETE FROM shops WHERE id = %s'
        try:
            self.execute(query, (shop_id,))
        except Exception:
            raise RepositoryException('Error deleting shop')

    def delete_all(self):
        query = 'DELETE FROM shops WHERE 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error deleting shops')

    def reset_autoincrement(self):
        query = 'ALTER TABLE shops AUTO_INCREMENT = 1'
        try:
            self.execute(query)
        except Exception:
            raise RepositoryException('Error resetting shops auto-increment')

    def count(self):
        query = 'SELECT COUNT(*) FROM shops'
        cursor = self.execute(query)
        return cursor.fetchone()[0]

    def get_id_by_name(self, name):
        query = 'SELECT id FROM shops WHERE name = %s LIMIT 1'
        cursor = self.execute(query, (name,))
        return cursor.fetchone()[0]
