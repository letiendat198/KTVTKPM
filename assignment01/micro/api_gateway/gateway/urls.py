from django.urls import path
from .views import register, login_view, books, add_to_cart, cart

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register, name="register"),
    path("books/", books, name="books"),
    path("add-to-cart/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
]
