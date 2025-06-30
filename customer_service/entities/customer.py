
"""Customer entity module."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class Address(BaseModel):
    """
    Represents a customer's address.
    """

    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    """
    Represents a product in a customer's purchase history.
    """

    product_id: str
    name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    """
    Represents a customer's purchase.
    """

    date: str
    items: List[Product]
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class CommunicationPreferences(BaseModel):
    """
    Represents a customer's communication preferences.
    """

    email: bool = True
    sms: bool = True
    push_notifications: bool = True
    model_config = ConfigDict(from_attributes=True)


class ReadingProfile(BaseModel):
    """
    Represents a customer's reading profile.
    """

    preferred_genres: List[str]
    reading_level: str
    favorite_authors: List[str]
    reading_goals: str
    interests: List[str]
    model_config = ConfigDict(from_attributes=True)


class Customer(BaseModel):
    """
    Represents a customer.
    """

    account_number: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    email: str
    phone_number: str
    customer_start_date: str
    years_as_customer: int
    billing_address: Address
    purchase_history: List[Purchase]
    loyalty_points: int
    preferred_store: str
    communication_preferences: CommunicationPreferences
    reading_profile: ReadingProfile
    scheduled_appointments: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Converts the Customer object to a JSON string.

        Returns:
            A JSON string representing the Customer object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_customer(current_customer_id: str) -> Optional["Customer"]:
        """
        Retrieves a customer based on their ID.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            The Customer object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy customer.
        return Customer(
            customer_id=current_customer_id,
            account_number="428765091",
            customer_first_name="Alex",
            customer_last_name="Johnson",
            email="alex.johnson@example.com",
            phone_number="+1-702-555-1212",
            customer_start_date="2022-06-10",
            years_as_customer=2,
            billing_address=Address(
                street="123 Main St", city="Anytown", state="CA", zip="12345"
            ),
            purchase_history=[  # Example purchase history
                Purchase(
                    date="2023-03-05",
                    items=[
                        Product(
                            product_id="book-111",
                            name="The Thursday Murder Club by Richard Osman",
                            quantity=1,
                        ),
                        Product(
                            product_id="bookmark-222",
                            name="Leather Bookmark Set",
                            quantity=1,
                        ),
                    ],
                    total_amount=24.98,
                ),
                Purchase(
                    date="2023-07-12",
                    items=[
                        Product(
                            product_id="book-333",
                            name="Educated by Tara Westover",
                            quantity=1,
                        ),
                        Product(
                            product_id="book-444",
                            name="The Seven Husbands of Evelyn Hugo",
                            quantity=1,
                        ),
                    ],
                    total_amount=32.5,
                ),
                Purchase(
                    date="2024-01-20",
                    items=[
                        Product(
                            product_id="book-555",
                            name="Project Hail Mary by Andy Weir",
                            quantity=1,
                        ),
                        Product(
                            product_id="lamp-666",
                            name="LED Reading Lamp",
                            quantity=1,
                        ),
                    ],
                    total_amount=45.25,
                ),
            ],
            loyalty_points=133,
            preferred_store="Downtown Library & Bookstore",
            communication_preferences=CommunicationPreferences(
                email=True, sms=False, push_notifications=True
            ),
            reading_profile=ReadingProfile(
                preferred_genres=["mystery", "memoir", "science fiction"],
                reading_level="advanced",
                favorite_authors=["Richard Osman", "Tara Westover", "Andy Weir"],
                reading_goals="Read 24 books this year, explore more diverse authors",
                interests=["book clubs", "author events", "reading challenges"],
            ),
            scheduled_appointments={},
        )
