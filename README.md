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
![Home Tab](/assets/home.png)

---

### 📚 Books Tab
Search, view, and add books with detailed fields like title, author, publisher, ISBN, year, total copies, and available copies.
![Books Tab](/assets/books%20tab.png)

---

### 🔁 Issue/Return Tab
Allows users to issue available books and return previously borrowed ones. Displays book details, issue date, and due date.
![Issue Return Tab](/assets/issue%20return%20tab.png)

---

### 📈 Reports Tab
Visualizes the top issued books using a clean bar chart powered by `matplotlib`.
![Reports Tab](/assets/reports.png)

---

### ⚙️ Settings Tab
Toggle dark mode to switch between light and dark themes.
![Settings Tab](/assets/settings.png)

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
**Important**<br>
run all this command in one single terminal , otherwise use full path for files 
1. **Install git (if not already installed)**
   ```bash
   winget install --id Git.Git -e --source winget
   ```
2. **Clone the repository (open powershell)**  
    ```bash
    cd Downloads
    git clone https://github.com/vishnu-iitp/LMS-iitp.git
    cd LMS-iitp
    ```

3. **Install dependencies**  
    ```bash
    pip install -r requirements.txt
    ```

4. **Create The database and run the sql code** <br>
    I. create first local connection (if not alreay created )
   ```bash
   mysql -u root -p
   ```
    II. Open Mysql workbench<br>
    III. Use the local connection ( default username and password is root )<br>
    IV. Create schema (right click on left pannel (Schema ) >>click on create schema  >> name it lms_db >> apply >> apply >> finish<br>
    V. file > open sql script >> choose the lms_db.sql >> click on thunder ⚡ icon to run it<br>
6. **Now Run the Main.py file (open powershell )**
    ```python
    python main.py
    ```
 
7. **first register and then login with the same username and password**
8. **Enjoy**

---

## 🙌 Contributing

Pull requests are welcome! If you'd like to add a feature or fix a bug, feel free to fork the repo and make a PR.

---

## 📄 License

This project is open-source under the MIT License.
