
from database.db_connection import get_connection


def create_tables():
    connection = get_connection()

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS Customer (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS Product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                stock INTEGER NOT NULL CHECK(stock >= 0),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL DEFAULT 0
                    CHECK(total_amount >= 0),
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN (
                        'Pending', 'Confirmed', 'Shipped',
                        'Delivered', 'Cancelled'
                    )),
                FOREIGN KEY (customer_id)
                    REFERENCES Customer(customer_id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS OrderItem (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL CHECK(unit_price >= 0),
                FOREIGN KEY (order_id)
                    REFERENCES Orders(order_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (product_id)
                    REFERENCES Product(product_id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS Payment (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                payment_method TEXT NOT NULL
                    CHECK(payment_method IN ('UPI', 'Card', 'Cash on Delivery')),
                payment_status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(payment_status IN (
                        'Pending', 'Successful', 'Failed', 'Refunded'
                    )),
                transaction_reference TEXT NOT NULL UNIQUE,
                payment_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id)
                    REFERENCES Orders(order_id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS InventoryLog (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                change_quantity INTEGER NOT NULL
                    CHECK(change_quantity != 0),
                reason TEXT NOT NULL,
                order_id INTEGER,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id)
                    REFERENCES Product(product_id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (order_id)
                    REFERENCES Orders(order_id)
                    ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_orders_customer
                ON Orders(customer_id);

            CREATE INDEX IF NOT EXISTS idx_orderitem_order
                ON OrderItem(order_id);

            CREATE INDEX IF NOT EXISTS idx_orderitem_product
                ON OrderItem(product_id);

            CREATE INDEX IF NOT EXISTS idx_payment_order
                ON Payment(order_id);

            CREATE INDEX IF NOT EXISTS idx_inventory_product
                ON InventoryLog(product_id);
        """)

        connection.commit()
        print("All database tables created successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
