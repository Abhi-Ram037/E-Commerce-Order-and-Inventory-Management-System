
import sqlite3

from database.schema import create_tables
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.payment import Payment
from reports.sales_reports import SalesReports
from services.ecommerce_system import ECommerceSystem
from services.inventory_manager import InventoryManager


system = ECommerceSystem()
inventory = InventoryManager()


def print_rows(rows):
    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(dict(row))


def customer_menu():
    while True:
        print("\n===== Customer Management =====")
        print("1. Register Customer")
        print("2. Display All Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. View Customer Order History")
        print("6. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Enter name: ").strip()
                email = input("Enter email: ").strip()
                phone = input("Enter phone: ").strip()

                customer_id = system.register_customer(
                    name, email, phone
                )
                print("Customer registered. ID:", customer_id)

            elif choice == "2":
                print_rows(Customer.display_all())

            elif choice == "3":
                search_type = input(
                    "Search by ID or email: "
                ).strip().lower()

                if search_type == "id":
                    customer_id = int(input("Enter customer ID: "))
                    customer = Customer.search(
                        customer_id=customer_id
                    )
                elif search_type == "email":
                    email = input("Enter email: ").strip()
                    customer = Customer.search(email=email)
                else:
                    print("Choose ID or email.")
                    continue

                if customer:
                    print(dict(customer))
                else:
                    print("Customer not found.")

            elif choice == "4":
                customer_id = int(input("Enter customer ID: "))
                name = input("Enter new name: ").strip()
                email = input("Enter new email: ").strip()
                phone = input("Enter new phone: ").strip()

                updated = Customer.update(
                    customer_id, name, email, phone
                )

                if updated:
                    print("Customer updated successfully.")
                else:
                    print("Customer not found.")

            elif choice == "5":
                customer_id = int(input("Enter customer ID: "))
                print_rows(Customer.order_history(customer_id))

            elif choice == "6":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print("Input error:", error)
        except sqlite3.Error as error:
            print("Database error:", error)


def product_menu():
    while True:
        print("\n===== Product Management =====")
        print("1. Add Product")
        print("2. Display Products")
        print("3. Search Product by Name")
        print("4. Filter by Category")
        print("5. Sort Products by Price")
        print("6. Update Product")
        print("7. Delete Product")
        print("8. View Low-Stock Products")
        print("9. Adjust Inventory")
        print("10. View Inventory History")
        print("11. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Product name: ").strip()
                category = input("Category: ").strip()
                price = float(input("Price: "))
                stock = int(input("Initial stock: "))

                product_id = system.add_product(
                    name, category, price, stock
                )
                print("Product added. ID:", product_id)

            elif choice == "2":
                print_rows(Product.display_all())

            elif choice == "3":
                name = input("Enter product name: ").strip()
                print_rows(Product.search_by_name(name))

            elif choice == "4":
                category = input("Enter category: ").strip()
                print_rows(Product.filter_by_category(category))

            elif choice == "5":
                print_rows(Product.sort_by_price())

            elif choice == "6":
                product_id = int(input("Product ID: "))
                name = input("New name: ").strip()
                category = input("New category: ").strip()
                price = float(input("New price: "))
                stock = int(input("New stock: "))

                updated = Product.update_product(
                    product_id, name, category, price, stock
                )

                print(
                    "Product updated successfully."
                    if updated else "Product not found."
                )

            elif choice == "7":
                product_id = int(input("Product ID to delete: "))
                deleted = Product.delete_product(product_id)

                if deleted:
                    print(
                        "Product deleted if it existed and "
                        "was not referenced by existing records."
                    )
                else:
                    print(
                        "Cannot delete product because it is "
                        "referenced by existing records."
                    )

            elif choice == "8":
                threshold = int(input("Stock threshold: "))
                print_rows(
                    inventory.get_low_stock_products(threshold)
                )

            elif choice == "9":
                product_id = int(input("Product ID: "))
                quantity = int(
                    input("Stock change (+ to add, - to remove): ")
                )
                reason = input("Reason for adjustment: ").strip()

                updated = inventory.adjust_stock(
                    product_id, quantity, reason
                )

                print(
                    "Inventory updated successfully."
                    if updated else
                    "Product not found or insufficient stock."
                )

            elif choice == "10":
                product_id = int(input("Product ID: "))
                print_rows(
                    inventory.get_inventory_history(product_id)
                )

            elif choice == "11":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print("Input error:", error)
        except sqlite3.Error as error:
            print("Database error:", error)


