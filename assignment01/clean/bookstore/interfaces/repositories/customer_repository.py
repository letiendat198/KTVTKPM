from abc import ABC, abstractmethod


class CustomerRepository(ABC):

    @abstractmethod
    def create(self, username, password, phone_number, dob):
        """Create and return a new customer"""
        pass

    @abstractmethod
    def exists(self, username):
        """Check if a username already exists"""
        pass

    @abstractmethod
    def get_by_credentials(self, username, password):
        """Return customer if credentials are valid, else None"""
        pass

    @abstractmethod
    def get_by_id(self, customer_id):
        """Return customer by ID"""
        pass
