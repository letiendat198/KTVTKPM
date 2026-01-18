import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse

CUSTOMER_SERVICE = "http://localhost:8001"
BOOK_SERVICE = "http://localhost:8002"
CART_SERVICE = "http://localhost:8003"


def register(request):
    if request.method == "POST":
        response = requests.post(
            f"{CUSTOMER_SERVICE}/register/",
            json={
                "username": request.POST["username"],
                "password": request.POST["password"],
                "phone_number": request.POST["phone_number"],
                "dob": request.POST["dob"]
            }
        )

        if response.status_code == 201:
            return redirect("login")
        return HttpResponse("Registration failed")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        response = requests.post(
            f"{CUSTOMER_SERVICE}/login/",
            json={
                "username": request.POST["username"],
                "password": request.POST["password"]
            }
        )

        if response.status_code == 200:
            request.session["customer_id"] = response.json()["customer_id"]
            return redirect("books")

        return HttpResponse("Invalid credentials")

    return render(request, "login.html")


def books(request):
    response = requests.get(f"{BOOK_SERVICE}/books/all")
    books = None
    if response:
        books = response.json()
    return render(request, "book_list.html", {"books": books})


def add_to_cart(request, book_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    requests.post(
        f"{CART_SERVICE}/cart/add/",
        json={
            "customer_id": customer_id,
            "book_id": book_id
        }
    )

    return redirect("cart")


def cart(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    response = requests.get(f"{CART_SERVICE}/cart/{customer_id}/")
    cart_data = None
    if response:
        cart_data = response.json()
        print(cart_data)
        books = []
        for item in cart_data["items"]:
            response = requests.get(f"{BOOK_SERVICE}/books/{item['book_id']}")
            book_data = None
            if response:
                book_data = response.json()
                books.append({
                    "book": book_data["book"],
                    "quantity": item["cart"],
                    "subtotal": int(item["cart"]) * int(book_data["book"]["price"])
                })

        cart_data = {
            "items": books,
            "total_price": sum([int(i["subtotal"]) for i in books])
        }

    print(cart_data)
    return render(request, "cart.html", cart_data)