def order_menu():
    while True:
        print("\n===== Order Management =====")
        print("1. Place Order")
        print("2. View Order Details")
        print("3. View Customer Order History")
        print("4. Cancel Order")
        print("5. Update Order Status")
        print("6. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                customer_id = int(input("Customer ID: "))
                items = []

                while True:
                    product_id = int(input("Product ID: "))
                    quantity = int(input("Quantity: "))
                    items.append((product_id, quantity))

                    more = input(
                        "Add another product? (yes/no): "
                    ).strip().lower()

                    if more not in ("yes", "y"):
                        break

                order_id = system.place_order(customer_id, items)
                print("Order created successfully. ID:", order_id)

            elif choice == "2":
                order_id = int(input("Order ID: "))
                details = system.get_order_details(order_id)

                if details is None:
                    print("Order not found.")
                else:
                    print("\nOrder Details:")
                    print(dict(details["order"]))

                    print("\nOrder Items:")
                    print_rows(details["items"])

            elif choice == "3":
                customer_id = int(input("Customer ID: "))
                print_rows(
                    system.get_customer_order_history(customer_id)
                )

            elif choice == "4":
                order_id = int(input("Order ID to cancel: "))
                print(system.cancel_order(order_id))

            elif choice == "5":
                order_id = int(input("Order ID: "))

                print("1. Mark as Shipped")
                print("2. Mark as Delivered")

                status_choice = input(
                    "Choose status: "
                ).strip()

                statuses = {
                    "1": "Shipped",
                    "2": "Delivered"
                }

                if status_choice not in statuses:
                    print("Invalid status choice.")
                    continue

                message = system.update_order_status(
                    order_id,
                    statuses[status_choice]
                )
                print(message)

            elif choice == "6":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print("Order error:", error)
        except sqlite3.Error as error:
            print("Database error:", error)


def payment_menu():
    while True:
        print("\n===== Payment Management =====")
        print("1. Process Payment")
        print("2. View All Payments")
        print("3. View Payments for an Order")
        print("4. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                order_id = int(input("Order ID: "))
                details = system.get_order_details(order_id)

                if details is None:
                    print("Order not found.")
                    continue

                order = details["order"]

                print(
                    f"Order total: {order['total_amount']:.2f}"
                )
                print("Order status:", order["status"])

                amount = float(input("Payment amount: "))

                print("1. UPI")
                print("2. Card")
                print("3. Cash on Delivery")

                method_choice = input(
                    "Choose payment method: "
                ).strip()

                methods = {
                    "1": "UPI",
                    "2": "Card",
                    "3": "Cash on Delivery"
                }

                if method_choice not in methods:
                    print("Invalid payment method.")
                    continue

                method = methods[method_choice]
                simulate_success = True

                if method in ("UPI", "Card"):
                    answer = input(
                        "Simulate successful payment? (yes/y, no/n): "
                    ).strip().lower()

                    if answer in ("yes", "y"):
                        simulate_success = True
                    elif answer in ("no", "n"):
                        simulate_success = False
                    else:
                        print("Invalid choice. Enter yes/y or no/n.")
                        continue

                result = system.process_payment(
                    order_id,
                    amount,
                    method,
                    simulate_success
                )

                print("\nPayment Result:")
                print(result)

            elif choice == "2":
                print_rows(Payment.get_payments())

            elif choice == "3":
                order_id = int(input("Order ID: "))
                print_rows(Payment.get_payments(order_id))

            elif choice == "4":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print("Payment error:", error)
        except sqlite3.Error as error:
            print("Database error:", error)


def reports_menu():
    while True:
        print("\n===== Sales Reports =====")
        print("1. Customer Summary")
        print("2. Low-Stock Products")
        print("3. Lowest and Highest Product Prices")
        print("4. Products Never Ordered")
        print("5. Quantity Sold")
        print("6. Best-Selling Products")
        print("7. Category-Wise Sales")
        print("8. Total Revenue")
        print("9. Daily Sales")
        print("10. Monthly Sales")
        print("11. Order Status Counts")
        print("12. Payment Summary")
        print("13. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                print_rows(SalesReports.customer_summary())

            elif choice == "2":
                threshold = int(input("Stock threshold: "))
                print_rows(
                    SalesReports.low_stock_products(threshold)
                )

            elif choice == "3":
                result = SalesReports.price_extremes()
                print("Lowest price:", result["lowest_price"])
                print("Highest price:", result["highest_price"])

            elif choice == "4":
                print_rows(SalesReports.never_ordered_products())

            elif choice == "5":
                print_rows(SalesReports.quantity_sold())

            elif choice == "6":
                print_rows(SalesReports.best_selling_products())

            elif choice == "7":
                print_rows(SalesReports.category_sales())

            elif choice == "8":
                print(
                    f"Total revenue: "
                    f"{SalesReports.total_revenue():.2f}"
                )

            elif choice == "9":
                print_rows(SalesReports.daily_sales())

            elif choice == "10":
                print_rows(SalesReports.monthly_sales())

            elif choice == "11":
                print_rows(SalesReports.order_status_counts())

            elif choice == "12":
                print_rows(SalesReports.payment_summary())

            elif choice == "13":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print("Report error:", error)
        except sqlite3.Error as error:
            print("Database error:", error)


def main():
    create_tables()

    while True:
        print("\n===== E-Commerce Management System =====")
        print("1. Customer Management")
        print("2. Product Management")
        print("3. Order Management")
        print("4. Payment Management")
        print("5. Sales Reports")
        print("6. View All Inventory")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            customer_menu()

        elif choice == "2":
            product_menu()

        elif choice == "3":
            order_menu()

        elif choice == "4":
            payment_menu()

        elif choice == "5":
            reports_menu()

        elif choice == "6":
            print_rows(inventory.get_inventory())

        elif choice == "7":
            print("Application closed.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
