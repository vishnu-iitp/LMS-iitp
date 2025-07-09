import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt
from db import DatabaseManager
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import qdarkstyle

# first dialogue box 
class LoginDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("LMS Login")
        self.resize(300, 150)
        layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton("Login")
        btn_register = QPushButton("Register")

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_register)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        btn_login.clicked.connect(self.attempt_login)
        btn_register.clicked.connect(self.open_register)

        self.user_info = None  

    def attempt_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return
        info = self.db.validate_login(username, password)
        if info:
            self.user_info = info
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_register(self):
        dlg = RegisterDialog(self.db)
        dlg.exec_()

# register wala screen
class RegisterDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Register New Account")
        self.resize(400, 300)
        layout = QVBoxLayout()

        # Member details
        self.fullname_edit = QLineEdit()
        self.fullname_edit.setPlaceholderText("Full Name")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Phone")

        # User credentials
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("Confirm Password")
        self.confirm_edit.setEchoMode(QLineEdit.Password)

        btn_register = QPushButton("Create Account")

        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.fullname_edit)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.confirm_edit)
        layout.addWidget(btn_register)

        self.setLayout(layout)

        btn_register.clicked.connect(self.attempt_register)

    def attempt_register(self):
        full_name = self.fullname_edit.text().strip()
        email = self.email_edit.text().strip()
        phone = self.phone_edit.text().strip()
        username = self.username_edit.text().strip()
        pwd = self.password_edit.text().strip()
        confirm = self.confirm_edit.text().strip()
        if not all([full_name, email, username, pwd, confirm]):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return
        if pwd != confirm:
            QMessageBox.warning(self, "Password Error", "Passwords do not match.")
            return
        success = self.db.create_member_and_user(full_name, email, phone, username, pwd)
        if success:
            QMessageBox.information(self, "Success", "Account created! You can now login.")
            self.accept()
        else:
            QMessageBox.warning(self, "Registration Failed", "Username or email may already exist.")

