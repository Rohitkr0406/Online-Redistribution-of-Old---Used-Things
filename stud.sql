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

-- 8. Add UserRole Column to donorreg Table (Role Differentiation)
ALTER TABLE donorreg ADD COLUMN UserRole VARCHAR(20) DEFAULT 'donor';

-- 9. Recipient / Needy Person Registration Table
CREATE TABLE IF NOT EXISTS recipient (
    Slno INT AUTO_INCREMENT UNIQUE KEY,
    Recipientid VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Mobile VARCHAR(20) NOT NULL,
    Address VARCHAR(200) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    Pin VARCHAR(10) NULL,
    Password VARCHAR(255) NOT NULL,
    Remarks VARCHAR(200) NULL,
    UserRole VARCHAR(20) DEFAULT 'recipient',
    DateJoined DATE NULL
);

-- 10. Donation Requests Table
CREATE TABLE IF NOT EXISTS donationrequest (
    ReqId VARCHAR(50) PRIMARY KEY,
    Recipientid VARCHAR(50) NOT NULL,
    Proid VARCHAR(50) NOT NULL,
    ReqDate DATE NOT NULL,
    Status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    Remarks VARCHAR(200) NULL
);

-- Note: Administrator management is natively handled through Django's built-in
-- authentication and administration framework (django.contrib.auth / django.contrib.admin).
-- Administrator superusers are created via: python manage.py createsuperuser

