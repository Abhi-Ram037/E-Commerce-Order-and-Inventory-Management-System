
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.payment import Payment


class ECommerceSystem:

    def register_customer(self, name, email, phone):
        customer = Customer(name, email, phone)
        return customer.register()

    def add_product(self, name, category, price, stock):
        product = Product(name, category, price, stock)
        return product.add_product()

    def place_order(self, customer_id, items):
        order = Order(customer_id, items)
        return order.create_order()

    def process_payment(
        self,
        order_id,
        amount,
        payment_method,
        simulate_success=True
    ):
        payment = Payment(order_id, amount, payment_method)
        return payment.process_payment(simulate_success)

    def cancel_order(self, order_id):
        return Order.cancel_order(order_id)

    def get_order_details(self, order_id):
        return Order.get_order_details(order_id)

    def get_customer_order_history(self, customer_id):
        return Order.customer_history(customer_id)

    
    def update_order_status(self, order_id, new_status):
        return Order.update_status(order_id, new_status)

