import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer

BOOK_SERVICE_URL = "http://localhost:8002/books/"

@api_view(["POST"])
def add_to_cart(request):
    customer_id = request.data["customer_id"]
    book_id = request.data["book_id"]

    cart, _ = Cart.objects.get_or_create(customer_id=customer_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id
    )
    if not created:
        item.quantity += 1
        item.save()

    return Response({"message": "Added to cart"})

@api_view(["GET"])
def view_cart(request, customer_id):
    cart = Cart.objects.filter(customer_id=customer_id).first()
    if not cart:
        return Response({"items": []})

    serializer = CartSerializer(cart)
    return Response(serializer.data)
