
class User:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def get_details(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Phone: {self.phone}"
