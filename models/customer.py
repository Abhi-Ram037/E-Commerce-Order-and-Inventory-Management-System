
import sqlite3
from models.user import User
from database.db_connection import get_connection


class Customer(User):
    def __init__(self, name, email, phone, customer_id=None):
        super().__init__(name, email, phone)
        self.customer_id = customer_id

    def register(self):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO Customer (name, email, phone)
                VALUES (?, ?, ?)
                """,
                (self.name, self.email, self.phone)
            )

            connection.commit()
            self.customer_id = cursor.lastrowid
            return self.customer_id

        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise ValueError(
                "Customer email already exists or details are invalid."
            ) from error

        finally:
            connection.close()

    @staticmethod
    def display_all():
        connection = get_connection()

        try:
            return connection.execute(
                "SELECT * FROM Customer ORDER BY customer_id"
            ).fetchall()
        finally:
            connection.close()

    @staticmethod
    def search(customer_id=None, email=None):
        connection = get_connection()

        try:
            if customer_id is not None:
                return connection.execute(
                    "SELECT * FROM Customer WHERE customer_id = ?",
                    (customer_id,)
                ).fetchone()

            if email is not None:
                return connection.execute(
                    "SELECT * FROM Customer WHERE email = ? COLLATE NOCASE",
                    (email,)
                ).fetchone()

            raise ValueError("Provide a customer ID or email.")

        finally:
            connection.close()

    @staticmethod
    def update(customer_id, name, email, phone):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE Customer
                SET name = ?, email = ?, phone = ?
                WHERE customer_id = ?
                """,
                (name, email, phone, customer_id)
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True

        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise ValueError(
                "Email already exists or details are invalid."
            ) from error

        finally:
            connection.close()

    @staticmethod
    def order_history(customer_id):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT order_id, order_date, total_amount, status
                FROM Orders
                WHERE customer_id = ?
                ORDER BY order_date DESC
                """,
                (customer_id,)
            ).fetchall()

        finally:
            connection.close()

    def __str__(self):
        return (
            f"Customer ID: {self.customer_id}, "
            f"Name: {self.name}, "
            f"Email: {self.email}, "
            f"Phone: {self.phone}"
        )
