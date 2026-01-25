from django.db import models


# =====================
# CUSTOMER
# =====================
class Address(models.Model):
    num = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.num}, {self.street}, {self.city}"


class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


# =====================
# BOOK
# =====================
class Category(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.FloatField()

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title


# =====================
# ORDER
# =====================
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.customer.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

class Staff(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    username = models.CharField(max_length=50, unique=True, default="")
    password = models.CharField(max_length=128, default="")

    def __str__(self):
        return f"{self.name} ({self.role})"

class Rating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ("customer", "book")

    def __str__(self):
        return f"{self.book.title} - {self.score}/5"

class Shipping(models.Model):
    method_name = models.CharField(max_length=50)
    fee = models.FloatField()

    def __str__(self):
        return f"{self.method_name} ({self.fee})"


class Payment(models.Model):
    method_name = models.CharField(max_length=50)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.method_name} - {self.status}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    shipping = models.ForeignKey(
        Shipping, on_delete=models.SET_NULL, null=True
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"
