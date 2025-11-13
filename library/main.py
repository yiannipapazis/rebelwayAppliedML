from library.library import Library
from library.book import Book
import time

database = "./database.json"

library = Library("Grand Central Library", database)

# Create some books
harry_potter = Book(name="Harry Potter", author="J.K. Rowling", type="Fantasy", pages=300)
library.add_book(harry_potter, 10)
time.sleep(1)
lord_of_the_rings = Book(name="The Lord of the Rings", author="J.R.R. Tolkien", type="Fantasy", pages=400)
library.add_book(lord_of_the_rings, 5)
time.sleep(1)
twilight = Book(name="The Twilight Saga", author="Stephenie Meyer", type="Fantasy", pages=250)
library.add_book(twilight, 8)
time.sleep(1)
hunger_games = Book(name="The Hunger Games", author="Suzanne Collins", type="Science Fiction", pages=350)
library.add_book(hunger_games, 12)
time.sleep(1)
dune = Book(name="Dune", author="Frank Herbert", type="Science Fiction", pages=450)
library.add_book(dune, 7)

# Create accounts through the library
john = library.create_account(name="John Smith", email="john.smith@gmail.com")
time.sleep(2)
jane = library.create_account(name="Jane Doe", email="jane.doe@gmail.com")
time.sleep(2)
bob = library.create_account(name="Bob Johnson", email="bob.johnson@gmail.com")
time.sleep(2)
mary = library.create_account(name="Mary Brown", email="mary.brown@gmail.com")

john.borrow_book("Dune", library)
john.show_borrowed_books(library)


mary.borrow_book("The Hunger Games", library)
mary.show_borrowed_books(library)

bob.borrow_book("The Lord of the Rings", library)
bob.show_borrowed_books(library)

john.return_book("Dune", library)
john.show_borrowed_books(library)

mary.return_book("The Hunger Games", library)
mary.show_borrowed_books(library)
