from bookstore.interfaces.repositories.cart_repository import CartRepository
from ..orm.models import Cart, CartItem, Book


class DjangoCartRepository(CartRepository):

    def get_or_create_cart(self, customer_id):
        cart, _ = Cart.objects.get_or_create(
            customer_id=customer_id
        )
        return cart

    def get_cart_by_customer(self, customer_id):
        return Cart.objects.filter(customer_id=customer_id).first()

    def get_items(self, cart_id):
        return CartItem.objects.select_related("book").filter(cart_id=cart_id)

    def get_item(self, cart_id, book_id):
        return CartItem.objects.filter(
            cart_id=cart_id,
            book_id=book_id
        ).first()

    def add_item(self, cart_id, book_id, quantity):
        book = Book.objects.get(id=book_id)
        return CartItem.objects.create(
            cart_id=cart_id,
            book=book,
            quantity=quantity
        )

    def update_item(self, cart_item):
        cart_item.save()
        return cart_item
