from .models import Category, Customer, Cart, CartItem, Book


# =====================
# CustomerDAO
# =====================
class CustomerDAO:

    @staticmethod
    def register(customer_id, name, email, password):
        return Customer.objects.create(
            id=customer_id,
            name=name,
            email=email,
            password=password
        )

    @staticmethod
    def view_cart(customer_id):
        return Cart.objects.filter(customer_id=customer_id).last()


# =====================
# OrderDAO
# =====================
class CartDAO:

    @staticmethod
    def add_to_cart(customer_id, book_id, quantity):
        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item


# =====================
# BookDAO
# =====================
class BookDAO:

    @staticmethod
    def update_book(book_id, stock, price):
        book = Book.objects.get(id=book_id)
        book.stock = stock
        book.price = price
        book.save()
        return book

from .models import Order, OrderItem, Shipping, Payment, Cart

class OrderDAO:

    @staticmethod
    def checkout(customer, shipping, payment):
        cart = Cart.objects.filter(customer=customer).last()
        if not cart:
            return None

        total = 0
        order = Order.objects.create(
            customer=customer,
            total_price=0,
            shipping=shipping,
            payment=payment
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            total += item.quantity * item.book.price

        order.total_price = total + shipping.fee
        order.save()

        cart.delete()
        return order

from .models import Rating

class RatingDAO:

    @staticmethod
    def rate_book(customer, book, score):
        rating, _ = Rating.objects.update_or_create(
            customer=customer,
            book=book,
            defaults={"score": score}
        )
        return rating

class InventoryDAO:

    @staticmethod
    def add_new_book(title, author, price, stock, category_id):
        category = Category.objects.get(id=category_id)
        return Book.objects.create(
            title=title,
            author=author,
            price=price,
            stock=stock,
            category=category
        )

    @staticmethod
    def import_stock(book_id, quantity):
        book = Book.objects.get(id=book_id)
        book.stock += quantity
        book.save()
        return book