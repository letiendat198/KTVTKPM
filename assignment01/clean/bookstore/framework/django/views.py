from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict

from bookstore.infrastructure.django_repositories.customer_repository import DjangoCustomerRepository
from bookstore.infrastructure.django_repositories.book_repository import DjangoBookRepository
from bookstore.infrastructure.django_repositories.cart_repository import DjangoCartRepository

from bookstore.usecases.register_customer import RegisterCustomerUseCase
from bookstore.usecases.login_customer import LoginCustomerUseCase
from bookstore.usecases.view_books import ViewBookCatalogUseCase
from bookstore.usecases.add_to_cart import AddToCartUseCase
from bookstore.usecases.view_cart import ViewCartUseCase

def register(request):
    if request.method == "POST":
        repo = DjangoCustomerRepository()
        usecase = RegisterCustomerUseCase(repo)

        try:
            usecase.execute(
                username=request.POST["username"],
                password=request.POST["password"],
                phone_number=request.POST["phone_number"],
                dob=request.POST["dob"]
            )
            return redirect("login")
        except ValueError as e:
            return HttpResponse(str(e))

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        repo = DjangoCustomerRepository()
        usecase = LoginCustomerUseCase(repo)

        customer = usecase.execute(
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if not customer:
            return HttpResponse("Invalid credentials")

        request.session["customer_id"] = customer.id
        return redirect("book_list")

    return render(request, "login.html")

def book_list(request):
    repo = DjangoBookRepository()
    usecase = ViewBookCatalogUseCase(repo)

    books = usecase.execute()
    return render(request, "book_list.html", {"books": books})

def add_to_cart(request, book_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    cart_repo = DjangoCartRepository()
    book_repo = DjangoBookRepository()

    usecase = AddToCartUseCase(cart_repo, book_repo)
    usecase.execute(customer_id=customer_id, book_id=book_id)

    return redirect("view_cart")

def view_cart(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    repo = DjangoCartRepository()
    usecase = ViewCartUseCase(repo)

    result = usecase.execute(customer_id)
    result_list = []
    for item in result["items"]:
        book_dict = model_to_dict(item.book)
        item_dict = model_to_dict(item)
        print(item_dict)
        item_dict["book"] = book_dict
        item_dict["subtotal"] = item.quantity * item.book.price

        result_list.append(item_dict)

    return render(request, "cart.html", {
        "items": result_list,
        "total_price": result["total_price"]
    })
