import json
from colorama import init, Fore, Style

init(autoreset=True)

class BookCollection:
    def __init__(self):
        self.books = []
        self.storage_file = 'books_data.json'
        self.read_books_from_file()

    def read_books_from_file(self):
        try:
            with open(self.storage_file, 'r') as file:
                self.books = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books_to_file(self):
        with open(self.storage_file, 'w') as file:
            json.dump(self.books, file, indent=4)

    def create_new_book(self):
        print(Fore.CYAN + "\n--- Add New Book ---")
        title = input("Enter the book title: ")
        author = input("Enter the book author: ")
        year = input("Enter the year of publication: ")
        genre = input("Enter the genre of the book: ")
        read_input = input("Have you read this book? (yes/no): ").lower()
        read = True if read_input == 'yes' else False

        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }

        self.books.append(book)
        self.save_books_to_file()
        print(Fore.GREEN + f"Book '{title}' added to the collection.")

    def delete_book(self):
        print(Fore.CYAN + "\n--- Delete Book ---")
        title = input("Enter the title of the book to delete: ")
        for book in self.books:
            if book['title'].lower() == title.lower():
                self.books.remove(book)
                self.save_books_to_file()
                print(Fore.GREEN + f"Book '{title}' removed from the collection.")
                return
        print(Fore.RED + f"Book '{title}' not found in the collection.")

    def search_books(self):
        print(Fore.CYAN + "\n--- Search Books ---")
        print("Search by:\n1. Title\n2. Author\n3. Genre")
        choice = input("Enter your choice (1-3): ")
        search_type = {'1': 'title', '2': 'author', '3': 'genre'}.get(choice)
        if not search_type:
            print(Fore.RED + "Invalid choice.")
            return

        search_text = input(f"Enter the {search_type} to search: ").lower()
        found_books = [book for book in self.books if search_text in book[search_type].lower()]

        if found_books:
            print(Fore.GREEN + "Matching books:")
            for index, book in enumerate(found_books, start=1):
                status = Fore.YELLOW + "Read" if book['read'] else Fore.MAGENTA + "Unread"
                print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            print(Fore.RED + "No matching books found.")

    def update_book(self):
        print(Fore.CYAN + "\n--- Update Book ---")
        title = input("Enter the title of the book to update: ")
        for book in self.books:
            if book['title'].lower() == title.lower():
                print(Fore.YELLOW + "Leave input blank to keep the current value.")
                new_title = input(f"New title (current: {book['title']}): ")
                new_author = input(f"New author (current: {book['author']}): ")
                new_year = input(f"New year (current: {book['year']}): ")
                new_genre = input(f"New genre (current: {book['genre']}): ")
                new_read = input("Have you read this book? (yes/no): ").lower()

                if new_title: book['title'] = new_title
                if new_author: book['author'] = new_author
                if new_year: book['year'] = new_year
                if new_genre: book['genre'] = new_genre
                if new_read in ['yes', 'no']: book['read'] = (new_read == 'yes')

                self.save_books_to_file()
                print(Fore.GREEN + "Book updated successfully.")
                return
        print(Fore.RED + "Book not found.")

    def display_books(self):
        print(Fore.CYAN + "\n--- Book Collection ---")
        if not self.books:
            print(Fore.YELLOW + "No books in the collection.")
            return
        for index, book in enumerate(self.books, start=1):
            status = Fore.GREEN + "Read" if book['read'] else Fore.RED + "Unread"
            print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def show_reading_progress(self):
        print(Fore.CYAN + "\n--- Reading Progress ---")
        total = len(self.books)
        if total == 0:
            print(Fore.YELLOW + "No books in the collection.")
            return
        read_count = sum(1 for book in self.books if book['read'])
        percentage = (read_count / total) * 100
        print(f"Total books: {total}")
        print(Fore.GREEN + f"Books read: {read_count}")
        print(Fore.BLUE + f"Reading progress: {percentage:.2f}%")

    def main_menu(self):
        while True:
            print(Fore.LIGHTBLUE_EX + "\n=== Personal Library Manager ===")
            print("1. Add a new book")
            print("2. Delete a book")
            print("3. Search for books")
            print("4. Update a book")
            print("5. Display all books")
            print("6. Show reading progress")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")
            if choice == '1':
                self.create_new_book()
            elif choice == '2':
                self.delete_book()
            elif choice == '3':
                self.search_books()
            elif choice == '4':
                self.update_book()
            elif choice == '5':
                self.display_books()
            elif choice == '6':
                self.show_reading_progress()
            elif choice == '7':
                self.save_books_to_file()
                print(Fore.CYAN + "Library saved. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    manager = BookCollection()
    manager.main_menu()

