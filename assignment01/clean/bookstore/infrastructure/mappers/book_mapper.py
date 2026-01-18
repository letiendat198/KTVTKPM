from domain.entities.book import Book as DomainBook

def orm_to_domain_book(orm_book):
    return DomainBook(
        id=orm_book.id,
        title=orm_book.title,
        author=orm_book.author,
        price=orm_book.price,
        stock=orm_book.stock
    )
