class RegisterCustomerUseCase:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def execute(self, username, password, phone_number, dob):
        if self.customer_repository.exists(username):
            raise ValueError("Username already exists")

        customer = self.customer_repository.create(
            username=username,
            password=password,
            phone_number=phone_number,
            dob=dob
        )

        return customer
