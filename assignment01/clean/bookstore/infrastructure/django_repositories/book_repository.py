from bookstore.interfaces.repositories.book_repository import BookRepository
from ..orm.models import Book


class DjangoBookRepository(BookRepository):

    def get_all(self):
        return Book.objects.all()

    def get_by_id(self, book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None
