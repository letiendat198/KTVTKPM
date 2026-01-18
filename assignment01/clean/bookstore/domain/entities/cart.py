class CartItem:
    def __init__(self, book, quantity):
        self.book = book
        self.quantity = quantity

    def subtotal(self):
        return self.book.price * self.quantity


class Cart:
    def __init__(self, id, customer_id, items):
        self.id = id
        self.customer_id = customer_id
        self.items = items

    def total_price(self):
        return sum(item.subtotal() for item in self.items)
