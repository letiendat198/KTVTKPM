class LoginCustomerUseCase:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def execute(self, username, password):
        customer = self.customer_repository.get_by_credentials(
            username=username,
            password=password
        )

        if not customer:
            raise ValueError("Invalid username or password")

        return customer
