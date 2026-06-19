# Online Redistribution of Old & Used Things for the Needy

"Online Redistribution of Old & Used Things for the Needy" is a web-based client-server system built with **Python (3.7+)**, **Django 6.0.6**, and **MySQL** that connects donors who have unused items (clothes, books, utensils, furniture, etc.) with underprivileged communities and organizations in need.

The application streamlines collection, inventory (stock management), distribution, complaint tracking, and detailed report generation, replacing manual registers with a digital platform.

---

## 📖 Table of Contents
1. [Key Features](#-key-features)
2. [Project Architecture](#-project-architecture)
3. [Technology Stack](#-technology-stack)
4. [Project Structure](#-project-structure)
5. [Database Schema & SQL Script](#-database-schema--sql-script)
6. [Installation & Setup Guide](#-installation--setup-guide)
7. [Running the Project](#-running-the-project)
8. [Limitations & Future Scope](#-limitations--future-scope)
9. [Bibliography](#-bibliography)

---

## ✨ Key Features

- **Donor Registration & Profiles:** Allows individuals to sign up, manage profiles, and list usable old items.
- **Unused Things Directory:** Admins record new item entries, categorization, sub-categorization, purchase date, and condition status.
- **Collection Management:** Log donation arrivals, donor addresses, receiver status, and volunteer logs.
- **Stock & Inventory Control:** Live tracking of available items (stock vs. distributed quantities).
- **Redistribution & Logistics:** Track the delivery details, location of distribution, receiver names, contact numbers, and quantity distributed.
- **Support & Communication:** Interactive forms for reporting complaints, registering feedback, and tracking contact requests.
- **Comprehensive Reports:** Separate search-enabled reporting interfaces for donors, collections, distributions, stock, complaints, and contact logs.

---

## 🏗 Project Architecture

This application follows a **Three-Tier Client-Server Architecture**:

1. **Presentation Layer:** Designed using HTML5, CSS3, and JavaScript, rendering clean forms and tables for donors and administrators.
2. **Business Logic Layer:** Django 3.0 controller views implementing backend permissions, access rights, routing, and processing logic.
3. **Data Layer:** A relational MySQL database (`stud`) managing data integrity and validation via the `pymysql` database driver.

---

## 🛠 Technology Stack

- **Front-end:** HTML5, CSS3, JavaScript
- **Back-end Web Framework:** Django 3.0 (with Python 3.7+)
- **Database Engine:** MySQL 5.0.12 or higher
- **Database Driver:** `pymysql`
- **Development IDE:** PyCharm / VS Code
- **Operating System:** Windows 10/11 / Linux

---

## 📁 Project Structure

The project is structured into multiple decoupled Django applications:

```text
Online Redistribution of Old & Used Things/
│
├── FinalProject/              # Main project configurations
│   ├── settings.py            # Main settings (database configs, apps list)
│   ├── urls.py                # Core URL routing
│   └── wsgi.py / asgi.py      # Server entry points
│
├── FirstApp/                  # Home, Login, and Connectivity test module
│   ├── templates/             # HTML Templates (Home.html, LogIn.html)
│   └── views.py               # View logic
│
├── RegApp/                    # Registration & Master items management
│   ├── templates/             # Donator.html, UnUsed.html
│   └── views.py               # Donator and Unused things CRUD logic
│
├── DetailApp/                 # Core collection, stock, and distribution processes
│   ├── templates/             # Collection.html, Stock.html, Distribution.html
│   └── views.py               # Collection, Stock, and Distribution CRUD logic
│
├── ComApp/                    # Suggestions, complaints, and contact submissions
│   ├── templates/             # Complaint.html, ContactUs.html
│   └── views.py               # Complaint & Contact Us data persistence
│
├── ReportApp/                 # Administrative search and report generation
│   ├── templates/             # Report lists, donor/stock/unused report templates
│   └── views.py               # Analytical report queries using LEFT JOINs
│
├── manage.py                  # Django administrative command-line script
├── myenv/                     # Python Virtual Environment
├── project.md                 # Detailed project code and documentation
└── synopsis.md                # Project synopsis overview
```

---

## 🗄 Database Schema & SQL Script

To execute the database logic, you must set up the MySQL database named `stud`. Below is the complete SQL script to create the necessary tables with correct data types matching the codebase:

```sql
CREATE DATABASE IF NOT EXISTS stud;
USE stud;

-- 1. Donator Registration Table
CREATE TABLE IF NOT EXISTS donorreg (
    Slno INT AUTO_INCREMENT UNIQUE KEY,
    Donorid VARCHAR(50) PRIMARY KEY,
    Dname VARCHAR(50) NOT NULL,
    Dpsd VARCHAR(20) NOT NULL,
    Dcpsd VARCHAR(20) NOT NULL,
    Dob VARCHAR(50) NOT NULL,
    Gen VARCHAR(50) NOT NULL,
    Dmob VARCHAR(50) NOT NULL,
    Demail VARCHAR(20) NOT NULL,
    Add1 VARCHAR(100) NOT NULL,
    Add2 VARCHAR(100) NOT NULL,
    State VARCHAR(20) NOT NULL,
    City VARCHAR(30) NOT NULL,
    Pin VARCHAR(30) NULL,
    Remarks VARCHAR(20) NULL
);

-- 2. Used/Old Unused Things Master Table
CREATE TABLE IF NOT EXISTS unusedthing (
    Slno INT UNIQUE KEY,
    Proid VARCHAR(50) PRIMARY KEY,
    ProName VARCHAR(30) NOT NULL,
    ProCate VARCHAR(30) NOT NULL,
    ProSubCate VARCHAR(30) NOT NULL,
    ProSerial VARCHAR(30) NOT NULL,
    ProBatchno VARCHAR(30) NOT NULL,
    PurchDate DATE NOT NULL,
    Status VARCHAR(30) NOT NULL,
    Remarks VARCHAR(20) NULL
);

-- 3. Collections Details Table
CREATE TABLE IF NOT EXISTS collectiontable (
    Slno INT UNIQUE KEY,
    Proid VARCHAR(50) PRIMARY KEY,
    CollQty VARCHAR(10) NOT NULL,
    RecDate DATE NOT NULL,
    Status VARCHAR(30) NOT NULL,
    DonBy VARCHAR(50) NOT NULL,
    DonorAdd VARCHAR(150) NOT NULL,
    RecBy VARCHAR(50) NOT NULL,
    Remarks VARCHAR(150) NOT NULL
);

-- 4. Stock Details Table
CREATE TABLE IF NOT EXISTS stockdetails (
    Slno INT UNIQUE KEY,
    Proid VARCHAR(50) PRIMARY KEY,
    Pname VARCHAR(30) NOT NULL,
    Cate VARCHAR(30) NOT NULL,
    SubCate VARCHAR(30) NOT NULL,
    ProSlno VARCHAR(30) NOT NULL,
    BatchNo VARCHAR(30) NOT NULL,
    DisAmt VARCHAR(30) NOT NULL,
    StockAmt VARCHAR(30) NOT NULL,
    Remarks VARCHAR(20) NULL
);

-- 5. Redistribution/Distribution Details Table
CREATE TABLE IF NOT EXISTS distributetable (
    Slno INT UNIQUE KEY,
    Proid VARCHAR(50) PRIMARY KEY,
    DisQty VARCHAR(10) NOT NULL,
    DisDate DATE NOT NULL,
    DisBy VARCHAR(50) NOT NULL,
    RecName VARCHAR(50) NOT NULL,
    RecAdd VARCHAR(150) NOT NULL,
    RecMob VARCHAR(15) NOT NULL,
    RecBy VARCHAR(50) NOT NULL,
    Remarks VARCHAR(150) NOT NULL
);

-- 6. Suggestions & Complaints Table
CREATE TABLE IF NOT EXISTS complainttable (
    Slno VARCHAR(20) PRIMARY KEY,
    Did VARCHAR(50) NOT NULL,
    CompDate VARCHAR(50) NOT NULL,
    IssuType VARCHAR(50) NOT NULL,
    CompDetails VARCHAR(500) NOT NULL,
    Remarks VARCHAR(200) NULL
);

-- 7. Contact Us Details Table
CREATE TABLE IF NOT EXISTS contactus (
    Slno VARCHAR(20) PRIMARY KEY,
    Admid VARCHAR(50) NOT NULL,
    ComName VARCHAR(50) NOT NULL,
    ComEmail VARCHAR(50) NOT NULL,
    ComAdd VARCHAR(200) NOT NULL,
    ComMob VARCHAR(50) NOT NULL,
    Remarks VARCHAR(200) NULL
);
```

---

## ⚙️ Installation & Setup Guide

### Step 1: Install Python & MySQL
1. Download and install [Python](https://www.python.org/downloads/) (Version 3.7 to 3.12 recommended). Ensure you check **"Add Python to PATH"** during installation.
2. Install [MySQL Server](https://dev.mysql.com/downloads/installer/) (Community Edition) and set up the `root` user password.

### Step 2: Set Up the Database
1. Open the MySQL Command Line Client or a management tool like MySQL Workbench / phpMyAdmin.
2. Log in as your root user:
   ```bash
   mysql -u root -p
   ```
3. Copy, paste, and run the SQL script provided in the [Database Schema & SQL Script](#-database-schema--sql-script) section above.

### Step 3: Configure credentials and environment variables
This project no longer hardcodes secrets in source. It loads configuration from environment variables (or a local `.env` during development).

- Copy the example env file and edit values for your machine:

    - PowerShell:
        ```powershell
        Copy-Item .env.example .env
        notepad .env
        ```
    - Linux/macOS:
        ```bash
        cp .env.example .env
        nano .env
        ```

- Required variables (see `.env.example`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

- Security notes:
    - Keep `.env` private. The repository contains `.env.example` (safe) and `.gitignore` already ignores `.env`.
    - If you ever accidentally commit secrets, rotate them immediately (change DB password, regenerate secret keys, API keys).
    - To untrack a local `.env` accidentally committed run:
        ```bash
        git rm --cached .env
        git commit -m "Stop tracking local .env"
        ```
    - To purge secrets from git history consider using `git filter-repo` or the BFG Repo-Cleaner. Example (dangerous — read docs first):
        ```bash
        # using git filter-repo (must be installed)
        git filter-repo --path .env --invert-paths
        ```

### Step 4: Virtual environment & dependencies
1. Open a terminal in the project root.
2. Activate the included virtual environment (the repo contains `myenv`):

     - PowerShell:
         ```powershell
         .\myenv\Scripts\Activate.ps1
         ```
     - Command Prompt:
         ```cmd
         .\myenv\Scripts\activate.bat
         ```
     - Linux/macOS (if you create your own venv):
         ```bash
         source myenv/bin/activate
         ```

3. Install runtime dependencies from the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

`requirements.txt` includes `Django==6.0.6`, `python-dotenv` (optional, used to load `.env` locally), and `mysqlclient`.

---

## 🚀 Running the Project

1. Verify the database connectivity by starting the Django development server:
   ```bash
   python manage.py runserver
   ```
2. Open your web browser and navigate to:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3. To verify the MySQL connection from the browser, visit the Connectivity test page:
   [http://127.0.0.1:8000/FirstApp/ConnecivityPage](http://127.0.0.1:8000/FirstApp/ConnecivityPage)
   * If correct, you will see a message: `"Database Connected Successfully..."`
   * If there is an error, review the MySQL configuration parameters.

### Accessing Project Sections:
- **Home:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Donator Registration:** [http://127.0.0.1:8000/RegApp/Donator](http://127.0.0.1:8000/RegApp/Donator)
- **Unused Things Entry:** [http://127.0.0.1:8000/RegApp/Unused](http://127.0.0.1:8000/RegApp/Unused)
- **Collections Log:** [http://127.0.0.1:8000/DetailApp/Collection](http://127.0.0.1:8000/DetailApp/Collection)
- **Stock Log:** [http://127.0.0.1:8000/DetailApp/Stock](http://127.0.0.1:8000/DetailApp/Stock)
- **Distribution Details:** [http://127.0.0.1:8000/DetailApp/Distribution](http://127.0.0.1:8000/DetailApp/Distribution)
- **Complaints & Feedback:** [http://127.0.0.1:8000/ComApp/Complaint](http://127.0.0.1:8000/ComApp/Complaint)
- **Contact Us:** [http://127.0.0.1:8000/ComApp/Contactus](http://127.0.0.1:8000/ComApp/Contactus)
- **Reports Dashboard:** [http://127.0.0.1:8000/ReportApp/](http://127.0.0.1:8000/ReportApp/)

---

## ⚠️ Limitations & Future Scope

### Current Limitations:
1. **Direct Password Storage:** Current version stores passwords as plain text in the custom database table.
2. **Local MySQL Hardcoding:** Database settings are declared directly in Python views instead of centralized configuration files.
3. **No Financial Transactions:** Does not support shipping fees or monetized donations.
4. **Manual Logistics:** No automated tracking of delivery routes or courier partners.

### Future Scope:
- Integration of Django's default `contrib.auth` for encrypted authentication.
- Developing native mobile companion apps for Android & iOS.
- Cloud hosting deployment (AWS RDS/Azure SQL) for automatic backup, failover, and global reach.
- Integration of SMTP/SMS gateways for live notifications to donors and receivers.

---

## 📚 Bibliography

### Reference Books:
* **Python Crash Course** – Eric Matthews
* **Head-First Python** – Paul Barry
* **Learn Python the Hard Way** – Zed A. Shaw (3rd Edition)
* **Python Programming** – John Zelle
* **Learn MySQL Administration in a Month of Lunches** – Don Jones

### Websites Referenced:
* [Django Project Documentation](https://docs.djangoproject.com/)
* [PyMySQL PyPI documentation](https://pypi.org/project/PyMySQL/)
* [Coders Helpline](https://www.codershelpline.com/)
* [TutorialsPoint](https://www.tutorialspoint.com/)
