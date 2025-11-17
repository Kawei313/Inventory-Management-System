# dashboard.py - Dashboard + Ẩn Total khi mở Sales, giữ nguyên icon & chức năng
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from employees import employee_form
from supplier import supplier_form
from tax import tax_form
from products import product_form
from category import category_form
from sales import sales_form  # <-- ĐÃ THÊM
import sys
from tkinter import messagebox
import subprocess
import os
import pymysql
from datetime import datetime

def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="Viet20112004@") # Sửa lai account cho đúng
        cursor = connection.cursor()
    except:
        messagebox.showerror("Error", "Database connectivity issue try again")
        return None, None
    return cursor, connection

sys.stdout.reconfigure(encoding='utf-8')

# --- Logout & Exit ---
def logout(window):
    confirm = messagebox.askyesno("Xác nhận Logout", "Bạn có chắc chắn muốn đăng xuất không?")
    if confirm:
        window.destroy()
        python_exec = sys.executable
        subprocess.Popen([python_exec, os.path.join(os.path.dirname(__file__), "login_auto_role.py")])

def exit_app(window):
    confirm = messagebox.askyesno("Xác nhận Thoát", "Bạn có chắc chắn muốn thoát chương trình không?")
    if confirm:
        window.destroy()

# --- Giao diện chính ---
window = Tk()
window.title("Dashboard")
window.geometry("1270x668")
window.resizable(0, 0)
window.config(bg="white")

# Header
bg_image = PhotoImage(file=r"helpers/icons/inventory.png")
titleLabel = Label(window, image=bg_image, compound=LEFT,
                   text="  Inventory Management System",
                   font=("Times New Roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window, text="Logout", font=("Times New Roman", 20, "bold"),
                      fg="#010c48", cursor="hand2", command=lambda: logout(window))
logoutButton.place(x=1100, y=10)

subtitleLabel = Label(window, text="", font=("Times New Roman", 15), bg="#4d636d", fg="white")
subtitleLabel.place(x=0, y=70, relwidth=1)

def update_subtitle():
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M:%S %p")
    subtitleLabel.config(text=f"Welcome Admin\t\t Date: {date}\t\t Time: {time}")
    window.after(1000, update_subtitle)
update_subtitle()

# --- MENU BÊN TRÁI ---
leftFrame = Frame(window)
leftFrame.place(x=0, y=102, width=200, height=555)

logoImage = PhotoImage(file=r"helpers/icons/logo.png")
Label(leftFrame, image=logoImage).pack()

menuLabel = Label(leftFrame, text="Menu", font=("Times New Roman", 20, "bold"), bg="#009688")
menuLabel.pack(fill=X)

# Các nút menu (giữ nguyên icon)
employee_icon = PhotoImage(file=r"helpers/icons/employee.png")
employee_button = Button(leftFrame, image=employee_icon, compound=LEFT, text=" Employees",
                         font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w", padx=10,
                         command=lambda: employee_form(window))
employee_button.pack(fill=X)

supplier_icon = PhotoImage(file=r"helpers/icons/supplier.png")
supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT, text="  Supplier",
                         font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w", padx=10,
                         command=lambda: supplier_form(window))
supplier_button.pack(fill=X)

category_icon = PhotoImage(file=r"helpers/icons/category.png")
category_button = Button(leftFrame, image=category_icon, compound=LEFT, text="  Category",
                         font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w",
                         command=lambda: category_form(window))
category_button.pack(fill=X)

product_icon = PhotoImage(file=r"helpers/icons/product.png")
product_button = Button(leftFrame, image=product_icon, compound=LEFT, text="  Product",
                        font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w",
                        command=lambda: product_form(window))
product_button.pack(fill=X)

sales_icon = PhotoImage(file=r"helpers/icons/sales.png")
sales_button = Button(leftFrame, image=sales_icon, compound=LEFT, text="  Sales",
                      font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w",
                      command=lambda: open_sales())
sales_button.pack(fill=X)

tax_icon = PhotoImage(file=r"helpers/icons/product.png")
tax_button = Button(leftFrame, image=tax_icon, compound=LEFT, text="  Tax",
                    font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w", padx=10,
                    command=lambda: tax_form(window))
tax_button.pack(fill=X)

exit_icon = PhotoImage(file=r"helpers/icons/exit.png")
exit_button = Button(leftFrame, image=exit_icon, compound=LEFT, text="  Exit",
                     font=("Times New Roman", 20, "bold"), cursor="hand2", anchor="w",
                     command=lambda: exit_app(window))
exit_button.pack(fill=X)

# --- VÙNG NỘI DUNG BÊN PHẢI ---
# content_frame = Frame(window, bg="white")
content_frame = None
# Không pack/place ở đây

