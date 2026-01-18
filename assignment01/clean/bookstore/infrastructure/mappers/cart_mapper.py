from domain.entities.cart import Cart as DomainCart, CartItem as DomainCartItem
from infrastructure.mappers.book_mapper import orm_to_domain_book

def orm_to_domain_cart(orm_cart):
    items = []

    for item in orm_cart.items.select_related("book").all():
        domain_book = orm_to_domain_book(item.book)
        items.append(
            DomainCartItem(
                book=domain_book,
                quantity=item.quantity
            )
        )

    return DomainCart(
        id=orm_cart.id,
        customer_id=orm_cart.customer_id,
        items=items
    )

