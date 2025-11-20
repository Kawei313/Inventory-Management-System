CREATE DATABASE IF NOT EXISTS inventory_system;
USE inventory_system;

-- BẢNG NHÂN VIÊN
CREATE TABLE IF NOT EXISTS employee_data (
    empid INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    gender VARCHAR(50),
    dob VARCHAR(30),
    contact VARCHAR(30),
    employment_type VARCHAR(50),
    education VARCHAR(50),
    word_shift VARCHAR(50),
    address VARCHAR(100),
    doj VARCHAR(30),
    salary VARCHAR(50),
    usertype VARCHAR(50),
    password VARCHAR(50)
);

-- BẢNG NHÀ CUNG CẤP
CREATE TABLE IF NOT EXISTS supplier_data (
    invoice INT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(15),
    description TEXT
);

-- BẢNG DANH MỤC SẢN PHẨM
CREATE TABLE IF NOT EXISTS category_data (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

-- BẢNG SẢN PHẨM
CREATE TABLE IF NOT EXISTS product_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    supplier VARCHAR(100),
    name VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT,
    status VARCHAR(50)
);

-- 🧾 BẢNG THUẾ (TAX)
CREATE TABLE IF NOT EXISTS tax_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tax_rate DECIMAL(5,2),  -- Ví dụ: 8.00 cho 8%
    effective_date DATE DEFAULT (CURRENT_DATE)
);

-- 💰 BẢNG HÓA ĐƠN BÁN HÀNG
CREATE TABLE IF NOT EXISTS sales_data (
    invoice_no INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_contact VARCHAR(20),
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2),
    discount DECIMAL(10,2),
    tax DECIMAL(10,2),
    net_pay DECIMAL(12,2)
);

-- 🛒 BẢNG CHI TIẾT SẢN PHẨM TRONG HÓA ĐƠN
CREATE TABLE IF NOT EXISTS sales_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no INT,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    discount DECIMAL(10,2),
    final_price DECIMAL(12,2),
    FOREIGN KEY (invoice_no) REFERENCES sales_data(invoice_no) ON DELETE CASCADE
);

-- 📊 BẢNG PHÂN QUYỀN NGƯỜI DÙNG (nếu có admin và user)
CREATE TABLE IF NOT EXISTS user_accounts (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    empid INT,
    username VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',  -- admin hoặc user
    FOREIGN KEY (empid) REFERENCES employee_data(empid)
);