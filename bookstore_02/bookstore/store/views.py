from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .dao import CartDAO, CustomerDAO, OrderDAO, BookDAO, RatingDAO
from .models import Cart, CartItem, Customer, Book
import uuid


# =========================
# AUTH
# =========================
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        customer = CustomerDAO.register(
            customer_id=str(uuid.uuid4()),
            name=request.POST["name"],
            email=request.POST["email"],
            password=request.POST["password"]
        )
        request.session["customer_id"] = customer.id
        request.session["customer_name"] = customer.name
        return redirect("book_list")

    return render(request, "shop/register.html")


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        try:
            customer = Customer.objects.get(
                email=request.POST["email"],
                password=request.POST["password"]
            )
            request.session["customer_id"] = customer.id
            request.session["customer_name"] = customer.name
            return redirect("book_list")
        except Customer.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, "shop/login.html")


def logout(request):
    request.session.flush()
    return redirect("login")


# =========================
# BOOK – VIEW + ADD TO CART
# =========================

def recommend_books(book_id, limit=4):
    # Các cart item chứa book hiện tại
    related_items = CartItem.objects.filter(book_id=book_id)

    # Các cart liên quan
    cart_ids = related_items.values_list("cart_id", flat=True)

    # Các item khác trong những cart đó
    items = CartItem.objects.filter(cart_id__in=cart_ids)

    # Các book khác (trừ book đang xem)
    books = Book.objects.filter(
        id__in=items.values_list("book_id", flat=True)
    ).exclude(id=book_id).distinct()[:limit]

    return books

def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # ==========================
    # RECOMMENDATION
    # ==========================
    recommended_books = []

    customer_id = request.session.get("customer_id")
    if customer_id:
        cart = Cart.objects.filter(customer_id=customer_id).first()
        if cart:
            first_item = CartItem.objects.filter(cart=cart).first()
            if first_item:
                recommended_books = recommend_books(first_item.book_id)

    return render(request, "shop/book_list.html", {
        "books": books,
        "query": query,
        "recommended_books": recommended_books
    })


@require_http_methods(["POST"])
def add_book_to_cart(request, book_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    quantity = int(request.POST.get("quantity", 1))

    CartDAO.add_to_cart(
        customer_id=customer_id,
        book_id=book_id,
        quantity=quantity
    )

    messages.success(request, "Book added to cart")
    return redirect("book_list")


# =========================
# CART
# =========================
def view_cart(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    cart = CustomerDAO.view_cart(customer_id)
    items = cart.items.all() if cart else []

    return render(request, "shop/cart.html", {"items": items})


# =========================
# BOOK (ADMIN)
# =========================
@require_http_methods(["GET", "POST"])
def update_book(request):
    if request.method == "POST":
        BookDAO.update_book(
            book_id=request.POST["book_id"],
            stock=int(request.POST["stock"]),
            price=float(request.POST["price"])
        )
        messages.success(request, "Book updated successfully")

    return render(request, "shop/update_book.html")

@require_http_methods(["POST"])
def rate_book(request, book_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)
    book = Book.objects.get(id=book_id)

    RatingDAO.rate_book(
        customer=customer,
        book=book,
        score=int(request.POST["score"])
    )

    return redirect("book_list")

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Shipping, Payment, Customer
from .dao import OrderDAO


@require_http_methods(["GET", "POST"])
def checkout(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)

    if request.method == "POST":
        shipping_id = request.POST["shipping"]
        payment_id = request.POST["payment"]

        shipping = Shipping.objects.get(id=shipping_id)
        payment = Payment.objects.get(id=payment_id)

        order = OrderDAO.checkout(
            customer=customer,
            shipping=shipping,
            payment=payment
        )

        if not order:
            messages.error(request, "Cart is empty")
            return redirect("view_cart")

        return redirect("order_success", order_id=order.id)

    shippings = Shipping.objects.all()
    payments = Payment.objects.all()

    return render(
        request,
        "shop/checkout.html",
        {
            "shippings": shippings,
            "payments": payments
        }
    )

def order_success(request, order_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    from .models import Order
    order = Order.objects.get(id=order_id)

    return render(request, "shop/order_success.html", {"order": order})

def staff_required(request):
    staff_id = request.session.get("staff_id")
    return staff_id is not None

from .dao import InventoryDAO
from .models import Staff, Book, Category
from django.contrib import messages


@require_http_methods(["GET", "POST"])
def staff_import_book(request):
    if not staff_required(request):
        return redirect("staff_login")

    if request.method == "POST":
        # Nhập sách mới
        if request.POST.get("type") == "new":
            InventoryDAO.add_new_book(
                title=request.POST["title"],
                author=request.POST["author"],
                price=float(request.POST["price"]),
                stock=int(request.POST["stock"]),
                category_id=request.POST["category"]
            )
            messages.success(request, "New book added successfully")

        # Nhập thêm số lượng
        else:
            InventoryDAO.import_stock(
                book_id=request.POST["book_id"],
                quantity=int(request.POST["quantity"])
            )
            messages.success(request, "Stock updated successfully")

        return redirect("staff_import_book")

    books = Book.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        "shop/staff_import_book.html",
        {
            "books": books,
            "categories": categories
        }
    )

# =========================
# STAFF AUTH
# =========================
@require_http_methods(["GET", "POST"])
@require_http_methods(["GET", "POST"])
def staff_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            staff = Staff.objects.get(
                username=username,
                password=password
            )

            request.session["staff_id"] = staff.id
            request.session["staff_name"] = staff.name
            request.session["staff_role"] = staff.role

            return redirect("staff_import_book")

        except Staff.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, "shop/staff_login.html")


def staff_logout(request):
    request.session.pop("staff_id", None)
    request.session.pop("staff_name", None)
    request.session.pop("staff_role", None)
    return redirect("staff_login")

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book, Rating


def rate_book(request, book_id):
    # 1. Check login
    customer_id = request.session.get("customer_id")
    if not customer_id:
        messages.error(request, "Please login to rate books")
        return redirect("login")

    book = get_object_or_404(Book, id=book_id)

    # 2. Lấy rating cũ nếu có
    rating = Rating.objects.filter(
        customer_id=customer_id,
        book=book
    ).first()

    if request.method == "POST":
        score = int(request.POST["score"])

        if score < 1 or score > 5:
            messages.error(request, "Score must be between 1 and 5")
            return redirect("rate_book", book_id=book.id)

        if rating:
            rating.score = score
            rating.save()
            messages.success(request, "Rating updated")
        else:
            Rating.objects.create(
                customer_id=customer_id,
                book=book,
                score=score
            )
            messages.success(request, "Rating submitted")

        return redirect("book_detail", book_id=book.id)

    return render(request, "shop/rate_book.html", {
        "book": book,
        "rating": rating
    })

from django.db.models import Avg

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    avg_rating = Rating.objects.filter(book=book).aggregate(
        Avg("score")
    )["score__avg"]

    user_rating = None
    customer_id = request.session.get("customer_id")
    if customer_id:
        user_rating = Rating.objects.filter(
            customer_id=customer_id,
            book=book
        ).first()

    return render(request, "shop/book_detail.html", {
        "book": book,
        "avg_rating": avg_rating,
        "user_rating": user_rating
    })


