# Library Management System (LMS) 📚

A simple yet feature-rich **Library Management System** built using **Python** and **MariaDB**.

This project manages books, library members, book issuing/returning, and even offers useful analytics — all through a clean and responsive GUI.

I created this project to learn backend development using Python and MariaDB, including topics like user authentication, CRUD operations, and real-world data relationships.

---

## 🔍 Overview

The LMS uses **PyQt5** for the graphical interface and **MariaDB** as the database engine.  
It supports user authentication, book inventory, member management, issuing/returning books, and visual reports.

### 🔑 Core Features:
- 🔎 Search and manage books
- 👤 Add/edit members and users (with login)
- 🔐 Password hashing using `hashlib`
- 📆 Issue/return books with due dates
- 📊 Top issued books chart
- 🌗 Dark Mode UI toggle

---

## ✨ Quick Tour (Screenshots)

### 🏠 Home Tab
Welcome screen with personalized greeting and navigation instructions.
![Home Tab](/mnt/data/home.png)

---

### 📚 Books Tab
Search, view, and add books with detailed fields like title, author, publisher, ISBN, year, total copies, and available copies.
![Books Tab](/mnt/data/books%20tab.png)

---

### 🔁 Issue/Return Tab
Allows users to issue available books and return previously borrowed ones. Displays book details, issue date, and due date.
![Issue Return Tab](/mnt/data/issue%20return%20tab.png)

---

### 📈 Reports Tab
Visualizes the top issued books using a clean bar chart powered by `matplotlib`.
![Reports Tab](/mnt/data/reports.png)

---

### ⚙️ Settings Tab
Toggle dark mode to switch between light and dark themes.
![Settings Tab](/mnt/data/settings.png)

---

## 🛠️ Technologies Used

- **Python 3**
- **MariaDB**
- **PyMySQL** — Database connection
- **PyQt5** — GUI
- **hashlib** — Password hashing
- **matplotlib** — Charting
- **datetime** — Due date calculations

---

## 📦 Database Tables

The system auto-creates these tables if they don't exist:
- `books`
- `members`
- `users`
- `issued_books`

All with proper foreign key relationships for data consistency.

---

## 📘 Sample Data

If your database starts empty, 10 classic books (e.g., *1984*, *The Hobbit*, *Fahrenheit 451*) are automatically added for testing purposes.

---

## 🚀 How to Run

1. **Clone the repository**  
    ```bash
    git clone https://github.com/yourusername/library-management-system.git
    cd library-management-system
    ```

2. **Install dependencies**  
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the GUI application**  
    ```bash
    python3 main.py
    ```

---

## 🙌 Contributing

Pull requests are welcome! If you'd like to add a feature or fix a bug, feel free to fork the repo and make a PR.

---

## 📄 License

This project is open-source under the MIT License.
