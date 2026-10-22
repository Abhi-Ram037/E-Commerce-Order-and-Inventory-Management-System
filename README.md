# E-Commerce Order and Inventory Management System

## 📌 Project Overview

The **E-Commerce Order and Inventory Management System** is a Python-based command-line application designed to manage customers, products, orders, payments, and inventory efficiently.

The project uses Python object-oriented programming and SQLite for data storage. It includes transaction management, inventory tracking, sales reports, and automated tests to demonstrate reliable order processing.

## 🚀 Features

### 1. Customer Management
- Register new customers.
- Display all registered customers.
- Search customers by ID or email.
- Update customer details.
- View customer order history.

### 2. Product Management
- Add new products with name, category, price, and stock.
- Display all products.
- Search products by name.
- Filter products by category.
- Sort products by price.
- Update and delete products.
- Identify low-stock products.

### 3. Inventory Management
- Track available product quantities.
- Increase or decrease stock.
- Prevent stock from becoming negative during order processing.
- Maintain inventory logs.
- View inventory history and stock changes.

### 4. Order Management
- Create orders containing multiple products.
- Validate customer details and product availability.
- Calculate order totals automatically.
- Reduce stock when orders are placed.
- View order details and customer order history.
- Cancel eligible orders and restore inventory.
- Update order status from Confirmed to Shipped and from Shipped to Delivered.

### 5. Payment Management
- Simulate UPI payments.
- Simulate card payments.
- Support cash-on-delivery orders.
- Record successful, failed, pending, and refunded payment statuses.
- View payment history.

**Note:** Payments and refunds are simulated locally. The project does not connect to an actual payment gateway or transfer money.

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
- Use SQLite transactions to protect stock updates during concurrent order placement.
- Test simultaneous purchase attempts.
- Verify order creation, payment processing, cancellation, and stock restoration.
- Run automated tests using Python's built-in `unittest` framework.

## 🛠️ Technologies Used

- **Programming Language:** Python 3
- **Database:** SQLite3
- **Concepts:** Object-Oriented Programming, inheritance, exception handling, and modular programming
- **Database Operations:** SQL, joins, constraints, and transactions
- **Concurrency:** Python `threading` module
- **Testing:** Python `unittest` framework
- **Version Control:** Git and GitHub

## 📂 Project Structure

```text
ecommerce_system/
│
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   └── schema.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── customer.py
│   ├── product.py
│   ├── order.py
│   └── payment.py
│
├── services/
│   ├── __init__.py
│   ├── ecommerce_system.py
│   └── inventory_manager.py
│
├── reports/
│   ├── __init__.py
│   └── sales_reports.py
│
├── tests/
│   ├── test_concurrency.py
│   └── test_ecommerce.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3 installed on your system.
- Git installed on your system.
- A terminal such as PowerShell or the VS Code terminal.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Abhi-Ram037/E-Commerce-Order-and-Inventory-Management-System.git
```

### Step 2: Navigate to the Project Directory

```bash
cd E-Commerce-Order-and-Inventory-Management-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run Python directly through the virtual environment without changing the execution policy:

```powershell
.\venv\Scripts\python.exe main.py
```

### Step 5: Install Dependencies

The current implementation uses Python's standard library, including `sqlite3`, `threading`, and `unittest`. No third-party packages are required.

If a `requirements.txt` file is present:

```bash
python -m pip install -r requirements.txt
```

## ▶️ Running the Application

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

Follow the on-screen prompts to perform operations.

## 🧪 Running Automated Tests

Run all tests:

```bash
python -m unittest discover -s tests -v
```

Run the concurrency test separately:

```bash
python -m unittest discover -s tests -p "test_concurrency.py" -v
```

Run the core functionality tests separately:

```bash
python -m unittest discover -s tests -p "test_ecommerce.py" -v
```

A successful test run should finish with `OK`. The number of tests depends on the test methods currently present in the repository.

## 🗄️ Database Design

The application uses the following SQLite tables:

| Table | Purpose |
|---|---|
| `Customer` | Stores customer details |
| `Product` | Stores product information, price, and stock |
| `Orders` | Stores order details, totals, and status |
| `OrderItem` | Stores products and quantities associated with each order |
| `Payment` | Records payment methods, amounts, and statuses |
| `InventoryLog` | Tracks inventory changes and related orders |

Foreign keys and database constraints help maintain relationships and data consistency. Transactions protect critical order and stock operations.

## 🔒 Important Notes

- This project is intended for educational and demonstration purposes.
- Payment processing and refunds are simulated; no real transactions occur.
- SQLite is suitable for this learning project, but a production application may require a more scalable database and additional concurrency controls.
- Authentication, authorization, and production-grade payment integration are not included in the current implementation.
- Keep your virtual environment, local database, and secret configuration files out of version control.

## 🔮 Future Enhancements

- Build a REST API using Django REST Framework or FastAPI.
- Add user authentication and role-based access control.
- Integrate a payment gateway in a secure test environment.
- Implement delivery tracking and notifications.
- Add a web-based user interface.
- Export reports to CSV or Excel.
- Add logging and continuous integration for automated tests.

## 🎯 Learning Outcomes

This project demonstrates practical application of:

- Python classes and inheritance.
- Modular application design.
- SQLite database integration.
- SQL queries and relationships.
- Exception handling and validation.
- Transaction management.
- Inventory and order processing.
- Multithreading and concurrency testing.
- Automated software testing.
- Git and GitHub version control.

## 👨‍💻 Author

**Abhiram**

GitHub: [Abhi-Ram037](https://github.com/Abhi-Ram037)

## 📄 License

This project is intended for learning and demonstration purposes. Add a license file if you wish to distribute the project under specific reuse terms.
