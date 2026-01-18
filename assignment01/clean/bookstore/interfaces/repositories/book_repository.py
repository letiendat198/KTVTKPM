from abc import ABC, abstractmethod


class BookRepository(ABC):

    @abstractmethod
    def get_all(self):
        """Return list of all books"""
        pass

    @abstractmethod
    def get_by_id(self, book_id):
        """Return a single book by ID"""
        pass
