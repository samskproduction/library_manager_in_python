import streamlit as st
import json
from collections import Counter

FILE_NAME = "library.json"

def load_library():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.warning("Library file not found, starting with an empty library.")
        return []
    except json.JSONDecodeError:
        st.warning("Error decoding the library file, starting with an empty library.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

def save_library(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"])

if menu == "Add a Book":
    st.subheader("Add a Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if not title or not author:
            st.error("Title and Author are required fields!")
        else:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
            library.append(book)
            save_library(library)
            st.success("Book added successfully!")

elif menu == "Remove a Book":
    st.subheader("Remove a Book")
    book_titles = [book["title"] for book in library]
    title_to_remove = st.selectbox("Select a book to remove", book_titles) 
    
    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != title_to_remove]
        save_library(library)
        st.success("Book removed successfully!")

elif menu == "Search for a Book":
    st.subheader("Search for a Book")
    search_term = st.text_input("Enter title or author")
    if st.button("Search"):
        if not search_term:
            st.warning("Please enter a title or author to search.")
        else:
            results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
            if results:
                for book in results:
                    st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
            else:
                st.warning("No matching books found.")

elif menu == "Display All Books":
    st.subheader("Your Library")
    if not library:
        st.write("Your library is empty.")
    else:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

elif menu == "Display Statistics":
    st.subheader("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    
    genre_count = Counter([book["genre"] for book in library])
    most_common_genre = genre_count.most_common(1)
    if most_common_genre:
        most_common_genre = most_common_genre[0]
    else:
        most_common_genre = ("N/A", 0)
    
    average_year = sum(book["year"] for book in library) / total_books if total_books > 0 else 0

    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {read_percentage:.1f}%")
    st.write(f"Most common genre: {most_common_genre[0]} with {most_common_genre[1]} books")
    st.write(f"Average publication year: {average_year:.0f}")
