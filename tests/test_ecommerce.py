
import tempfile
import unittest
from pathlib import Path

import database.db_connection as db_connection
from database.schema import create_tables
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.payment import Payment


class ECommerceTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = db_connection.DATABASE_PATH

        db_connection.DATABASE_PATH = (
            Path(self.temp_dir.name) / "test_ecommerce.db"
        )

        create_tables()

        self.customer = Customer(
            "Abhi",
            "abhi@example.com",
            "9876543210"
        )
        self.customer_id = self.customer.register()

        self.product = Product(
            "Laptop",
            "Electronics",
            50000,
            10
        )
        self.product_id = self.product.add_product()

    def tearDown(self):
        db_connection.DATABASE_PATH = self.original_database_path
        self.temp_dir.cleanup()

    def test_customer_registration(self):
        customer = Customer.search(customer_id=self.customer_id)

        self.assertIsNotNone(customer)
        self.assertEqual(customer["name"], "Abhi")

    def test_duplicate_customer_email(self):
        duplicate = Customer(
            "Another Customer",
            "ABHI@example.com",
            "9999999999"
        )

        with self.assertRaises(ValueError):
            duplicate.register()

    def test_product_creation(self):
        product = Product(
            "Mouse",
            "Accessories",
            500,
            20
        )

        product_id = product.add_product()

        self.assertGreater(product_id, 0)

        products = Product.display_all()
        self.assertEqual(len(products), 2)

    def test_order_reduces_stock(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 2)]
        )

        order_id = order.create_order()

        self.assertGreater(order_id, 0)

        product = next(
            item for item in Product.display_all()
            if item["product_id"] == self.product_id
        )

        self.assertEqual(product["stock"], 8)

    def test_insufficient_stock_creates_no_order(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 100)]
        )

        with self.assertRaises(ValueError):
            order.create_order()

        connection = db_connection.get_connection()

        try:
            order_count = connection.execute(
                "SELECT COUNT(*) AS total FROM Orders"
            ).fetchone()["total"]

            product = connection.execute(
                "SELECT stock FROM Product WHERE product_id = ?",
                (self.product_id,)
            ).fetchone()

            self.assertEqual(order_count, 0)
            self.assertEqual(product["stock"], 10)

        finally:
            connection.close()

    def test_successful_payment(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 1)]
        )

        order_id = order.create_order()

        payment = Payment(
            order_id,
            50000,
            "UPI"
        )

        result = payment.process_payment()

        self.assertEqual(result["status"], "Successful")

        details = Order.get_order_details(order_id)

        self.assertEqual(details["order"]["status"], "Confirmed")

    def test_cancellation_restores_stock_and_refunds(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 2)]
        )

        order_id = order.create_order()

        Payment(
            order_id,
            100000,
            "Card"
        ).process_payment()

        message = Order.cancel_order(order_id)

        self.assertIn("Order cancelled", message)

        details = Order.get_order_details(order_id)
        self.assertEqual(details["order"]["status"], "Cancelled")

        product = next(
            item for item in Product.display_all()
            if item["product_id"] == self.product_id
        )

        self.assertEqual(product["stock"], 10)

        payments = Payment.get_payments(order_id)
        self.assertEqual(payments[0]["payment_status"], "Refunded")

        
    def test_order_status_workflow(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 1)]
        )

        order_id = order.create_order()

        Payment(
            order_id,
            50000,
            "UPI"
        ).process_payment()

        message = Order.update_status(order_id, "Shipped")
        self.assertIn("Shipped", message)

        message = Order.update_status(order_id, "Delivered")
        self.assertIn("Delivered", message)

        details = Order.get_order_details(order_id)
        self.assertEqual(
            details["order"]["status"],
            "Delivered"
        )

    def test_invalid_order_status_transition(self):
        order = Order(
            self.customer_id,
            [(self.product_id, 1)]
        )

        order_id = order.create_order()

        with self.assertRaises(ValueError):
            Order.update_status(order_id, "Delivered")

        details = Order.get_order_details(order_id)

        self.assertEqual(
            details["order"]["status"],
            "Pending"
        )



if __name__ == "__main__":
    unittest.main()
