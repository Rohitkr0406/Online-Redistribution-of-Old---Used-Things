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
├── myenv/
├── Project SRS                   # Projct requirements and specifications
     ├── project.md                 # Detailed project code and documentation
     └── synopsis.md                # Project synopsis overview
```

---

## 🗄 Database Schema & SQL Script

The complete MySQL database schema, table definitions, default roles, and default administrator credentials are defined in the [stud.sql](file:///d:/Coding/Online%20Redistribution%20of%20Old%20&%20Used%20Things/stud.sql) file at the root of the project.

---

## ⚙️ Installation & Setup Guide

### Step 1: Install Python & MySQL
1. Download and install [Python](https://www.python.org/downloads/) (Version 3.7 to 3.14.3 recommended). Ensure you check **"Add Python to PATH"** during installation.
2. Install [MySQL Server](https://dev.mysql.com/downloads/installer/) (Community Edition) and set up the `root` user password.

### Step 2: Set Up the Database
1. Open your terminal or command prompt in the project root directory.
2. Run the SQL initialization script using the command:
   ```bash
   mysql -u root -p < stud.sql
   ```
   *(Alternatively, you can open [stud.sql](file:///d:/Coding/Online%20Redistribution%20of%20Old%20&%20Used%20Things/stud.sql), copy its contents, and execute them inside MySQL Workbench or phpMyAdmin).*

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
2. Create a virtual environment named `myenv` (since virtual environment folders are gitignored):

     - Windows (PowerShell/CMD):
         ```bash
         python -m venv myenv
         ```
     - Linux/macOS:
         ```bash
         python3 -m venv myenv
         ```

3. Activate the virtual environment:

     - PowerShell:
         ```powershell
         .\myenv\Scripts\Activate.ps1
         ```
     - Command Prompt:
         ```cmd
         .\myenv\Scripts\activate.bat
         ```
     - Linux/macOS:
         ```bash
         source myenv/bin/activate
         ```

4. Install runtime dependencies from the provided `requirements.txt`:

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

#### 1. Donor Portal & Public Site
- **Home / About:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Donator Registration:** [http://127.0.0.1:8000/RegApp/Donator](http://127.0.0.1:8000/RegApp/Donator)
- **Donor Login:** [http://127.0.0.1:8000/FirstApp/Login](http://127.0.0.1:8000/FirstApp/Login)
- **Donate Unused Things:** [http://127.0.0.1:8000/RegApp/Unused](http://127.0.0.1:8000/RegApp/Unused) (Requires donor login)
- **Register Complaint:** [http://127.0.0.1:8000/ComApp/Complaint](http://127.0.0.1:8000/ComApp/Complaint) (Requires donor login)
- **Contact Us:** [http://127.0.0.1:8000/ComApp/Contactus](http://127.0.0.1:8000/ComApp/Contactus) (Requires donor login)

#### 2. Administrator Panel
- **Admin Login:** [http://127.0.0.1:8000/admin/login/](http://127.0.0.1:8000/admin/login/)
  - **Default AdminID:** `admin` *(or Email:* `admin@example.com`*)*
  - **Default Password:** `admin123`
- **Admin Dashboard:** [http://127.0.0.1:8000/admin/dashboard/](http://127.0.0.1:8000/admin/dashboard/)
- **Donors List:** [http://127.0.0.1:8000/admin/donors/](http://127.0.0.1:8000/admin/donors/)
- **Donated Items:** [http://127.0.0.1:8000/admin/items/](http://127.0.0.1:8000/admin/items/)
- **Collection logs:** [http://127.0.0.1:8000/DetailApp/Collection](http://127.0.0.1:8000/DetailApp/Collection) (Restricted to Admin Panel)
- **Stock details:** [http://127.0.0.1:8000/DetailApp/Stock](http://127.0.0.1:8000/DetailApp/Stock) (Restricted to Admin Panel)
- **Distribution details:** [http://127.0.0.1:8000/DetailApp/Distribution](http://127.0.0.1:8000/DetailApp/Distribution) (Restricted to Admin Panel)
- **Reports Dashboard:** [http://127.0.0.1:8000/ReportApp/](http://127.0.0.1:8000/ReportApp/) (Restricted to Admin Panel)

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
