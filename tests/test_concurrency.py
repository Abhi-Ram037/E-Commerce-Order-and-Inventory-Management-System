
import threading
import tempfile
import unittest
from pathlib import Path

import database.db_connection as db_connection
from database.schema import create_tables
from models.order import Order


class ConcurrencyTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_connection.DATABASE_PATH

        db_connection.DATABASE_PATH = (
            Path(self.temp_dir.name) / "test_ecommerce.db"
        )

        create_tables()

        connection = db_connection.get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO Product (name, category, price, stock)
                VALUES (?, ?, ?, ?)
                """,
                ("Laptop", "Electronics", 50000, 5)
            )
            self.product_id = cursor.lastrowid

            self.customer_ids = []

            for number in range(10):
                cursor = connection.execute(
                    """
                    INSERT INTO Customer (name, email, phone)
                    VALUES (?, ?, ?)
                    """,
                    (
                        f"Customer {number + 1}",
                        f"customer{number + 1}@example.com",
                        f"90000000{number:02d}"
                    )
                )
                self.customer_ids.append(cursor.lastrowid)

            connection.commit()

        finally:
            connection.close()

    def tearDown(self):
        db_connection.DATABASE_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_concurrent_orders(self):
        barrier = threading.Barrier(10)
        results = []
        results_lock = threading.Lock()

        def place_order(customer_id):
            try:
                barrier.wait(timeout=10)

                order = Order(
                    customer_id,
                    [(self.product_id, 1)]
                )

                order_id = order.create_order()

                result = ("success", order_id)

            except Exception as error:
                result = ("error", str(error))

            with results_lock:
                results.append(result)

        threads = []

        for customer_id in self.customer_ids:
            thread = threading.Thread(
                target=place_order,
                args=(customer_id,)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=45)

        self.assertFalse(
            any(thread.is_alive() for thread in threads),
            "Some threads did not finish."
        )

        successful_orders = [
            result for result in results
            if result[0] == "success"
        ]

        failed_orders = [
            result for result in results
            if result[0] == "error"
        ]

        self.assertEqual(len(results), 10)
        self.assertEqual(len(successful_orders), 5)
        self.assertEqual(len(failed_orders), 5)

        for result in failed_orders:
            self.assertIn("Insufficient stock", result[1])

        connection = db_connection.get_connection()

        try:
            product = connection.execute(
                "SELECT stock FROM Product WHERE product_id = ?",
                (self.product_id,)
            ).fetchone()

            order_count = connection.execute(
                "SELECT COUNT(*) AS total FROM Orders"
            ).fetchone()["total"]

            item_count = connection.execute(
                "SELECT COUNT(*) AS total FROM OrderItem"
            ).fetchone()["total"]

            inventory_log_count = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM InventoryLog
                WHERE product_id = ? AND reason = 'Order placed'
                """,
                (self.product_id,)
            ).fetchone()["total"]

            self.assertEqual(product["stock"], 0)
            self.assertGreaterEqual(product["stock"], 0)
            self.assertEqual(order_count, 5)
            self.assertEqual(item_count, 5)
            self.assertEqual(inventory_log_count, 5)

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
