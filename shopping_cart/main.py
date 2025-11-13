from shopping_cart.item import Item
from shopping_cart.cart import Cart

def print_sep():
    print("-----------------------------------------------------")

if __name__ == "__main__":

    # The main databae for the cart to pass to the class
    database = "./database.json"
    my_cart = Cart(database)

    # Search for an item
    print("Searching item...")
    results = my_cart.search_items("apple")
    print_sep()
    
    # Get the total amount of items in the cart
    print("Total items in the current cart:")
    total_item_count = my_cart.get_total_item_count()
    print(f"Total items count: {total_item_count}")
    print_sep()

    # Create an item so it can be added to the cart
    print("Adding item to the cart...")
    milk = Item("Milk","Dairy", 2.99)
    my_cart.add_item_to_cart(milk)
    print_sep()

    onion = Item("Onion","Vegetable", 1.99)
    my_cart.add_item_to_cart(onion)
    print_sep()

    # Get all items
    my_cart.get_all_items(verbose=1)
    print_sep()
    my_cart.remove_items_from_cart_by_query("milk")

    my_cart.get_total_price_of_items()