# E-Commerce Order and Inventory Management System

## Project Overview

The E-Commerce Order and Inventory Management System is a Python-based command-line application designed to manage customers, products, orders, payments, and inventory.

The project uses object-oriented programming and SQLite for data storage. It includes transaction management, inventory tracking, sales reports, and automated testing.

## Features

### 1. Customer Management
- Register new customers.
- Display all customers.
- Search customers by ID or email.
- Update customer details.
- View customer order history.

### 2. Product Management
- Add and display products.
- Search products by name.
- Filter products by category.
- Sort products by price.
- Update and delete products.
- Identify low-stock products.

### 3. Inventory Management
- Track product stock.
- Increase or decrease stock.
- Prevent stock from becoming negative during order processing.
- Maintain inventory logs.
- View inventory history.

### 4. Order Management
- Create orders containing multiple products.
- Validate customer details and product availability.
- Calculate order totals automatically.
- Reduce stock when orders are placed.
- View order details and customer order history.
- Cancel eligible orders and restore inventory.
- Update order status from Confirmed to Shipped and from Shipped to Delivered.

### 5. Payment Management
- Simulate UPI and card payments.
- Support cash on delivery.
- Record successful, failed, pending, and refunded payment statuses.
- View payment history.

**Note:** Payments and refunds are simulated. No real transactions are processed.

### 6. Sales Reports
- Customer purchase summaries.
- Low-stock product reports.
- Lowest and highest product prices.
- Products that have never been ordered.
- Quantity sold by product.
- Best-selling products.
- Category-wise sales.
- Total revenue.
- Daily and monthly sales.
- Order status summaries.
- Payment summaries.

### 7. Concurrency and Testing
- Use SQLite transactions for order and inventory operations.
- Test simultaneous purchase attempts.
- Test order creation, payments, cancellations, and stock restoration.
- Run automated tests using Python's built-in `unittest` framework.

## Technologies Used

- Python 3
- SQLite3
- Object-oriented programming
- SQL and database transactions
- Python `threading` module
- Python `unittest` framework
- Git and GitHub

## Project Structure

```text
ecommerce_system/
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   └── schema.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── customer.py
│   ├── product.py
│   ├── order.py
│   └── payment.py
├── services/
│   ├── __init__.py
│   ├── ecommerce_system.py
│   └── inventory_manager.py
├── reports/
│   ├── __init__.py
│   └── sales_reports.py
├── tests/
│   ├── test_concurrency.py
│   └── test_ecommerce.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites
- Python 3
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Abhi-Ram037/E-Commerce-Order-and-Inventory-Management-System.git
```

### 2. Navigate to the Project Directory

```bash
cd E-Commerce-Order-and-Inventory-Management-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

The current implementation uses Python's standard library and does not require third-party packages.

If a `requirements.txt` file is present, run:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

From the project root, run:

```bash
python main.py
```

The application creates the required SQLite database tables when it starts.

The main menu provides access to:

1. Customer Management
2. Product Management
3. Order Management
4. Payment Management
5. Sales Reports
6. View All Inventory
7. Exit

## Running Automated Tests

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Run the concurrency test:

```bash
python -m unittest discover -s tests -p "test_concurrency.py" -v
```

Run the core functionality tests:

```bash
python -m unittest discover -s tests -p "test_ecommerce.py" -v
```

A successful test run should finish with `OK`.

## Database Design

The application uses the following SQLite tables:

| Table | Purpose |
|---|---|
| `Customer` | Stores customer details |
| `Product` | Stores product information, price, and stock |
| `Orders` | Stores order details, totals, and status |
| `OrderItem` | Stores products and quantities for each order |
| `Payment` | Records payment methods, amounts, and statuses |
| `InventoryLog` | Tracks inventory changes and related orders |

Foreign keys, database constraints, and transactions help maintain data consistency.

## Important Notes

- This project is intended for educational purposes.
- Payments and refunds are simulated; no real money is transferred.
- Authentication and production-grade payment integration are not included.
- Keep virtual environments, local database files, and secret configuration files out of version control.

## Future Enhancements

- Build a REST API using Django REST Framework or FastAPI.
- Add authentication and role-based access control.
- Integrate a payment gateway.
- Implement delivery tracking and notifications.
- Add a web-based user interface.
- Export reports to CSV or Excel.
- Add continuous integration for automated tests.

## Learning Outcomes

This project demonstrates:

- Python classes and inheritance.
- Modular application design.
- SQLite database integration.
- SQL queries and relationships.
- Exception handling and validation.
- Transaction management.
- Inventory and order processing.
- Multithreading and automated testing.
- Git and GitHub version control.

## Author

**Abhiram**

GitHub: [Abhi-Ram037](https://github.com/Abhi-Ram037)

## License

This project is intended for learning and demonstration purposes. Add a license file if you plan to distribute it under specific reuse terms.
