from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Customer, Book, Cart, CartItem
from django.utils import timezone

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        phone_number = request.POST["phone_number"]
        dob = request.POST["dob"]

        Customer.objects.create(
            username=username,
            password=password,
            phone_number=phone_number,
            dob=dob
        )
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            customer = Customer.objects.get(username=username, password=password)
            request.session["customer_id"] = customer.id
            return redirect("book_list")
        except Customer.DoesNotExist:
            return HttpResponse("Invalid username or password")

    return render(request, "login.html")

def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})

def add_to_cart(request, book_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)
    book = get_object_or_404(Book, id=book_id)

    cart, created = Cart.objects.get_or_create(
        customer=customer,
        defaults={"created_at": timezone.now()}
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")

def view_cart(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)
    cart = Cart.objects.filter(customer=customer).first()

    items = []
    total_price = 0

    if cart:
        items = cart.items.select_related("book")
        total_price = sum(item.book.price * item.quantity for item in items)

    context = {
        "items": items,
        "total_price": total_price
    }

    return render(request, "cart.html", context)