# db.py

import pymysql
from pymysql.cursors import DictCursor
from datetime import date, timedelta
import hashlib

class DatabaseManager:
    """
    Manages connection to MariaDB (via PyMySQL), table creation, seeding, and common operations:
    - User/member creation & authentication
    - Book CRUD
    - Issue/return operations
    - Analytics (top issued books)
    """

    def __init__(self, user, password, database, unix_socket=None, host=None, port=None):
        """
        Initialize connection to MariaDB. On failure, raises exception.

        Parameters:
        - user: str, DB username
        - password: str, DB password
        - database: str, database name
        - unix_socket: str or None, path to the Unix socket file (e.g., "/var/lib/mysql/mysql.sock")
        - host: str or None, hostname for TCP connection (e.g., "127.0.0.1")
        - port: int or None, port for TCP connection (e.g., 3306)

        If unix_socket is provided, connection is attempted via that socket.
        Otherwise, host/port are used for TCP. If host/port are None, defaults to 127.0.0.1:3306.
        """
        conn_args = {
            "user": user,
            "password": password,
            "database": database,
            "cursorclass": DictCursor,
            "autocommit": True,
            "connect_timeout": 5,
        }
        if unix_socket:
            conn_args["unix_socket"] = unix_socket
        else:
            conn_args["host"] = host or "127.0.0.1"
            conn_args["port"] = port or 3306

        # Attempt connection
        self.conn = pymysql.connect(**conn_args)

        # Ensure tables exist and seed sample books if needed
        self._create_tables_if_not_exist()
        self._seed_sample_books_if_empty()

    def _create_tables_if_not_exist(self):
        """
        Create the required tables (books, members, users, issued_books) if they do not already exist.
        """
        with self.conn.cursor() as cursor:
            # books table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
              book_id INT AUTO_INCREMENT PRIMARY KEY,
              title VARCHAR(255) NOT NULL,
              author VARCHAR(255),
              publisher VARCHAR(255),
              isbn VARCHAR(20) UNIQUE,
              year_published YEAR,
              total_copies INT NOT NULL DEFAULT 1,
              available_copies INT NOT NULL DEFAULT 1,
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """)
            # members table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
              member_id INT AUTO_INCREMENT PRIMARY KEY,
              full_name VARCHAR(255) NOT NULL,
              email VARCHAR(255) UNIQUE,
              phone VARCHAR(20),
              join_date DATE DEFAULT CURRENT_DATE,
              status ENUM('active','suspended','alumni') DEFAULT 'active'
            ) ENGINE=InnoDB;
            """)
            # users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              user_id INT AUTO_INCREMENT PRIMARY KEY,
              member_id INT NULL,
              username VARCHAR(50) NOT NULL UNIQUE,
              password_hash VARCHAR(255) NOT NULL,
              role ENUM('member','librarian','admin') NOT NULL DEFAULT 'member',
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (member_id) REFERENCES members(member_id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
            ) ENGINE=InnoDB;
            """)
            # issued_books table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
              issue_id INT AUTO_INCREMENT PRIMARY KEY,
              book_id INT NOT NULL,
              member_id INT NOT NULL,
              issue_date DATE NOT NULL DEFAULT CURRENT_DATE,
              due_date DATE NOT NULL,
              return_date DATE DEFAULT NULL,
              FOREIGN KEY (book_id) REFERENCES books(book_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
              FOREIGN KEY (member_id) REFERENCES members(member_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
              INDEX(book_id),
              INDEX(member_id)
            ) ENGINE=InnoDB;
            """)

    def _seed_sample_books_if_empty(self):
        """
        If books table is empty, insert 10 popular books.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS cnt FROM books;")
            result = cursor.fetchone()
            if result and result.get('cnt', 0) == 0:
                sample_books = [
                    ("1984","George Orwell","Secker & Warburg","9780451524935",1949,5),
                    ("Pride and Prejudice","Jane Austen","T. Egerton","9781503290563",1813,3),
                    ("To Kill a Mockingbird","Harper Lee","J.B. Lippincott & Co.","9780061120084",1960,4),
                    ("The Great Gatsby","F. Scott Fitzgerald","Charles Scribner's Sons","9780743273565",1925,4),
                    ("Moby Dick","Herman Melville","Richard Bentley","9781503280786",1851,2),
                    ("War and Peace","Leo Tolstoy","The Russian Messenger","9780199232765",1869,2),
                    ("Hamlet","William Shakespeare","N/A","9780451526922",1603,3),
                    ("The Catcher in the Rye","J.D. Salinger","Little, Brown and Company","9780316769488",1951,3),
                    ("The Hobbit","J.R.R. Tolkien","George Allen & Unwin","9780547928227",1937,5),
                    ("Fahrenheit 451","Ray Bradbury","Ballantine Books","9781451673319",1953,4),
                ]
                for title, author, publisher, isbn, year, copies in sample_books:
                    try:
                        cursor.execute("""
                        INSERT INTO books 
                          (title, author, publisher, isbn, year_published, total_copies, available_copies)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """, (title, author, publisher, isbn, year, copies, copies))
                    except Exception as e:
                        # Skip any insertion errors (e.g., duplicates)
                        print(f"Seed book insertion error: {e}")

    # ---------- User/Auth methods ----------

    def hash_password(self, plain_text_password: str) -> str:
        """
        Hash a password using SHA-256. (For demo only; consider stronger hashing for production.)
        """
        return hashlib.sha256(plain_text_password.encode('utf-8')).hexdigest()

    def create_member_and_user(self, full_name, email, phone, username, plain_password) -> bool:
        """
        Create a new member and corresponding user.
        Returns True if successful, False if username/email already exists.
        """
        pwd_hash = self.hash_password(plain_password)
        with self.conn.cursor() as cursor:
            # Insert into members
            try:
                cursor.execute("""
                    INSERT INTO members (full_name, email, phone)
                    VALUES (%s, %s, %s);
                """, (full_name, email, phone))
                member_id = cursor.lastrowid
            except pymysql.err.IntegrityError as e:
                # Likely email duplicate
                print("Member creation failed:", e)
                return False

            # Insert into users
            try:
                cursor.execute("""
                    INSERT INTO users (member_id, username, password_hash, role)
                    VALUES (%s, %s, %s, 'member');
                """, (member_id, username, pwd_hash))
                return True
            except pymysql.err.IntegrityError as e:
                # Username duplicate: rollback member insertion
                print("User creation failed:", e)
                # Delete the member row we just inserted
                cursor.execute("DELETE FROM members WHERE member_id=%s;", (member_id,))
                return False

    def validate_login(self, username, plain_password):
        """
        Validate username/password.
        Returns dict {'user_id':..., 'member_id':..., 'username':..., 'role':...} if valid,
        or None if invalid.
        """
        pwd_hash = self.hash_password(plain_password)
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, member_id, password_hash, role
                FROM users
                WHERE username=%s;
            """, (username,))
            row = cursor.fetchone()
            if row and row.get('password_hash') == pwd_hash:
                return {
                    'user_id': row['user_id'],
                    'member_id': row['member_id'],
                    'username': username,
                    'role': row['role']
                }
            else:
                return None

    # ---------- Book operations ----------

    def get_all_books(self):
        """
        Return list of dicts for all books.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books;")
            return cursor.fetchall()

    def search_books(self, keyword):
        """
        Search books by title or author (case-insensitive LIKE).
        """
        like_kw = f"%{keyword}%"
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM books
                WHERE title LIKE %s OR author LIKE %s;
            """, (like_kw, like_kw))
            return cursor.fetchall()

    def add_book(self, title, author, publisher, isbn, year_published, total_copies):
        """
        Insert a new book. Returns True if success, False if e.g. ISBN duplicate.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO books
                      (title, author, publisher, isbn, year_published, total_copies, available_copies)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (title, author, publisher, isbn, year_published, total_copies, total_copies))
                return True
            except pymysql.err.IntegrityError as e:
                print("Add book failed:", e)
                return False

    # ---------- Issue / Return operations ----------

    def get_available_books(self):
        """
        Return list of books with available_copies > 0.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books WHERE available_copies > 0;")
            return cursor.fetchall()

    def issue_book(self, book_id, member_id, days=14) -> bool:
        """
        Issue a book: insert into issued_books, decrement available_copies.
        'days' is loan duration. Returns True if success, False otherwise.
        """
        today = date.today()
        due = today + timedelta(days=days)
        with self.conn.cursor() as cursor:
            try:
                # Insert into issued_books
                cursor.execute("""
                    INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
                    VALUES (%s, %s, %s, %s);
                """, (book_id, member_id, today, due))
                # Decrement available_copies if > 0
                cursor.execute("""
                    UPDATE books
                    SET available_copies = available_copies - 1
                    WHERE book_id=%s AND available_copies > 0;
                """, (book_id,))
                # If no row updated, rollback the issue
                if cursor.rowcount == 0:
                    self.conn.rollback()
                    return False
                return True
            except Exception as e:
                print("Issue book failed:", e)
                self.conn.rollback()
                return False

    def get_issued_books_by_member(self, member_id):
        """
        Return current issued_books entries for this member where return_date IS NULL.
        Includes: issue_id, book_id, title, issue_date, due_date.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT ib.issue_id, b.book_id, b.title, ib.issue_date, ib.due_date
                FROM issued_books ib
                JOIN books b ON ib.book_id=b.book_id
                WHERE ib.member_id=%s AND ib.return_date IS NULL;
            """, (member_id,))
            return cursor.fetchall()

    def return_book(self, issue_id) -> bool:
        """
        Mark return_date = today for the given issue_id, and increment available_copies.
        Returns True if success, False otherwise.
        """
        today = date.today()
        with self.conn.cursor() as cursor:
            try:
                # Get book_id for this issue
                cursor.execute("""
                    SELECT book_id FROM issued_books
                    WHERE issue_id=%s AND return_date IS NULL;
                """, (issue_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                book_id = row['book_id']
                # Update issued_books
                cursor.execute("""
                    UPDATE issued_books
                    SET return_date=%s
                    WHERE issue_id=%s;
                """, (today, issue_id))
                # Increment available_copies
                cursor.execute("""
                    UPDATE books
                    SET available_copies = available_copies + 1
                    WHERE book_id=%s;
                """, (book_id,))
                return True
            except Exception as e:
                print("Return book failed:", e)
                self.conn.rollback()
                return False

    # ---------- Analytics ----------

    def get_top_issued_books(self, limit=10):
        """
        Return list of dicts: { 'title': ..., 'issue_count': ... }, ordered by issue_count DESC, up to `limit`.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT b.title AS title, COUNT(*) AS issue_count
                FROM issued_books ib
                JOIN books b ON ib.book_id=b.book_id
                GROUP BY ib.book_id
                ORDER BY issue_count DESC
                LIMIT %s;
            """, (limit,))
            return cursor.fetchall()

    # ---------- Close ----------

    def close(self):
        """
        Close the underlying DB connection.
        """
        self.conn.close()
