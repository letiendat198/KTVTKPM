class ViewCartUseCase:
    def __init__(self, cart_repository):
        self.cart_repository = cart_repository

    def execute(self, customer_id):
        cart = self.cart_repository.get_cart_by_customer(customer_id)

        if not cart:
            return {
                "items": [],
                "total_price": 0
            }

        items = self.cart_repository.get_items(cart.id)

        total_price = sum(
            item.book.price * item.quantity
            for item in items
        )

        return {
            "items": items,
            "total_price": total_price
        }
