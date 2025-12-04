#Name:Trigya Yogi
#Date:3 December 2025
CATALOG_FILE = "simple_catalog.txt"

def load_books():
    """Loads book data from the file into a list of dictionaries."""
    books = []
    try:
        with open(CATALOG_FILE, 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) == 4:
                    books.append({
                        'isbn': data[0],
                        'title': data[1],
                        'author': data[2],
                        'status': data[3]
                    })
        print(f"Loaded {len(books)} books.")
    except FileNotFoundError:
        print("Catalog file not found. Starting fresh.")
    return books

def save_books(books):
    try:
        with open(CATALOG_FILE, 'w') as f:
            for book in books:
                line = f"{book['isbn']},{book['title']},{book['author']},{book['status']}\n"
                f.write(line)
        print(f"Saved {len(books)} books.")
    except Exception as e:
        print(f"Error saving file: {e}")

def get_user_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")

def find_book(books, isbn):
    for book in books:
        if book['isbn'] == isbn:
            return book
    return None

def add_book(books):
    print("\n--- Add New Book ---")
    isbn = get_user_input("Enter ISBN: ")
    title = get_user_input("Enter Title: ")
    author = get_user_input("Enter Author: ")

    if find_book(books, isbn):
        print(f"Error: Book with ISBN {isbn} already exists.")
        return

    new_book = {
        'isbn': isbn,
        'title': title,
        'author': author,
        'status': 'Available'
    }
    books.append(new_book)
    print(f"Added: {title}")
    save_books(books)

def update_status(books, new_status):
    print(f"\n--- {new_status} Book ---")
    isbn = get_user_input("Enter ISBN: ")
    book = find_book(books, isbn)
    
    if book:
        if book['status'] != new_status:
            book['status'] = new_status
            print(f"Status updated for {book['title']}: {new_status}")
            save_books(books)
        else:
            print(f"Book is already set to {new_status}.")
    else:
        print(f"Error: Book {isbn} not found.")

def search_catalog(books):
    print("\n--- Search Catalog ---")
    query = get_user_input("Enter search query: ").lower()
    
    results = [b for b in books if 
               query in b['isbn'].lower() or
               query in b['title'].lower() or
               query in b['author'].lower()]
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        for b in results:
            print(f"ISBN: {b['isbn']} | Title: {b['title']} | Author: {b['author']} | Status: {b['status']}")
    else:
        print("No matches found.")

def display_all(books):
    if not books:
        print("\nThe library catalog is empty.")
        return

    print("\n=== Library Catalog ===")
    for b in books:
        print(f"ISBN: {b['isbn']} | Title: {b['title']} | Status: {b['status']}")
    print("=========================")

def main():
    books = load_books() 

    while True:
        print("\n--- Library Menu ---")
        print("1. Add New Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Search Catalog")
        print("5. Display All Books")
        print("6. Exit and Save")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_book(books)
        
        elif choice == '2':
            update_status(books, 'Issued')
        
        elif choice == '3':
            update_status(books, 'Available')
        
        elif choice == '4':
            search_catalog(books)
        
        elif choice == '5':
            display_all(books)
        
        elif choice == '6':
            print("\nExiting. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
