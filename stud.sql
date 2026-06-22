CREATE DATABASE IF NOT EXISTS stud;
USE stud;

-- 1. Donator Registration Table
CREATE TABLE IF NOT EXISTS donorreg (
    Slno INT AUTO_INCREMENT UNIQUE KEY,
    Donorid VARCHAR(50) PRIMARY KEY,
    Dname VARCHAR(50) NOT NULL,
    Dpsd VARCHAR(255) NOT NULL,
    Dcpsd VARCHAR(255) NOT NULL,
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
    Remarks VARCHAR(20) NULL,
    Donorid VARCHAR(50) DEFAULT NULL
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

-- 8. Administrator Credentials Table
CREATE TABLE IF NOT EXISTS adminlogin (
    AdminID VARCHAR(50) PRIMARY KEY,
    AdminName VARCHAR(100) NOT NULL,
    AdminEmail VARCHAR(100) NOT NULL UNIQUE,
    AdminPassword VARCHAR(255) NOT NULL,
    AdminPhone VARCHAR(15),
    AdminAddress VARCHAR(255),
    Created_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(20) DEFAULT 'Active'
);

-- 9. Admin Active Sessions Table
CREATE TABLE IF NOT EXISTS admin_sessions (
    SessionID VARCHAR(100) PRIMARY KEY,
    AdminID VARCHAR(50),
    LoginTime DATETIME,
    LastActivity DATETIME,
    LogoutTime DATETIME,
    FOREIGN KEY (AdminID) REFERENCES adminlogin(AdminID) ON DELETE CASCADE
);

-- 10. Admin Audit Logs Table
CREATE TABLE IF NOT EXISTS admin_audit_logs (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    AdminID VARCHAR(50),
    Action VARCHAR(255),
    Details TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AdminID) REFERENCES adminlogin(AdminID) ON DELETE CASCADE
);

-- 11. Add UserRole Column to donorreg Table (Role Differentiation)
ALTER TABLE donorreg ADD COLUMN UserRole VARCHAR(20) DEFAULT 'donor';

-- 12. Insert Default Administrator (Default login credentials)
-- Hashed password matches 'admin123' via Django's secure PBKDF2 hashing
INSERT INTO adminlogin (AdminID, AdminName, AdminEmail, AdminPassword, AdminPhone, AdminAddress, Status)
VALUES ('admin', 'Admin User', 'admin@example.com', 'pbkdf2_sha256$1200000$yyBlhRpkzjEB636zszzkhg$eoPJGJsH+51PayqQi4yG+BQzrqsxKrR0olF1uaxzfOM=', '9999999999', 'Admin Headquarters', 'Active')
ON DUPLICATE KEY UPDATE AdminID=AdminID;
