# Library Management System (LMS) 📚

This is a simple yet functional **Library Management System** built using **Python** and **MariaDB**.  
It manages books, library members, issuing and returning of books, and basic analytics like top issued books.

I built this project to understand how a backend system works with databases — including how to structure tables, write CRUD operations, implement login systems, and handle real-world use cases like issuing books with due dates.

---

## 🔍 Overview

The system is written in Python and connects to a MariaDB database using the `PyMySQL` library.  
It runs as a backend module and can be easily integrated with a GUI (like Tkinter) or a web frontend (like Flask/Django) if needed.

### Key Functionalities:
- Add/search books
- Register members and users (with roles)
- Login authentication with hashed passwords
- Issue and return books
- View current issued books
- Simple analytics: top issued books

---

## 🛠️ Technologies Used

- **Python 3**
- **MariaDB**
- **PyMySQL** (for database connection)
- **hashlib** (for password hashing)
- **datetime** (for date calculations)

---

## 📦 Database Tables

The project automatically creates the following tables if they don’t exist:
- `books`
- `members`
- `users`
- `issued_books`

Each table uses proper relationships via foreign keys, ensuring consistency in the data.

---

## 📘 Sample Books

If the database is empty, the system seeds it with 10 popular classic books like *1984*, *The Great Gatsby*, *The Hobbit*, etc.  
This makes it easier to test the application immediately after setup.

---

## 🧪 How to Run

1. **Clone this repository**:
    ```bash
    git clone https://github.com/yourusername/library-management-system.git
    cd library-management-system
    ```
2. **Install all the reuirements**
    ```bash
    pip install -r requirements
    ```

Install all the required libraries and then proceed to step 3 

---

3. **Run the GUI application**
   ```bash
   python3 main.py
   ```