# --- TẤT CẢ TOTAL FRAMES (giữ nguyên như cũ) ---
emp_frame = Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon = PhotoImage(file=r"helpers/icons/total_employee.png")
Label(emp_frame, image=total_emp_icon, bg="#2C3E50").pack()
Label(emp_frame, text="Total Employees", font=("Times New Roman", 15, "bold"), bg="#2C3E50", fg="white").pack()
total_emp_count_label = Label(emp_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#2C3E50", fg="white")
total_emp_count_label.pack()
for w in (emp_frame, emp_frame.winfo_children()[0], emp_frame.winfo_children()[1], total_emp_count_label):
    w.bind("<Button-1>", lambda e: employee_form(window))

sup_frame = Frame(window, bg="#8E44AD", bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon = PhotoImage(file=r"helpers/icons/total_sup.png")
Label(sup_frame, image=total_sup_icon, bg="#8E44AD").pack()
Label(sup_frame, text="Total Suppliers", font=("Times New Roman", 15, "bold"), bg="#8E44AD", fg="white").pack()
total_sup_count_label = Label(sup_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#8E44AD", fg="white")
total_sup_count_label.pack()
for w in (sup_frame, sup_frame.winfo_children()[0], sup_frame.winfo_children()[1], total_sup_count_label):
    w.bind("<Button-1>", lambda e: supplier_form(window))

cat_frame = Frame(window, bg="#27AE60", bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)
total_cat_icon = PhotoImage(file=r"helpers/icons/total_cat.png")
Label(cat_frame, image=total_cat_icon, bg="#27AE60").pack()
Label(cat_frame, text="Total Categories", font=("Times New Roman", 15, "bold"), bg="#27AE60", fg="white").pack()
total_cat_count_label = Label(cat_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#27AE60", fg="white")
total_cat_count_label.pack()
for w in (cat_frame, cat_frame.winfo_children()[0], cat_frame.winfo_children()[1], total_cat_count_label):
    w.bind("<Button-1>", lambda e: category_form(window))

prod_frame = Frame(window, bg="#E74C3C", bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon = PhotoImage(file=r"helpers/icons/total_prod.png")
Label(prod_frame, image=total_prod_icon, bg="#E74C3C").pack()
Label(prod_frame, text="Total Products", font=("Times New Roman", 15, "bold"), bg="#E74C3C", fg="white").pack()
total_prod_count_label = Label(prod_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#E74C3C", fg="white")
total_prod_count_label.pack()
for w in (prod_frame, prod_frame.winfo_children()[0], prod_frame.winfo_children()[1], total_prod_count_label):
    w.bind("<Button-1>", lambda e: product_form(window))

sales_frame = Frame(window, bg="#6D3CE7", bd=3, relief=RIDGE)
sales_frame.place(x=600, y=495, height=170, width=280)
total_sales_icon = PhotoImage(file=r"helpers/icons/total_sales.png")
Label(sales_frame, image=total_sales_icon, bg="#6D3CE7").pack(pady=10)
Label(sales_frame, text="Total Sales", font=("Times New Roman", 15, "bold"), bg="#6D3CE7", fg="white").pack()
total_sales_count_label = Label(sales_frame, text="0", font=("Times New Roman", 30, "bold"), bg="#6D3CE7", fg="white")
total_sales_count_label.pack()
for w in (sales_frame, sales_frame.winfo_children()[0], sales_frame.winfo_children()[1], total_sales_count_label):
    w.bind("<Button-1>", lambda e: open_sales())

# Danh sách để ẩn/hiện
total_frames = [emp_frame, sup_frame, cat_frame, prod_frame, sales_frame]

# --- MỞ SALES ---
# def open_sales():
#     for f in total_frames:
#         f.place_forget()
#     content_frame.place(x=200, y=102, width=1070, height=555)
#     sales_form(content_frame, show_dashboard)

# --- MỞ SALES ---
def open_sales():
    global content_frame

    # Ẩn tất cả total frames
    for f in total_frames:
        f.place_forget()

    # Hủy content_frame cũ nếu tồn tại
    if content_frame is not None:
        content_frame.destroy()

    # Tạo content_frame mới
    content_frame = Frame(window, bg="white")
    content_frame.place(x=200, y=102, width=1070, height=555)

    # Gọi sales_form
    sales_form(content_frame, show_dashboard)
# --- QUAY LẠI DASHBOARD ---
def show_dashboard():
    content_frame.place_forget()
    for f in total_frames:
        f.place_forget()
    # Đặt lại vị trí
    emp_frame.place(x=400, y=125, height=170, width=280)
    sup_frame.place(x=800, y=125, height=170, width=280)
    cat_frame.place(x=400, y=310, height=170, width=280)
    prod_frame.place(x=800, y=310, height=170, width=280)
    sales_frame.place(x=600, y=495, height=170, width=280)
    update_totals()

# --- Cập nhật số liệu ---
def update_totals():
    cursor, conn = connect_database()
    if not cursor: return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT COUNT(*) FROM employee_data"); total_emp_count_label.config(text=str(cursor.fetchone()[0]))
        cursor.execute("SELECT COUNT(*) FROM tax_data"); total_sup_count_label.config(text=str(cursor.fetchone()[0]))
        cursor.execute("SELECT COUNT(*) FROM category_data"); total_cat_count_label.config(text=str(cursor.fetchone()[0]))
        cursor.execute("SELECT COUNT(*) FROM product_data"); total_prod_count_label.config(text=str(cursor.fetchone()[0]))
        cursor.execute("SELECT COUNT(*) FROM tax_data"); total_sales_count_label.config(text=str(cursor.fetchone()[0]))
    except Exception as e:
        messagebox.showerror("Error", f"Query Error: {e}")
    finally:
        conn.close()
    window.after(3000, update_totals)

update_totals()
window.mainloop()