# sara tabs ke liye class
class BooksTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Search operation 
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by title or author")
        btn_search = QPushButton("Search")
        btn_refresh = QPushButton("Refresh")
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(btn_search)
        search_layout.addWidget(btn_refresh)

        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        headers = ["ID","Title","Author","Publisher","ISBN","Year","Total","Available"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
        form_layout = QHBoxLayout()
        self.inp_title = QLineEdit(); self.inp_title.setPlaceholderText("Title")
        self.inp_author = QLineEdit(); self.inp_author.setPlaceholderText("Author")
        self.inp_publisher = QLineEdit(); self.inp_publisher.setPlaceholderText("Publisher")
        self.inp_isbn = QLineEdit(); self.inp_isbn.setPlaceholderText("ISBN")
        self.inp_year = QLineEdit(); self.inp_year.setPlaceholderText("Year")
        self.inp_copies = QLineEdit(); self.inp_copies.setPlaceholderText("Copies")
        btn_add = QPushButton("Add Book")
        form_layout.addWidget(self.inp_title)
        form_layout.addWidget(self.inp_author)
        form_layout.addWidget(self.inp_publisher)
        form_layout.addWidget(self.inp_isbn)
        form_layout.addWidget(self.inp_year)
        form_layout.addWidget(self.inp_copies)
        form_layout.addWidget(btn_add)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(form_layout)
        self.setLayout(layout)

        
        btn_search.clicked.connect(self.search_books)
        btn_refresh.clicked.connect(self.load_all_books)
        btn_add.clicked.connect(self.add_book)

       
        self.load_all_books()

    def load_all_books(self):
        self.search_edit.clear()
        books = self.db.get_all_books()
        self._populate_table(books)

    def search_books(self):
        kw = self.search_edit.text().strip()
        if not kw:
            self.load_all_books()
        else:
            books = self.db.search_books(kw)
            self._populate_table(books)

    def _populate_table(self, books_list):
        self.table.setRowCount(0)
        for row_data in books_list:
            row = self.table.rowCount()
            self.table.insertRow(row)
            vals = [
                row_data.get('book_id'),
                row_data.get('title'),
                row_data.get('author'),
                row_data.get('publisher'),
                row_data.get('isbn'),
                row_data.get('year_published'),
                row_data.get('total_copies'),
                row_data.get('available_copies'),
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def add_book(self):
        title = self.inp_title.text().strip()
        author = self.inp_author.text().strip()
        publisher = self.inp_publisher.text().strip()
        isbn = self.inp_isbn.text().strip()
        year = self.inp_year.text().strip()
        copies = self.inp_copies.text().strip()
        if not title or not isbn or not year or not copies:
            QMessageBox.warning(self, "Input Error", "Title, ISBN, Year, and Copies are required.")
            return
        try:
            year_int = int(year)
            copies_int = int(copies)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Year and Copies must be integers.")
            return
        success = self.db.add_book(title, author, publisher, isbn, year_int, copies_int)
        if success:
            QMessageBox.information(self, "Success", "Book added.")
            self.inp_title.clear(); self.inp_author.clear()
            self.inp_publisher.clear(); self.inp_isbn.clear()
            self.inp_year.clear(); self.inp_copies.clear()
            self.load_all_books()
        else:
            QMessageBox.warning(self, "Failed", "Could not add book (maybe duplicate ISBN).")

class IssueReturnTab(QWidget):
    
    def __init__(self, db_manager, current_member_id):
        super().__init__()
        self.db = db_manager
        self.member_id = current_member_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

       
        issue_label = QLabel("Issue a Book:")
        self.combo_books = QComboBox()
        btn_issue = QPushButton("Issue Selected Book")
        issue_layout = QHBoxLayout()
        issue_layout.addWidget(self.combo_books)
        issue_layout.addWidget(btn_issue)

        
        return_label = QLabel("My Borrowed Books (Return below):")
        self.table_issued = QTableWidget()
        self.table_issued.setColumnCount(5)
        headers = ["Issue ID","Book ID","Title","Issue Date","Due Date"]
        self.table_issued.setHorizontalHeaderLabels(headers)
        self.table_issued.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        btn_return = QPushButton("Return Selected Book")

        layout.addWidget(issue_label)
        layout.addLayout(issue_layout)
        layout.addWidget(return_label)
        layout.addWidget(self.table_issued)
        layout.addWidget(btn_return)
        self.setLayout(layout)

        btn_issue.clicked.connect(self.issue_book)
        btn_return.clicked.connect(self.return_book)

        self.load_available_books()
        self.load_issued_books()

    def load_available_books(self):
        self.combo_books.clear()
        books = self.db.get_available_books()
        for b in books:
            text = f"{b['book_id']}: {b['title']} (Available: {b['available_copies']})"
            self.combo_books.addItem(text, b['book_id'])

    def load_issued_books(self):
        data = self.db.get_issued_books_by_member(self.member_id)
        self.table_issued.setRowCount(0)
        for row_data in data:
            row = self.table_issued.rowCount()
            self.table_issued.insertRow(row)
            vals = [
                row_data.get('issue_id'),
                row_data.get('book_id'),
                row_data.get('title'),
                row_data.get('issue_date'),
                row_data.get('due_date'),
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_issued.setItem(row, col, item)

    def issue_book(self):
        idx = self.combo_books.currentIndex()
        if idx < 0:
            return
        book_id = self.combo_books.currentData()
        if book_id is None:
            return
        success = self.db.issue_book(book_id, self.member_id)
        if success:
            QMessageBox.information(self, "Issued", "Book issued successfully.")
        else:
            QMessageBox.warning(self, "Failed", "Failed to issue book.")
        self.load_available_books()
        self.load_issued_books()

    def return_book(self):
        selected = self.table_issued.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Select Error", "Select a row to return.")
            return
        issue_id_item = self.table_issued.item(selected, 0)
        if not issue_id_item:
            return
        issue_id = int(issue_id_item.text())
        success = self.db.return_book(issue_id)
        if success:
            QMessageBox.information(self, "Returned", "Book returned successfully.")
        else:
            QMessageBox.warning(self, "Failed", "Failed to return book.")
        self.load_available_books()
        self.load_issued_books()

class ReportsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(5,4)))
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.plot_top_issued()

    def plot_top_issued(self):
        data = self.db.get_top_issued_books(limit=10)
        titles = [row['title'] for row in data]
        counts = [row['issue_count'] for row in data]
        ax = self.canvas.figure.subplots()
        ax.clear()
        if titles:
            ax.bar(titles, counts)
            ax.set_xlabel("Book Title")
            ax.set_ylabel("Issue Count")
            ax.set_title("Top Issued Books")
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, "No issues yet", ha='center', va='center')
        self.canvas.draw()

