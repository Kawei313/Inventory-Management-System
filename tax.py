# tax.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

tax_frame = None
tax_treeview = None
tax_rate_entry = None
current_tax_id = None

def create_tax_table():
    cursor, conn = connect_database()
    if not cursor: return
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tax_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tax_rate DECIMAL(5,2) NOT NULL,
                effective_date DATE DEFAULT (CURRENT_DATE)
            )
        """)
        conn.commit()
    except:
        pass
    finally:
        cursor.close()
        conn.close()

def load_taxes():
    global tax_treeview
    cursor, conn = connect_database()
    if not cursor: return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT id, tax_rate, effective_date FROM tax_data ORDER BY effective_date DESC")
        rows = cursor.fetchall()
        tax_treeview.delete(*tax_treeview.get_children())
        for row in rows:
            tax_treeview.insert("", END, values=(row[0], f"{row[1]:.2f}%", row[2]))
    except:
        pass
    finally:
        cursor.close()
        conn.close()

def select_tax(event):
    global current_tax_id
    selected = tax_treeview.focus()
    if not selected: return
    values = tax_treeview.item(selected, 'values')
    clear_form()
    tax_rate_entry.insert(0, values[1].replace("%", ""))
    current_tax_id = values[0]

def clear_form():
    global current_tax_id
    tax_rate_entry.delete(0, END)
    current_tax_id = None

def add_tax():
    rate = tax_rate_entry.get().strip()
    if not rate:
        messagebox.showerror("Lỗi", "Vui lòng nhập phần trăm thuế!")
        return
    try:
        rate_val = float(rate)
        if not (0 <= rate_val <= 100):
            raise ValueError
    except:
        messagebox.showerror("Lỗi", "Phần trăm phải từ 0 đến 100!")
        return

    cursor, conn = connect_database()
    if not cursor: return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("INSERT INTO tax_data (tax_rate) VALUES (%s)", (rate_val,))
        conn.commit()
        messagebox.showinfo("Thành công", f"Đã thêm thuế: {rate_val:.2f}%")
        load_taxes()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm: {e}")
    finally:
        cursor.close()
        conn.close()

def update_tax():
    global current_tax_id
    if not current_tax_id:
        messagebox.showerror("Lỗi", "Vui lòng chọn dòng để sửa!")
        return
    rate = tax_rate_entry.get().strip()
    if not rate:
        messagebox.showerror("Lỗi", "Vui lòng nhập phần trăm thuế!")
        return
    try:
        rate_val = float(rate)
        if not (0 <= rate_val <= 100):
            raise ValueError
    except:
        messagebox.showerror("Lỗi", "Phần trăm phải từ 0 đến 100!")
        return

    cursor, conn = connect_database()
    if not cursor: return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("UPDATE tax_data SET tax_rate=%s WHERE id=%s", (rate_val, current_tax_id))
        conn.commit()
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
        load_taxes()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
    finally:
        cursor.close()
        conn.close()

def tax_form(window):
    global tax_frame, tax_treeview, tax_rate_entry, current_tax_id
    current_tax_id = None

    tax_frame = Frame(window, bg="white")
    tax_frame.place(x=200, y=100, width=1070, height=567)

    Label(tax_frame, text="Quản Lý Thuế", font=("Times New Roman", 18, "bold"), bg="#0f4d7d", fg="white")\
        .place(x=0, y=0, relwidth=1, height=50)

    back_img = PhotoImage(file=r"helpers/icons/back_button.png")
    back_btn = Button(tax_frame, image=back_img, bd=0, bg="white", cursor="hand2",
                      command=tax_frame.place_forget)
    back_btn.image = back_img
    back_btn.place(x=10, y=5)

    cols = ("ID", "Phần Trăm Thuế", "Ngày Hiệu Lực")
    tax_treeview = ttk.Treeview(tax_frame, columns=cols, show="headings", height=15)
    for i, text in enumerate(["ID", "Phần Trăm Thuế", "Ngày Hiệu Lực"]):
        tax_treeview.heading(cols[i], text=text)
    tax_treeview.column("ID", width=100, anchor=CENTER)
    tax_treeview.column("Phần Trăm Thuế", width=200, anchor=CENTER)
    tax_treeview.column("Ngày Hiệu Lực", width=200, anchor=CENTER)
    tax_treeview.place(x=50, y=70, width=970, height=360)
    tax_treeview.bind("<<TreeviewSelect>>", select_tax)

    y = 450
    Label(tax_frame, text="Phần trăm thuế (%):", font=("Times New Roman", 14), bg="white").place(x=300, y=y)
    tax_rate_entry = Entry(tax_frame, font=("Times New Roman", 14), width=15, bg="lightyellow")
    tax_rate_entry.place(x=480, y=y)

    btn_y = 500
    Button(tax_frame, text="Thêm", width=12, font=("Times New Roman", 12), bg="#27AE60", fg="white", command=add_tax)\
        .place(x=400, y=btn_y)
    Button(tax_frame, text="Sửa", width=12, font=("Times New Roman", 12), bg="#2980B9", fg="white", command=update_tax)\
        .place(x=540, y=btn_y)
    Button(tax_frame, text="Làm mới", width=12, font=("Times New Roman", 12), bg="#95A5A6", fg="white", command=clear_form)\
        .place(x=680, y=btn_y)

    create_tax_table()
    load_taxes()