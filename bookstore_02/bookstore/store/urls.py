from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.login, name="login"),
    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),
    path("logout/", views.logout, name="logout"),

    path("books/", views.book_list, name="book_list"),
    path("books/add/<int:book_id>/", views.add_book_to_cart, name="add_book_to_cart"),

    path("cart/", views.view_cart, name="view_cart"),

    path("book/update/", views.update_book, name="update_book"),
    path("books/rate/<int:book_id>/", views.rate_book, name="rate_book"),

    path("checkout/", views.checkout, name="checkout"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),
    path("staff/import/", views.staff_import_book, name="staff_import_book"),
    path("books/<int:book_id>/rate/", views.rate_book, name="rate_book"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
]
