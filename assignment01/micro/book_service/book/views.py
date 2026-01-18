from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(["GET"])
def list_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_book(request, book_id):
    book = Book.objects.filter(id = book_id).first()
    if not book:
        return Response({"book": {}})
    
    serializer = BookSerializer(book)
    return Response({"book": serializer.data})