class SettingsTab(QWidget):

    def __init__(self, app_ref):
        super().__init__()
        self.app = app_ref
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.checkbox_dark = QCheckBox("Enable Dark Mode")
        layout.addWidget(self.checkbox_dark)
        self.setLayout(layout)
        self.checkbox_dark.stateChanged.connect(self.toggle_theme)

    def toggle_theme(self, state):
        if state == Qt.Checked:
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        else:
            self.app.setStyleSheet("")

class MainWindow(QMainWindow):
    def __init__(self, db_manager, user_info):
        super().__init__()
        self.db = db_manager
        self.user_info = user_info
        self.resize(800, 600)

        ui_path = os.path.join(os.path.dirname(__file__), "home.ui")
        if os.path.exists(ui_path):
            try:
                uic.loadUi(ui_path, self)
                
                if hasattr(self, 'tabWidget'):
                    self._setup_tabs(self.tabWidget)
                else:
                    self._create_central_tabs()
            except Exception as e:
                print("Failed to load home.ui:", e)
                self._create_central_tabs()
        else:
            self._create_central_tabs()

       
        self.setWindowTitle(f"LMS - Welcome {self.user_info.get('username')}")

    def _create_central_tabs(self):
        tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)
        self._setup_tabs(tabs)

    def _setup_tabs(self, tabs_widget):
       
        home_tab = QWidget()
        hlayout = QVBoxLayout()
        lbl = QLabel(f"Welcome, {self.user_info.get('username')}!\nUse the tabs to navigate.")
        lbl.setAlignment(Qt.AlignCenter)
        hlayout.addWidget(lbl)
        home_tab.setLayout(hlayout)
        tabs_widget.addTab(home_tab, "Home")

        
        books_tab = BooksTab(self.db)
        tabs_widget.addTab(books_tab, "Books")

       
        issue_tab = IssueReturnTab(self.db, self.user_info.get('member_id'))
        tabs_widget.addTab(issue_tab, "Issue/Return")

       
        reports_tab = ReportsTab(self.db)
        tabs_widget.addTab(reports_tab, "Reports")
       
        index_reports = tabs_widget.indexOf(reports_tab)
        def on_tab_changed(idx):
            if idx == index_reports:
                reports_tab.plot_top_issued()
        tabs_widget.currentChanged.connect(on_tab_changed)

       
        settings_tab = SettingsTab(QApplication.instance())
        tabs_widget.addTab(settings_tab, "Settings")

        
        if hasattr(self, 'actionLogout'):
           
            self.actionLogout.triggered.connect(self.logout)
        else:
            menubar = self.menuBar()
            account_menu = menubar.addMenu("Account")
            logout_action = QtWidgets.QAction("Logout", self)
            account_menu.addAction(logout_action)
            logout_action.triggered.connect(self.logout)

    def logout(self):
        self.close()
        main()


def main():
    app = QApplication(sys.argv)

    
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"  
    DB_PASS = "ayushroot"
    DB_NAME = "lms_db"

    try:
        db_manager = DatabaseManager(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )

    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"Cannot connect to database: {e}")
        sys.exit(1)

    login = LoginDialog(db_manager)
    if login.exec_() == QDialog.Accepted:
        user_info = login.user_info
        window = MainWindow(db_manager, user_info)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

