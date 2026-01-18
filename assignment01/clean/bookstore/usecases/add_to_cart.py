class AddToCartUseCase:
    def __init__(self, cart_repository, book_repository):
        self.cart_repository = cart_repository
        self.book_repository = book_repository

    def execute(self, customer_id, book_id):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")

        cart = self.cart_repository.get_or_create_cart(customer_id)

        cart_item = self.cart_repository.get_item(cart.id, book_id)

        if cart_item:
            cart_item.quantity += 1
            self.cart_repository.update_item(cart_item)
        else:
            self.cart_repository.add_item(
                cart_id=cart.id,
                book_id=book_id,
                quantity=1
            )

        return cart
