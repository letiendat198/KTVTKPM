from bookstore.interfaces.repositories.customer_repository import CustomerRepository
from ..orm.models import Customer


class DjangoCustomerRepository(CustomerRepository):

    def create(self, username, password, phone_number, dob):
        return Customer.objects.create(
            username=username,
            password=password,
            phone_number=phone_number,
            dob=dob
        )

    def exists(self, username):
        return Customer.objects.filter(username=username).exists()

    def get_by_credentials(self, username, password):
        try:
            return Customer.objects.get(
                username=username,
                password=password
            )
        except Customer.DoesNotExist:
            return None

    def get_by_id(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None
