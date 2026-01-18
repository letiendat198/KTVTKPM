from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.login_view, name="login"),
    path("books/", views.book_list, name="book_list"),
    path("add-to-cart/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
]
