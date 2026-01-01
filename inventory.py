#Goal: Set up a basic inventory management system using Python and SQLite. Project should support CRUD operations, have persistent storage, and a simple command-line interface that has input validation.

#Importing the sqlite3 module to interact with SQLite databases
import sqlite3

# Function to create a connection to the SQLite database, creating one if it doesn't exist
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Function to create the inventory table if it doesn't exist
cursor.execute("""
               CREATE TABLE IF NOT EXISTS inventory 
                (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   quantity INTEGER NOT NULL,
                   price REAL
                )
                """)    
conn.commit()
    
def add_item():
    name = input("Enter item name: ").strip()
    if not name:
        print("Item name cannot be empty. Please try again.")
        return
    
    quantity = input("Enter item quantity: ").strip()
    try:
        quantity = int(quantity)
        if quantity < 0:
            print("Quantity cannot be negative. Please try again.")
            return
    except ValueError:
        print("Invalid quantity. Please enter a valid positive integer.")
        return
    
    price = input("Enter item price (press Enter to leave blank): ").strip()
    if price == "":
        price = None
    else:
        try:
            price = float(price)
            if price < 0:
                print("Price cannot be negative. Please try again.")
                return
        except ValueError:
            print("Invalid price. Please enter a valid positive number.")
            return
    
    try:        
        cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", 
                (name, quantity, price)
        )
        conn.commit()
        print(f"Added '{name}' (Qty: {quantity}, Price: {'N/A' if price is None else f'${price:.2f}'})")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
   
def view_items():
    cursor.execute("SELECT id, name, quantity, price FROM inventory")
    items = cursor.fetchall()

    if not items:
        print("No items in inventory.")
        return

    print("\nInventory Items")
    print("-" * 55)
    print(f"{'ID':<5} {'Name':<20} {'Qty':<10} {'Price':<10}")
    print("-" * 55)

    for item_id, name, quantity, price in items:
        price_display = "N/A" if price is None else f"${price:.2f}"
        print(f"{item_id:<5} {name:<20} {quantity:<10} {price_display:<10}")
        
    print("-" * 55)
    print(f"Total items: {len(items)}")
        
def update_item():
    item_id = input("Enter item ID to update: ").strip()
    if not item_id.isdigit():
        print("Invalid ID.")
        return

    cursor.execute(
        "SELECT name, quantity, price FROM inventory WHERE id = ?",
        (int(item_id),)
    )
    item = cursor.fetchone()

    if not item:
        print("Item not found.")
        return

    current_name, current_quantity, current_price = item
    current_price_display = "N/A" if current_price is None else f"${current_price:.2f}"

    print("\nCurrent values:")
    print(f"Name: {current_name}")
    print(f"Quantity: {current_quantity}")
    print(f"Price: {current_price_display}")

    # --- Name ---
    name = input("Enter new name (press Enter to keep current): ").strip()
    if not name:
        name = current_name

    # --- Quantity ---
    qty_input = input("Enter new quantity (press Enter to keep current): ").strip()
    if qty_input == "":
        quantity = current_quantity
    else:
        try:
            quantity = int(qty_input)
            if quantity < 0:
                print("Quantity cannot be negative.")
                return
        except ValueError:
            print("Invalid quantity.")
            return

    # --- Price ---
    price_input = input(
        "Enter new price (press Enter to keep current, type 'clear' to remove): "
    ).strip()

    if price_input == "":
        price = current_price
    elif price_input.lower() == "clear":
        price = None
    else:
        try:
            price = float(price_input)
            if price < 0:
                print("Price cannot be negative.")
                return
        except ValueError:
            print("Invalid price.")
            return

    try:
        cursor.execute(
            "UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?",
            (name, quantity, price, int(item_id))
        )
        conn.commit()

        updated_price_display = "N/A" if price is None else f"${price:.2f}"
        print("\nItem updated successfully.")
        print(f"Updated to → Name: {name}, Qty: {quantity}, Price: {updated_price_display}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
def delete_item():
    item_id = input("Enter item ID to delete: ").strip()
    if not item_id.isdigit():
        print("Invalid ID.")
        return

    cursor.execute(
        "SELECT name, quantity, price FROM inventory WHERE id = ?",
        (int(item_id),)
    )
    item = cursor.fetchone()

    if not item:
        print("Item not found.")
        return

    name, quantity, price = item
    price_display = "N/A" if price is None else f"${price:.2f}"

    print("\nItem to be deleted:")
    print(f"Name: {name}")
    print(f"Quantity: {quantity}")
    print(f"Price: {price_display}")

    confirm = input("Are you sure you want to delete this item? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    try:
        cursor.execute(
            "DELETE FROM inventory WHERE id = ?",
            (int(item_id),)
        )
        conn.commit()
        print("Item deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def exit_program():
    print("Exiting the program.")
    conn.close()
    raise SystemExit

def main():
    actions = {
        '1': add_item,
        '2': view_items,
        '3': update_item,
        '4': delete_item,
        '5': exit_program
    }
    
    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")
  
if __name__ == "__main__":
    main()

   
    