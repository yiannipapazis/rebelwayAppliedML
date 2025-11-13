import pytest
from library.library import Library
from library.book import Book


@pytest.fixture
def library():
    database = "./tests/test_database.json"
    return Library("Test Library", database)


def test_add_book(library):
    book = Book(name="Test Book", author="Test Author", type="Test Type", pages=10)
    item = library.add_book(book, 5)
    assert library.inventory[item.id]

def test_create_account(library):
    john = library.create_account(name="John Smith", email="john.smith@gmail.com")
    assert john.name == "John Smith"
    assert john.email == "john.smith@gmail.com"

def test_borrow_book(library):
    book = Book(name="Harry Potter", author="J.K. Rowling", type="Fantasy", pages=300)
    item = library.add_book(book, 3)
    item.quantity = 3
    jane = library.create_account(name="Jane Doe", email="jane.doe@gmail.com")
    jane.borrow_book("Harry Potter", library)
    assert jane.books_borrowed_ids[0] == item.id
    assert item.quantity == 2
    jane.return_book("Harry Potter", library)
    assert item.quantity == 3

def test_search_book(library):
    book = Book(name="Dune", author="Frank Herbert", type="Science Fiction", pages=400)
    library.add_book(book, 1)
    assert library.find_item("Dune")



