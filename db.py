import pymysql
from pymysql.cursors import DictCursor
from datetime import date, timedelta
import hashlib

class DatabaseManager:

    def __init__(self, user, password, database, unix_socket=None, host=None, port=None):
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

        self.conn = pymysql.connect(**conn_args)

    # iss functon me password hassing and user authorization ho rha h 

    def hash_password(self, plain_text_password: str) -> str:
        return hashlib.sha256(plain_text_password.encode('utf-8')).hexdigest()

    def create_member_and_user(self, full_name, email, phone, username, plain_password) -> bool:
        pwd_hash = self.hash_password(plain_password)
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO members (full_name, email, phone)
                    VALUES (%s, %s, %s);
                """, (full_name, email, phone))
                member_id = cursor.lastrowid
            except pymysql.err.IntegrityError:
                return False

            try:
                cursor.execute("""
                    INSERT INTO users (member_id, username, password_hash, role)
                    VALUES (%s, %s, %s, 'member');
                """, (member_id, username, pwd_hash))
                return True
            except pymysql.err.IntegrityError:
                cursor.execute("DELETE FROM members WHERE member_id=%s;", (member_id,))
                return False

    def validate_login(self, username, plain_password):
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
            return None

    # book ka sara operation sql query ke through

    def get_all_books(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books;")
            return cursor.fetchall()

    def search_books(self, keyword):
        like_kw = f"%{keyword}%"
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM books
                WHERE title LIKE %s OR author LIKE %s;
            """, (like_kw, like_kw))
            return cursor.fetchall()

    def add_book(self, title, author, publisher, isbn, year_published, total_copies):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO books
                      (title, author, publisher, isbn, year_published, total_copies, available_copies)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (title, author, publisher, isbn, year_published, total_copies, total_copies))
                return True
            except pymysql.err.IntegrityError:
                return False

    def get_available_books(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books WHERE available_copies > 0;")
            return cursor.fetchall()

    # book issue aur return operation 

    def issue_book(self, book_id, member_id, days=14) -> bool:
        today = date.today()
        due = today + timedelta(days=days)
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
                    VALUES (%s, %s, %s, %s);
                """, (book_id, member_id, today, due))

                cursor.execute("""
                    UPDATE books
                    SET available_copies = available_copies - 1
                    WHERE book_id=%s AND available_copies > 0;
                """, (book_id,))

                if cursor.rowcount == 0:
                    self.conn.rollback()
                    return False
                return True
            except Exception:
                self.conn.rollback()
                return False

    def get_issued_books_by_member(self, member_id):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT ib.issue_id, b.book_id, b.title, ib.issue_date, ib.due_date
                FROM issued_books ib
                JOIN books b ON ib.book_id=b.book_id
                WHERE ib.member_id=%s AND ib.return_date IS NULL;
            """, (member_id,))
            return cursor.fetchall()

    def return_book(self, issue_id) -> bool:
        today = date.today()
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT book_id FROM issued_books
                    WHERE issue_id=%s AND return_date IS NULL;
                """, (issue_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                book_id = row['book_id']
                cursor.execute("""
                    UPDATE issued_books
                    SET return_date=%s
                    WHERE issue_id=%s;
                """, (today, issue_id))
                cursor.execute("""
                    UPDATE books
                    SET available_copies = available_copies + 1
                    WHERE book_id=%s;
                """, (book_id,))
                return True
            except Exception:
                self.conn.rollback()
                return False

    # graph ke liye most issued books ka data yaha se 

    def get_top_issued_books(self, limit=10):
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

    # yaha se connection close

    def close(self):
        self.conn.close()

