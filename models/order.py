
from database.db_connection import get_connection


class Order:

    def __init__(self, customer_id, items, order_id=None):
        self.customer_id = customer_id
        self.items = items
        self.order_id = order_id
        self.total_amount = 0.0

    def create_order(self):
        if not self.items:
            raise ValueError("An order must contain at least one product.")

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            customer = connection.execute(
                "SELECT customer_id FROM Customer WHERE customer_id = ?",
                (self.customer_id,)
            ).fetchone()

            if customer is None:
                raise ValueError("Customer does not exist.")

            order_items = {}

            for product_id, quantity in self.items:
                if (
                    isinstance(product_id, bool)
                    or not isinstance(product_id, int)
                    or product_id <= 0
                ):
                    raise ValueError(
                        "Product ID must be a positive integer."
                    )

                if (
                    isinstance(quantity, bool)
                    or not isinstance(quantity, int)
                    or quantity <= 0
                ):
                    raise ValueError(
                        "Quantity must be a positive integer."
                    )

                order_items[product_id] = (
                    order_items.get(product_id, 0) + quantity
                )

            products = {}

            for product_id, quantity in order_items.items():
                product = connection.execute(
                    """
                    SELECT product_id, name, price, stock
                    FROM Product
                    WHERE product_id = ?
                    """,
                    (product_id,)
                ).fetchone()

                if product is None:
                    raise ValueError(
                        f"Product ID {product_id} does not exist."
                    )

                if product["stock"] < quantity:
                    raise ValueError(
                        f"Insufficient stock for {product['name']}. "
                        f"Available: {product['stock']}, "
                        f"Requested: {quantity}."
                    )

                products[product_id] = product

            cursor = connection.execute(
                """
                INSERT INTO Orders (customer_id, total_amount, status)
                VALUES (?, 0, 'Pending')
                """,
                (self.customer_id,)
            )

            self.order_id = cursor.lastrowid
            self.total_amount = 0.0

            for product_id, quantity in order_items.items():
                product = products[product_id]
                unit_price = product["price"]

                line_total = round(unit_price * quantity, 2)

                cursor = connection.execute(
                    """
                    UPDATE Product
                    SET stock = stock - ?
                    WHERE product_id = ? AND stock >= ?
                    """,
                    (quantity, product_id, quantity)
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        f"Insufficient stock for {product['name']}."
                    )

                connection.execute(
                    """
                    INSERT INTO OrderItem
                    (order_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        self.order_id,
                        product_id,
                        quantity,
                        unit_price
                    )
                )

                connection.execute(
                    """
                    INSERT INTO InventoryLog
                    (product_id, change_quantity, reason, order_id)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        product_id,
                        -quantity,
                        "Order placed",
                        self.order_id
                    )
                )

                self.total_amount += line_total

            self.total_amount = round(self.total_amount, 2)

            connection.execute(
                """
                UPDATE Orders
                SET total_amount = ?
                WHERE order_id = ?
                """,
                (self.total_amount, self.order_id)
            )

            connection.commit()

            return self.order_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_order_details(order_id):
        connection = get_connection()

        try:
            order = connection.execute(
                """
                SELECT
                    o.order_id,
                    o.order_date,
                    o.total_amount,
                    o.status,
                    c.customer_id,
                    c.name,
                    c.email
                FROM Orders o
                JOIN Customer c
                    ON o.customer_id = c.customer_id
                WHERE o.order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if order is None:
                return None

            items = connection.execute(
                """
                SELECT
                    p.product_id,
                    p.name,
                    oi.quantity,
                    oi.unit_price,
                    oi.quantity * oi.unit_price AS line_total
                FROM OrderItem oi
                JOIN Product p
                    ON oi.product_id = p.product_id
                WHERE oi.order_id = ?
                """,
                (order_id,)
            ).fetchall()

            return {
                "order": order,
                "items": items
            }

        finally:
            connection.close()

    @staticmethod
    def customer_history(customer_id):
        connection = get_connection()

        try:
            customer = connection.execute(
                """
                SELECT customer_id
                FROM Customer
                WHERE customer_id = ?
                """,
                (customer_id,)
            ).fetchone()

            if customer is None:
                raise ValueError("Customer does not exist.")

            return connection.execute(
                """
                SELECT
                    order_id,
                    order_date,
                    total_amount,
                    status
                FROM Orders
                WHERE customer_id = ?
                ORDER BY order_date DESC, order_id DESC
                """,
                (customer_id,)
            ).fetchall()

        finally:
            connection.close()

    @staticmethod
    def cancel_order(order_id):
        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            order = connection.execute(
                """
                SELECT order_id, status
                FROM Orders
                WHERE order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if order is None:
                raise ValueError("Order not found.")

            if order["status"] == "Cancelled":
                raise ValueError("Order is already cancelled.")

            if order["status"] == "Delivered":
                raise ValueError(
                    "Delivered orders cannot be cancelled."
                )

            if order["status"] == "Shipped":
                raise ValueError(
                    "Shipped orders cannot be cancelled."
                )

            if order["status"] not in ("Pending", "Confirmed"):
                raise ValueError("Order cannot be cancelled.")

            items = connection.execute(
                """
                SELECT product_id, quantity
                FROM OrderItem
                WHERE order_id = ?
                """,
                (order_id,)
            ).fetchall()

            if not items:
                raise ValueError(
                    "Order has no items to restore."
                )

            for item in items:
                connection.execute(
                    """
                    UPDATE Product
                    SET stock = stock + ?
                    WHERE product_id = ?
                    """,
                    (item["quantity"], item["product_id"])
                )

                connection.execute(
                    """
                    INSERT INTO InventoryLog
                    (product_id, change_quantity, reason, order_id)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        item["product_id"],
                        item["quantity"],
                        "Order cancellation - stock restored",
                        order_id
                    )
                )

            connection.execute(
                """
                UPDATE Payment
                SET payment_status = 'Refunded'
                WHERE order_id = ?
                  AND payment_status = 'Successful'
                """,
                (order_id,)
            )

            connection.execute(
                """
                UPDATE Orders
                SET status = 'Cancelled'
                WHERE order_id = ?
                """,
                (order_id,)
            )

            connection.commit()

            return (
                "Order cancelled successfully. "
                "Inventory restored and eligible payments "
                "marked as refunded."
            )

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def __str__(self):
        return (
            f"Order ID: {self.order_id}, "
            f"Customer ID: {self.customer_id}, "
            f"Total: {self.total_amount:.2f}"
        )

    
    @staticmethod
    def update_status(order_id, new_status):
        allowed_transitions = {
            "Confirmed": ("Shipped", "Delivered"),
            "Shipped": ("Delivered",)
        }

        if new_status not in ("Shipped", "Delivered"):
            raise ValueError(
                "Status can only be updated to Shipped or Delivered."
            )

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            order = connection.execute(
                "SELECT status FROM Orders WHERE order_id = ?",
                (order_id,)
            ).fetchone()

            if order is None:
                raise ValueError("Order not found.")

            current_status = order["status"]

            if new_status not in allowed_transitions.get(
                current_status, ()
            ):
                raise ValueError(
                    f"Cannot change order status from "
                    f"{current_status} to {new_status}."
                )

            connection.execute(
                "UPDATE Orders SET status = ? WHERE order_id = ?",
                (new_status, order_id)
            )

            connection.commit()

            return (
                f"Order {order_id} status updated to {new_status}."
            )

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

