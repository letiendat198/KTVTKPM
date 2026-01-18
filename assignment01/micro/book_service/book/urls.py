from django.urls import path
from .views import list_books, get_book

urlpatterns = [
    path("all/", list_books),
    path("<int:book_id>/", get_book)
]
