# category.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

category_frame = None
category_treeview = None
id_entry = None
name_entry = None
description_text = None


def create_category_table():
    """Tạo bảng category nếu chưa tồn tại"""
    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT
            )
        """)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo bảng: {e}")
    finally:
        cursor.close()
        conn.close()


def treeview_data():
    """Load dữ liệu từ database lên treeview"""
    global category_treeview
    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM category ORDER BY id")
        rows = cursor.fetchall()
        category_treeview.delete(*category_treeview.get_children())
        for row in rows:
            category_treeview.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
    finally:
        cursor.close()
        conn.close()


def select_data(event):
    """Chọn dữ liệu từ treeview để hiển thị lên form"""
    selected = category_treeview.focus()
    if not selected:
        return
    values = category_treeview.item(selected, 'values')
    if not values:
        return

    clear_fields(False)
    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    description_text.insert(1.0, values[2] if values[2] else "")


def clear_fields(clear_selection=True):
    """Xóa các trường nhập liệu"""
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    description_text.delete(1.0, END)
    if clear_selection and category_treeview.selection():
        category_treeview.selection_remove(category_treeview.selection())


def add_category():
    """Thêm danh mục mới"""
    cat_id = id_entry.get().strip()
    cat_name = name_entry.get().strip()
    cat_desc = description_text.get(1.0, END).strip()

    if not cat_id or not cat_name:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ ID và Tên danh mục!")
        return

    try:
        cat_id = int(cat_id)
    except ValueError:
        messagebox.showerror("Lỗi", "ID phải là số nguyên!")
        return

    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM category WHERE id=%s", (cat_id,))
        if cursor.fetchone():
            messagebox.showerror("Lỗi", "ID này đã tồn tại!")
            return

        cursor.execute("INSERT INTO category (id, name, description) VALUES (%s, %s, %s)",
                       (cat_id, cat_name, cat_desc))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")
        treeview_data()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm: {e}")
    finally:
        cursor.close()
        conn.close()


def update_category():
    """Cập nhật danh mục"""
    selected = category_treeview.selection()
    if not selected:
        messagebox.showerror("Lỗi", "Vui lòng chọn danh mục để cập nhật!")
        return

    cat_id = id_entry.get().strip()
    cat_name = name_entry.get().strip()
    cat_desc = description_text.get(1.0, END).strip()

    if not cat_id or not cat_name:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ ID và Tên danh mục!")
        return

    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM category WHERE id=%s", (cat_id,))
        current_data = cursor.fetchone()
        if not current_data:
            messagebox.showerror("Lỗi", "Không tìm thấy danh mục!")
            return

        current_data = current_data[1:]
        new_data = (cat_name, cat_desc)

        if current_data == new_data:
            messagebox.showinfo("Thông báo", "Không có thay đổi nào!")
            return

        cursor.execute("UPDATE category SET name=%s, description=%s WHERE id=%s",
                       (cat_name, cat_desc, cat_id))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
        treeview_data()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_category():
    """Xóa danh mục"""
    selected = category_treeview.selection()
    if not selected:
        messagebox.showerror("Lỗi", "Vui lòng chọn danh mục để xóa!")
        return

    cat_id = id_entry.get().strip()
    if not cat_id:
        messagebox.showerror("Lỗi", "Không có ID để xóa!")
        return

    result = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa danh mục này?")
    if not result:
        return

    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("DELETE FROM category WHERE id=%s", (cat_id,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Lỗi", "Không tìm thấy danh mục để xóa!")
            return

        messagebox.showinfo("Thành công", "Đã xóa danh mục!")
        treeview_data()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa: {e}")
    finally:
        cursor.close()
        conn.close()


def search_category(search_value):
    """Tìm kiếm danh mục theo ID"""
    if not search_value:
        messagebox.showerror("Lỗi", "Vui lòng nhập ID để tìm kiếm!")
        return

    cursor, conn = connect_database()
    if not cursor:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM category WHERE id=%s", (search_value,))
        record = cursor.fetchone()

        if not record:
            messagebox.showerror("Lỗi", "Không tìm thấy danh mục!")
            return

        category_treeview.delete(*category_treeview.get_children())
        category_treeview.insert("", END, values=record)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")
    finally:
        cursor.close()
        conn.close()


def show_all(search_entry):
    """Hiển thị tất cả danh mục"""
    treeview_data()
    search_entry.delete(0, END)


def category_form(window):
    """Tạo form quản lý danh mục"""
    global category_frame, category_treeview, id_entry, name_entry, description_text

    category_frame = Frame(window, width=1070, height=567, bg="white")
    category_frame.place(x=200, y=100)

    # Header
    heading_label = Label(category_frame, text="Manage Category Details",
                          font=("Times New Roman", 16, "bold"),
                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)

    # Back button
    back_image = PhotoImage(file=r"helpers/icons/back_button.png")
    back_button = Button(category_frame, image=back_image, cursor="hand2",
                         bd=0, bg="white",
                         command=lambda: category_frame.place_forget())
    back_button.image = back_image
    back_button.place(x=10, y=30)

    # Left Frame - Form nhập liệu
    left_frame = Frame(category_frame, bg="white")
    left_frame.place(x=10, y=100)

    Label(left_frame, text="Id", font=("Times New Roman", 14, "bold"),
          bg="white").grid(row=0, column=0, padx=(20, 40), sticky="w")
    id_entry = Entry(left_frame, font=("Times New Roman", 14, "bold"),
                     bg="lightyellow")
    id_entry.grid(row=0, column=1, sticky="w")

    Label(left_frame, text="Category Name", font=("Times New Roman", 14, "bold"),
          bg="white").grid(row=1, column=0, padx=(20, 40), pady=20, sticky="w")
    name_entry = Entry(left_frame, font=("Times New Roman", 14, "bold"),
                       bg="lightyellow")
    name_entry.grid(row=1, column=1, sticky="w")

    Label(left_frame, text="Description", font=("Times New Roman", 14, "bold"),
          bg="white").grid(row=2, column=0, padx=(20, 40), pady=25, sticky="nw")
    description_text = Text(left_frame, width=25, height=6, bd=2)
    description_text.grid(row=2, column=1, sticky="w")

    # Button Frame
    button_frame = Frame(left_frame, bg="white")
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)

    Button(button_frame, text="Add", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=add_category).grid(row=0, column=0, padx=20)

    Button(button_frame, text="Update", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=update_category).grid(row=0, column=1, padx=20)

    Button(button_frame, text="Delete", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=delete_category).grid(row=0, column=2, padx=20)

    Button(button_frame, text="Clear", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=lambda: clear_fields(True)).grid(row=0, column=3, padx=20)

    # Right Frame - Treeview
    right_frame = Frame(category_frame, bg="white")
    right_frame.place(x=520, y=95, width=500, height=450)

    # Search Frame
    search_frame = Frame(right_frame)
    search_frame.pack(pady=(0, 20))

    Label(search_frame, text="Id", font=("Times New Roman", 14, "bold"),
          bg="white").grid(row=0, column=0, padx=(0, 15), sticky="w")
    search_entry = Entry(search_frame, font=("Times New Roman", 14, "bold"),
                         bg="lightyellow", width=12)
    search_entry.grid(row=0, column=1, sticky="w")

    Button(search_frame, text="Search", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=lambda: search_category(search_entry.get())).grid(row=0, column=2, padx=20)

    Button(search_frame, text="Show All", font=("Times New Roman", 14),
           width=8, cursor="hand2", fg="white", bg="#0f4d7d",
           command=lambda: show_all(search_entry)).grid(row=0, column=3)

    # Treeview
    category_treeview = ttk.Treeview(right_frame,
                                     columns=("id", "name", "description"),
                                     show="headings")
    category_treeview.pack(fill=BOTH, expand=True)

    category_treeview.heading("id", text="ID")
    category_treeview.heading("name", text="Category Name")
    category_treeview.heading("description", text="Description")

    category_treeview.column("id", width=80)
    category_treeview.column("name", width=160)
    category_treeview.column("description", width=300)

    # Scrollbar
    x_scroll = ttk.Scrollbar(right_frame, orient=HORIZONTAL,
                             command=category_treeview.xview)
    category_treeview.configure(xscrollcommand=x_scroll.set)
    x_scroll.pack(side=BOTTOM, fill=X)

    # Ngăn resize cột
    category_treeview.bind('<Button-1>',
                           lambda e: 'break' if category_treeview.identify_region(e.x, e.y) == "separator" else None)

    # Bind select event
    category_treeview.bind("<ButtonRelease-1>", select_data)

    # Tạo bảng và load dữ liệu
    create_category_table()
    treeview_data()