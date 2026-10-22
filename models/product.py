
import sqlite3
from database.db_connection import get_connection


class Product:
    def __init__(self, name, category, price, stock, product_id=None):
        self.product_id = product_id
        self.name = name.strip()
        self.category = category.strip()
        self.price = float(price)
        self.stock = int(stock)

        if not self.name or not self.category:
            raise ValueError("Name and category are required.")

        if self.price < 0:
            raise ValueError("Price cannot be negative.")

        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")

    def add_product(self):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO Product (name, category, price, stock)
                VALUES (?, ?, ?, ?)
                """,
                (self.name, self.category, self.price, self.stock)
            )
            connection.commit()
            self.product_id = cursor.lastrowid
            return self.product_id
        finally:
            connection.close()

    @staticmethod
    def display_all():
        connection = get_connection()
        try:
            return connection.execute(
                "SELECT * FROM Product ORDER BY product_id"
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def search_by_name(name):
        connection = get_connection()
        try:
            return connection.execute(
                "SELECT * FROM Product WHERE name LIKE ?",
                (f"%{name}%",)
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def filter_by_category(category):
        connection = get_connection()
        try:
            return connection.execute(
                "SELECT * FROM Product WHERE category = ? COLLATE NOCASE",
                (category,)
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def sort_by_price():
        connection = get_connection()
        try:
            return connection.execute(
                "SELECT * FROM Product ORDER BY price ASC"
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def low_stock(threshold):
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")

        connection = get_connection()
        try:
            return connection.execute(
                """
                SELECT * FROM Product
                WHERE stock <= ?
                ORDER BY stock ASC
                """,
                (threshold,)
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def update_product(product_id, name, category, price, stock):
        name = name.strip()
        category = category.strip()
        price = float(price)
        stock = int(stock)

        if not name or not category:
            raise ValueError("Name and category are required.")

        if price < 0 or stock < 0:
            raise ValueError("Price and stock cannot be negative.")

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            old_product = connection.execute(
                "SELECT stock FROM Product WHERE product_id = ?",
                (product_id,)
            ).fetchone()

            if old_product is None:
                connection.rollback()
                return False

            stock_change = stock - old_product["stock"]

            connection.execute(
                """
                UPDATE Product
                SET name = ?, category = ?, price = ?, stock = ?
                WHERE product_id = ?
                """,
                (name, category, price, stock, product_id)
            )

            if stock_change != 0:
                connection.execute(
                    """
                    INSERT INTO InventoryLog
                    (product_id, change_quantity, reason)
                    VALUES (?, ?, ?)
                    """,
                    (product_id, stock_change, "Manual product update")
                )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def delete_product(product_id):
        connection = get_connection()

        try:
            connection.execute(
                "DELETE FROM Product WHERE product_id = ?",
                (product_id,)
            )
            connection.commit()
            return True

        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    @staticmethod
    def adjust_stock(product_id, change_quantity, reason):
        change_quantity = int(change_quantity)
        reason = reason.strip()

        if change_quantity == 0:
            raise ValueError("Stock change cannot be zero.")

        if not reason:
            raise ValueError("A reason is required.")

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            cursor = connection.execute(
                """
                UPDATE Product
                SET stock = stock + ?
                WHERE product_id = ?
                AND stock + ? >= 0
                """,
                (change_quantity, product_id, change_quantity)
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.execute(
                """
                INSERT INTO InventoryLog
                (product_id, change_quantity, reason)
                VALUES (?, ?, ?)
                """,
                (product_id, change_quantity, reason)
            )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def __str__(self):
        return (
            f"Product ID: {self.product_id}, Name: {self.name}, "
            f"Category: {self.category}, Price: {self.price:.2f}, "
            f"Stock: {self.stock}"
        )
