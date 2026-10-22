
from database.db_connection import get_connection


class SalesReports:

    @staticmethod
    def customer_summary():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    c.customer_id,
                    c.name,
                    c.email,
                    COUNT(DISTINCT o.order_id) AS total_orders,
                    COALESCE(SUM(
                        CASE
                            WHEN p.payment_status = 'Successful'
                            THEN p.amount
                            ELSE 0
                        END
                    ), 0) AS successful_purchase_amount
                FROM Customer c
                LEFT JOIN Orders o
                    ON c.customer_id = o.customer_id
                LEFT JOIN Payment p
                    ON o.order_id = p.order_id
                GROUP BY c.customer_id, c.name, c.email
                ORDER BY successful_purchase_amount DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def low_stock_products(threshold=5):
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT product_id, name, category, price, stock
                FROM Product
                WHERE stock <= ?
                ORDER BY stock ASC
            """, (threshold,)).fetchall()
        finally:
            connection.close()

    @staticmethod
    def price_extremes():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    MIN(price) AS lowest_price,
                    MAX(price) AS highest_price
                FROM Product
            """).fetchone()
        finally:
            connection.close()

    @staticmethod
    def never_ordered_products():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT p.product_id, p.name, p.category, p.price, p.stock
                FROM Product p
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM OrderItem oi
                    WHERE oi.product_id = p.product_id
                )
                ORDER BY p.name
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def quantity_sold():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    COALESCE(SUM(
                        CASE
                            WHEN o.status != 'Cancelled'
                            THEN oi.quantity
                            ELSE 0
                        END
                    ), 0) AS quantity_sold
                FROM Product p
                LEFT JOIN OrderItem oi
                    ON p.product_id = oi.product_id
                LEFT JOIN Orders o
                    ON oi.order_id = o.order_id
                GROUP BY p.product_id, p.name
                ORDER BY quantity_sold DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def best_selling_products():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    SUM(oi.quantity) AS quantity_sold
                FROM Product p
                JOIN OrderItem oi
                    ON p.product_id = oi.product_id
                JOIN Orders o
                    ON oi.order_id = o.order_id
                WHERE o.status != 'Cancelled'
                GROUP BY p.product_id, p.name
                ORDER BY quantity_sold DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def category_sales():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    p.category,
                    SUM(oi.quantity) AS quantity_sold,
                    ROUND(
                        SUM(oi.quantity * oi.unit_price), 2
                    ) AS order_value
                FROM OrderItem oi
                JOIN Product p
                    ON oi.product_id = p.product_id
                JOIN Orders o
                    ON oi.order_id = o.order_id
                WHERE o.status != 'Cancelled'
                GROUP BY p.category
                ORDER BY order_value DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def total_revenue():
        connection = get_connection()
        try:
            result = connection.execute("""
                SELECT COALESCE(SUM(amount), 0) AS revenue
                FROM Payment
                WHERE payment_status = 'Successful'
            """).fetchone()
            return result["revenue"]
        finally:
            connection.close()

    @staticmethod
    def daily_sales():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    DATE(o.order_date) AS sale_date,
                    COUNT(DISTINCT o.order_id) AS total_orders,
                    ROUND(SUM(p.amount), 2) AS revenue
                FROM Orders o
                JOIN Payment p
                    ON o.order_id = p.order_id
                WHERE p.payment_status = 'Successful'
                    AND o.status != 'Cancelled'
                GROUP BY DATE(o.order_date)
                ORDER BY sale_date DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def monthly_sales():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    STRFTIME('%Y-%m', o.order_date) AS sale_month,
                    COUNT(DISTINCT o.order_id) AS total_orders,
                    ROUND(SUM(p.amount), 2) AS revenue
                FROM Orders o
                JOIN Payment p
                    ON o.order_id = p.order_id
                WHERE p.payment_status = 'Successful'
                    AND o.status != 'Cancelled'
                GROUP BY STRFTIME('%Y-%m', o.order_date)
                ORDER BY sale_month DESC
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def order_status_counts():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT status, COUNT(*) AS total_orders
                FROM Orders
                GROUP BY status
                ORDER BY status
            """).fetchall()
        finally:
            connection.close()

    @staticmethod
    def payment_summary():
        connection = get_connection()
        try:
            return connection.execute("""
                SELECT
                    payment_status,
                    COUNT(*) AS total_payments,
                    ROUND(SUM(amount), 2) AS total_amount
                FROM Payment
                GROUP BY payment_status
                ORDER BY payment_status
            """).fetchall()
        finally:
            connection.close()
