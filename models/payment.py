
import uuid
from database.db_connection import get_connection


class Payment:
    METHODS = ("UPI", "Card", "Cash on Delivery")

    def __init__(
        self,
        order_id,
        amount,
        payment_method,
        transaction_reference=None
    ):
        self.order_id = order_id
        self.amount = round(float(amount), 2)
        self.payment_method = payment_method
        self.transaction_reference = (
            transaction_reference or f"TXN-{uuid.uuid4().hex.upper()}"
        )

    def process_payment(self, simulate_success=True):
        if self.payment_method not in self.METHODS:
            raise ValueError("Invalid payment method.")

        if self.amount < 0:
            raise ValueError("Payment amount cannot be negative.")

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            order = connection.execute(
                """
                SELECT order_id, total_amount, status
                FROM Orders
                WHERE order_id = ?
                """,
                (self.order_id,)
            ).fetchone()

            if order is None:
                raise ValueError("Order not found.")

            if order["status"] != "Pending":
                raise ValueError(
                    "Only pending orders can be paid."
                )

            if round(order["total_amount"], 2) != self.amount:
                raise ValueError(
                    "Payment amount does not match the order total."
                )

            duplicate = connection.execute(
                """
                SELECT payment_id
                FROM Payment
                WHERE transaction_reference = ?
                """,
                (self.transaction_reference,)
            ).fetchone()

            if duplicate:
                raise ValueError(
                    "Transaction reference has already been used."
                )

            successful_payment = connection.execute(
                """
                SELECT payment_id
                FROM Payment
                WHERE order_id = ?
                AND payment_status = 'Successful'
                """,
                (self.order_id,)
            ).fetchone()

            if successful_payment:
                raise ValueError(
                    "This order already has a successful payment."
                )

            if self.payment_method == "Cash on Delivery":
                payment_status = "Pending"
                order_status = "Confirmed"
            elif simulate_success:
                payment_status = "Successful"
                order_status = "Confirmed"
            else:
                payment_status = "Failed"
                order_status = "Pending"

            connection.execute(
                """
                INSERT INTO Payment (
                    order_id, amount, payment_method,
                    payment_status, transaction_reference
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.order_id,
                    self.amount,
                    self.payment_method,
                    payment_status,
                    self.transaction_reference
                )
            )

            if order_status == "Confirmed":
                connection.execute(
                    """
                    UPDATE Orders
                    SET status = 'Confirmed'
                    WHERE order_id = ?
                    AND status = 'Pending'
                    """,
                    (self.order_id,)
                )

            connection.commit()

            return {
                "order_id": self.order_id,
                "amount": self.amount,
                "method": self.payment_method,
                "status": payment_status,
                "transaction_reference": self.transaction_reference
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_payments(order_id=None):
        connection = get_connection()

        try:
            if order_id is not None:
                return connection.execute(
                    """
                    SELECT * FROM Payment
                    WHERE order_id = ?
                    ORDER BY payment_id DESC
                    """,
                    (order_id,)
                ).fetchall()

            return connection.execute(
                """
                SELECT * FROM Payment
                ORDER BY payment_id DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def __str__(self):
        return (
            f"Order ID: {self.order_id}, "
            f"Amount: {self.amount:.2f}, "
            f"Method: {self.payment_method}, "
            f"Reference: {self.transaction_reference}"
        )
