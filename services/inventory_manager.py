
from models.product import Product
from database.db_connection import get_connection


class InventoryManager:

    def adjust_stock(self, product_id, quantity, reason):
        return Product.adjust_stock(
            product_id,
            quantity,
            reason
        )

    def get_low_stock_products(self, threshold=5):
        return Product.low_stock(threshold)

    def get_inventory(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT product_id, name, category, price, stock
                FROM Product
                ORDER BY product_id
                """
            ).fetchall()
        finally:
            connection.close()

    def get_inventory_history(self, product_id):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT change_quantity, reason, order_id, timestamp
                FROM InventoryLog
                WHERE product_id = ?
                ORDER BY log_id DESC
                """,
                (product_id,)
            ).fetchall()
        finally:
            connection.close()
