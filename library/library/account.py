import json
from dataclasses import asdict, dataclass, field
from library.random_number_utils import RandomUtils
from library.book import Book
from library.file__io import Fstream
from typing import TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from library.library import Library


@dataclass
class Account:
    name: str
    email: str
    account_id: str = field(default_factory=RandomUtils.generate_random_id)
    books_borrowed_ids: list[str] = field(default_factory=list)
    
    def borrow_book(self, book_name: str, library: "Library"):
        """
        Borrows a book from the library by storing its ID.

        Args:
            book (Book): The book to be added to the account.
        
        """
        self.print_head(f"{self.name} is attempting to borrow '{book_name}'...")
        item_to_borrow = library.find_item(book_name, verbose=False)

        if not item_to_borrow:
            print(f"Sorry, the book '{book_name}' could not be found in the library.")
            return
        
        if library.lend_item(item_to_borrow.id):
            self.books_borrowed_ids.append(item_to_borrow.id)
            print(f"Successfully borrowed '{item_to_borrow.book.name}'.")
            library.save_library(verbose=False)
        else:
            print(f"Sorry, '{item_to_borrow.book.name}' is currently out of stock.")
    
    @staticmethod
    def print_head(str: str):
        print("-----------------------------------------------------")
        print(str)
        print("-----------------------------------------------------")

    def show_borrowed_books(self, library: "Library"):
        """Displays the details of all books currently borrowed by the account."""
        self.print_head(f"Books borrowed by {self.name}:")
        if not self.books_borrowed_ids:
            print("No books currently borrowed.")
            return
        
        for book_id in self.books_borrowed_ids:
            item = library.inventory.get(book_id)
            if item:
                print(f"- {item.book.name} by {item.book.author}")

    def return_book(self, book_name: str, library: "Library"):
        """Returns a book to the library."""
        self.print_head(f"{self.name} is attempting to return '{book_name}'...")

        item_to_return = library.find_item(book_name, verbose=False)
        if not item_to_return:
            print(f"Cannot process return: '{book_name}' is not a valid library book.")
            return

        # Check if the user has actually borrowed this books
        if item_to_return.id in self.books_borrowed_ids:
            self.books_borrowed_ids.remove(item_to_return.id)
            library.receive_item(item_to_return.id)
            print(f"Successfully returned '{item_to_return.book.name}'.")
        else:
            print(f"Return failed: You have not borrowed '{item_to_return.book.name}'.")

    def return_all_books(self):
        """
        Remove all books from the account.
        """
        pass
