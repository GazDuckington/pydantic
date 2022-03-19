from typing import Optional, List
import pydantic

class ISBNMissingError(Exception):
    """Custom error for missing ISBN digits."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)

class ISBN10FormatError(Exception):
    """Custom error for ISBN 10 Format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)
        
class Author(pydantic.BaseModel):
    name: str
    verified: bool

class Book(pydantic.BaseModel):
    title: str
    author: str
    author2: Optional[Author]
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn10_or_isbn13(cls, values):
        """Check if either or both isbn10 or isbn13 exists."""
        if "isbn_10" not in values and "isbn_13" not in values:
            raise ISBNMissingError(
                    title=values["title"],
                    message="Document should have either ISBN10 or ISBN13"
                )
        return values

    @pydantic.validator("isbn_10")
    @classmethod
    def isbn_10_valid(cls, value):
        """Validation for ISBN 10 Number."""

        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(value=value, message="ISBN10 should be 10 digits.")
        
        def char_to_int(char: str) -> int:
            return 10 if char in "Xx" else int(char)

        weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(value=value, message="ISBN10 digit sum should be divisible by 11.")
        return value

    class Config:
        """Pydantic configurations."""
        allow_mutation = False
        anystr_lower = True

dummy_data = [
    {
    "title": "Zero to One",
    "subtitle": "Notes on Startups, or How to Build the Future",
    "author": "Peter Thiel",
    "publisher": "Ballantine Books",
    "isbn_10": "0753555190",
    "isbn_13": "978-0753555194",
    "price": 14.29,
    "author2": {
      "name": "Peter Thiel",
      "verified": True
    }
  },
  {
    "title": "The Lean Startup",
    "subtitle": "How Relentless Change Creates Radically Successful Businesses",
    "author": "Eric Ries",
    "publisher": "Penguin UK",    
    "isbn_10": "0670921602",
    "isbn_13": "978-0670921607",
    "price": 12.96
  },
  {
    "title": "A Promised Land",
    "author": "Barack Obama",
    "publisher": "Viking UK",
    "isbn_10": "0241491517",
    "isbn_13": "978-0241491515",
    "price": 31.74
  },
  {
    "title": "The Hard Thing about Hard Things",
    "subtitle": "Building a Business When There Are No Easy Answers",
    "author": "Ben Horowitz",
    "publisher": "HarperBusiness",
    "isbn_10": "0062273205",
    "isbn_13": "978-0062273208",
    "price": 15.55
  },
  {
    "title": "Design patterns",
    "subtitle": "Elements of reusable object-oriented software",
    "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
    "publisher": "Addison Wesley",
    "isbn_10": "0201633612",
    "isbn_13": "978-0201633610",
    "price": 50
  },
  {
    "title": "Clean Code",
    "subtitle": "A Handbook of Agile Software Craftsmanship",
    "author": "Robert Martin",
    "publisher": "Financial Times Prentice Hall",
    "isbn_10": "0132350882",
    "isbn_13": "978-0132350884",
    "price": 33.43
  }
]

def main() -> None:
    """Main Function"""

    # read dummy data as keyword arguments (**kwargs)
    books: List[Book] = [Book(**items) for items in dummy_data]
    print(books[0])

if __name__ == "__main__":
    main()