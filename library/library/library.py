import json
import os
from dataclasses import asdict, dataclass, field
from library.file__io import Fstream
from library.book import Book
from library.account import Account
from library.random_number_utils import RandomUtils

@dataclass
class LibraryItem:
    """Represents a book and its quantity in the library."""
    book: Book
    quantity: int
    id: str = field(default_factory=RandomUtils.generate_random_id)

@dataclass
class Library:
    name: str
    database_path:str
    inventory: dict[str, LibraryItem] = field(init=False, default_factory=dict)
    accounts: dict[str, Account] = field(init=False, default_factory=dict)

    def __post_init__(self):
        """
        Loads books from the database file after the instance is created.
        """
        print("Initializing library and loading books...")
        all_data = Fstream.load_json_files(self.database_path)

        # Load Books and Quantities into Inventory
        books_data = all_data.get("Books", {})
        quantities_data = all_data.get("Quantities", {})
        for book_id, book_data in books_data.items():
            quantity = quantities_data.get(book_id, 0)
            if quantity > 0:
                self.inventory[book_id] = LibraryItem(id=book_id, book=Book(**book_data), quantity=quantity)

        # Load Accounts
        accounts_data = all_data.get("Accounts", {})
        for account_id, account_data in accounts_data.items():
            self.accounts[account_id] = Account(account_id=account_id, **account_data)

        print(f"Library initialized with {len(self.inventory)} unique book titles and {len(self.accounts)} accounts.")
    
    def add_book(self, book: Book, quantity: int):
        existing_item = self.find_item(book.search_string, verbose=False)
        if not existing_item:
            new_item = LibraryItem(book=book, quantity=quantity)
            self.inventory[new_item.id] = new_item
            self.save_library()
            print(f"Added {book.name} to the library with quantity {quantity}.")
            return new_item
        else:
            print(f"{book.name} is already in the library. Adding quantity of {quantity} to existing book.")
            self.inventory[existing_item.id].quantity += quantity
            print(f"Updated quantity of {book.name} to {self.inventory[existing_item.id].quantity}.")
            self.save_library()
            return existing_item

    def create_account(self, name: str, email: str) -> Account:
        """Creates a new account, saves it, and adds it to the library's accounts."""
        # Check if an account with this email already exists
        for acc in self.accounts.values():
            if acc.email == email:
                print(f"An account with email {email} already exists.")
                return acc
        
        new_account = Account(name=name, email=email)
        self.accounts[new_account.account_id] = new_account
        self.save_library()
        print(f"Created account for {name}.")
        return new_account

    @staticmethod
    def print_head(str: str):
        print("-----------------------------------------------------")
        print(str)
        print("-----------------------------------------------------")
    
    def remove_book(self, book_id: str):
        if book_id in self.inventory:
            del self.inventory[book_id]
            self.save_library()
            print(f"Removed book with ID {book_id} from the library.")
    
    def find_item(self, query: str, verbose: bool = True):
        """
        Finds a book in the inventory by a search query.
        """
        for item in self.inventory.values():
            if query.lower() in item.book.search_string.lower():
                if verbose:
                    print(f"Found book: {item.book.name}")
                return item
        return None

    def get_total_books(self)->int:
        """
        Returns the total number of books in the library.
        """
        total = sum(item.quantity for item in self.inventory.values()) 
        self.print_head(f"Total number of books: {total}")
        return total

    def save_library(self, verbose: bool = True):
        """
        Saves the current library inventory to the database file.
        """
        all_data = Fstream.load_json_files(self.database_path)
        all_data["Books"] = {item.id: asdict(item.book) for item in self.inventory.values()}
        all_data["Quantities"] = {item.id: item.quantity for item in self.inventory.values()}
        all_data["Accounts"] = {}
        for account_id, account in self.accounts.items():
            all_data["Accounts"][account_id] = {key: value for key, value in asdict(account).items() if key != "account_id"}
        
        with open(self.database_path, 'w') as file:
            json.dump(all_data, file, indent=4)
        if verbose:
            self.print_head(f"{self.name}\nLibrary saved with {len(self.inventory)} unique book titles.")

    def lend_item(self, item_id: str) -> bool:
        """
        Lends an item if available. Returns True on success, False on failure.
        This method only handles the inventory count.
        """
        item = self.inventory.get(item_id)
        if item and item.quantity > 0:
            item.quantity -= 1
            self.save_library(verbose=False)
            return True
        return False

    def receive_item(self, item_id: str):
        """
        Receives an item back into the library, incrementing its quantity.
        """
        if item_id in self.inventory:
            self.inventory[item_id].quantity += 1
            self.save_library(verbose=False)