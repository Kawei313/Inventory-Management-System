import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import sys, importlib

# ===== Hàm Logout =====
def logout(win):
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?")
    if confirm:
        win.destroy()
        import login_auto_role
        importlib.reload(login_auto_role)
        login_auto_role.open_login_window()

# ===== Kết nối database =====
def connect_db():
    try:
        con = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",      # ⚠️ chỉnh theo mật khẩu MySQL của bạn
            database="inventory_system"
        )
        cur = con.cursor()
        return con, cur
    except Exception as e:
        messagebox.showerror("Database Error", f"Không thể kết nối database:\n{e}")
        return None, None

# ===== Hiển thị toàn bộ sản phẩm =====
def fetch_all_products(tree):
    con, cur = connect_db()
    if not con:
        return
    try:
        cur.execute("SELECT invoice_no, product_name, price, discount FROM sales_items")
        rows = cur.fetchall()
        tree.delete(*tree.get_children())  # xoá cũ
        for row in rows:
            tree.insert("", "end", values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi khi lấy dữ liệu sản phẩm:\n{e}")

# ===== Tìm kiếm sản phẩm theo tên =====
def search_product(tree, keyword):
    con, cur = connect_db()
    if not con:
        return
    try:
        cur.execute("SELECT invoice_no, product_name, price, discount FROM sales_items WHERE name LIKE %s",
                    ("%" + keyword + "%",))
        rows = cur.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi tìm kiếm:\n{e}")

# ===== Giao diện chính =====
def open_user_dashboard(username):
    win = tk.Tk()
    win.title("Inventory Management System - User")
    win.geometry("1200x700")
    win.configure(bg="white")

    # --- Header ---
    header = tk.Frame(win, bg="#0B3D91", height=60)
    header.pack(fill="x")

    tk.Label(header, text="Inventory Management System", bg="#0B3D91", fg="white",
             font=("Helvetica", 20, "bold")).pack(side="left", padx=20)
    tk.Label(header, text=f"Welcome {username}", bg="#0B3D91", fg="white",
             font=("Arial", 12, "italic")).pack(side="left", padx=20)

    tk.Button(header, text="Logout", bg="#003366", fg="white",
              font=("Arial", 11, "bold"), width=10,
              command=lambda: logout(win)).pack(side="right", padx=10, pady=10)

    # --- Left: Product List ---
    left_frame = tk.LabelFrame(win, text="All Products", font=("Arial", 12, "bold"),
                               bg="white", width=400, height=550)
    left_frame.place(x=20, y=80)

    tk.Label(left_frame, text="Product Name:", bg="white").place(x=10, y=10)
    search_entry = tk.Entry(left_frame, width=25)
    search_entry.place(x=130, y=10)
    tk.Button(left_frame, text="Search", bg="#4A90E2", fg="white",
              command=lambda: search_product(product_table, search_entry.get())
              ).place(x=320, y=8)

    # Product table
    cols = ("ID", "Name", "Price", "Discount")
    product_table = ttk.Treeview(left_frame, columns=cols, show="headings", height=18)
    for col in cols:
        product_table.heading(col, text=col)
        product_table.column(col, width=90)
    product_table.place(x=10, y=50)

    # Gọi dữ liệu thật từ MySQL
    fetch_all_products(product_table)

    # --- Right: Billing Area ---
    bill_frame = tk.LabelFrame(win, text="Customer Billing Area", font=("Arial", 12, "bold"),
                               bg="#fefae0", width=700, height=550)
    bill_frame.place(x=450, y=80)

    tk.Label(bill_frame, text="Customer Name:", bg="#fefae0").place(x=10, y=10)
    cust_name = tk.Entry(bill_frame, width=25)
    cust_name.place(x=150, y=10)
    tk.Label(bill_frame, text="Contact No:", bg="#fefae0").place(x=10, y=40)
    cust_phone = tk.Entry(bill_frame, width=25)
    cust_phone.place(x=150, y=40)

    bill_text = tk.Text(bill_frame, width=75, height=25)
    bill_text.place(x=10, y=80)

    # --- Bottom Buttons ---
    bottom = tk.Frame(win, bg="white")
    bottom.pack(side="bottom", fill="x", pady=10)
    tk.Button(bottom, text="Generate Bill", bg="#4A90E2", fg="white",
              font=("Arial", 11, "bold"), width=15).pack(side="left", padx=50)
    tk.Button(bottom, text="Print", bg="#4A90E2", fg="white",
              font=("Arial", 11, "bold"), width=15).pack(side="left", padx=20)
    tk.Button(bottom, text="Clear All", bg="#D9534F", fg="white",
              font=("Arial", 11, "bold"), width=15).pack(side="left", padx=20)

    win.mainloop()

# Test trực tiếp
if __name__ == "__main__":
    open_user_dashboard("UserTest")
