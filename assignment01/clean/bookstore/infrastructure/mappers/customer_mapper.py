from domain.entities.customer import Customer as DomainCustomer

def orm_to_domain_customer(orm_customer):
    return DomainCustomer(
        id=orm_customer.id,
        username=orm_customer.username,
        phone_number=orm_customer.phone_number,
        dob=orm_customer.dob
    )
