from abc import ABC, abstractmethod


class CartRepository(ABC):

    @abstractmethod
    def get_or_create_cart(self, customer_id):
        """Return existing cart or create a new one"""
        pass

    @abstractmethod
    def get_cart_by_customer(self, customer_id):
        """Return cart belonging to a customer"""
        pass

    @abstractmethod
    def get_items(self, cart_id):
        """Return all items in a cart"""
        pass

    @abstractmethod
    def get_item(self, cart_id, book_id):
        """Return a specific cart item"""
        pass

    @abstractmethod
    def add_item(self, cart_id, book_id, quantity):
        """Add a new item to cart"""
        pass

    @abstractmethod
    def update_item(self, cart_item):
        """Update existing cart item (e.g., quantity)"""
        pass
