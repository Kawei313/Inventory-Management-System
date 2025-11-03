from tkinter import *
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

def _get_db():
    # import lazy để tránh circular import với employees/dashboard
    try:
        from employees import connect_database
        return connect_database
    except Exception:
        return None

def create_product_table():
    # tạo database/bảng product_data nếu chưa có và đảm bảo cột description tồn tại
    connect_database = _get_db()
    if not connect_database:
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        # tạo bảng bao gồm cột description (an toàn nếu đã tồn tại)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100),
                supplier VARCHAR(100),
                name VARCHAR(100),
                price DECIMAL(10,2),
                quantity INT,
                status VARCHAR(50),
                description TEXT
            )
        """)
        # kiểm tra và thêm cột description nếu DB cũ thiếu
        try:
            cursor.execute("SHOW COLUMNS FROM product_data LIKE 'description'")
            if not cursor.fetchall():
                cursor.execute("ALTER TABLE product_data ADD COLUMN description TEXT")
        except Exception:
            # nếu không có quyền ALTER thì bỏ qua, người dùng có thể thêm thủ công
            pass
        conn.commit()
    except Exception as e:
        messagebox.showerror("Lỗi DB", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def _nap_du_lieu_comboboxes(cat_cb, sup_cb):
    # nạp danh mục và nhà cung cấp từ DB; nếu không có DB dùng giá trị mặc định
    connect_database = _get_db()
    if not connect_database:
        cat_cb['values'] = ["Điện tử", "Thực phẩm", "Văn phòng phẩm"]
        sup_cb['values'] = []
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        cat_cb['values'] = ["Điện tử", "Thực phẩm", "Văn phòng phẩm"]
        sup_cb['values'] = []
        return
    try:
        cursor.execute("USE inventory_system")
        try:
            cursor.execute("SELECT name FROM category_data")
            cats = [r[0] for r in cursor.fetchall()] or ["Điện tử", "Thực phẩm", "Văn phòng phẩm"]
        except Exception:
            cats = ["Điện tử", "Thực phẩm", "Văn phòng phẩm"]
        try:
            cursor.execute("SELECT name FROM supplier_data")
            sups = [r[0] for r in cursor.fetchall()] or []
        except Exception:
            sups = []
        cat_cb['values'] = cats
        sup_cb['values'] = sups
    except Exception:
        cat_cb['values'] = ["Điện tử", "Thực phẩm", "Văn phòng phẩm"]
        sup_cb['values'] = []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def treeview_data(treeview):
    # nạp dữ liệu sản phẩm vào treeview
    connect_database = _get_db()
    if not connect_database:
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT id, category, supplier, name, price, quantity, status FROM product_data ORDER BY id")
        rows = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for r in rows:
            pid, cat, sup, name, price, qty, status = r
            price_str = f"{price:.2f}" if isinstance(price, (float, Decimal)) else str(price)
            treeview.insert('', END, values=(pid, cat, sup, name, price_str, str(qty), status))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def add_product(category, supplier, name, price, quantity, status, description, treeview):
    # thêm sản phẩm mới (validate giá và số lượng)
    if not name.strip() or not price.strip() or not quantity.strip():
        messagebox.showerror("Lỗi", "Name, Price and Quantity are required")
        return
    try:
        price_val = Decimal(price.strip())
        quantity_val = int(quantity.strip())
    except (InvalidOperation, ValueError):
        messagebox.showerror("Lỗi", "Price phải là số và Quantity phải là số nguyên")
        return
    connect_database = _get_db()
    if not connect_database:
        messagebox.showerror("Lỗi", "DB connector không khả dụng")
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute(
            "INSERT INTO product_data (category, supplier, name, price, quantity, status, description) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (category.strip(), supplier.strip(), name.strip(), float(price_val), quantity_val, status.strip(), description.strip())
        )
        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def update_product(pid, category, supplier, name, price, quantity, status, description, treeview):
    # cập nhật sản phẩm đã chọn
    if not pid:
        messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để cập nhật")
        return
    try:
        price_val = Decimal(price.strip())
        quantity_val = int(quantity.strip())
    except (InvalidOperation, ValueError):
        messagebox.showerror("Lỗi", "Price phải là số và Quantity phải là số nguyên")
        return
    connect_database = _get_db()
    if not connect_database:
        messagebox.showerror("Lỗi", "DB connector không khả dụng")
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute(
            "UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, quantity=%s, status=%s, description=%s WHERE id=%s",
            (category.strip(), supplier.strip(), name.strip(), float(price_val), quantity_val, status.strip(), description.strip(), pid)
        )
        conn.commit()
        messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def delete_product(pid, treeview):
    # xóa sản phẩm đã chọn
    if not pid:
        messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa")
        return
    if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sản phẩm này?"):
        return
    connect_database = _get_db()
    if not connect_database:
        messagebox.showerror("Lỗi", "DB connector không khả dụng")
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("USE inventory_system")
        cursor.execute("DELETE FROM product_data WHERE id=%s", (pid,))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã xóa sản phẩm")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def search_product(option, value, treeview):
    # tìm kiếm theo tên/danh mục/nhà cung cấp
    if not value.strip():
        messagebox.showerror("Lỗi", "Nhập nội dung tìm kiếm")
        return
    if option not in ("name", "category", "supplier"):
        messagebox.showerror("Lỗi", "Tùy chọn tìm kiếm không hợp lệ")
        return
    connect_database = _get_db()
    if not connect_database:
        messagebox.showerror("Lỗi", "DB connector không khả dụng")
        return
    cursor, conn = connect_database()
    if not cursor or not conn:
        return
    try:
        cursor.execute("USE inventory_system")
        q = f"SELECT id, category, supplier, name, price, quantity, status FROM product_data WHERE {option} LIKE %s"
        cursor.execute(q, (f"%{value}%",))
        rows = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for r in rows:
            pid, cat, sup, name, price, qty, status = r
            price_str = f"{price:.2f}" if isinstance(price, (float, Decimal)) else str(price)
            treeview.insert('', END, values=(pid, cat, sup, name, price_str, str(qty), status))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def product_form(root):
    # hiển thị form quản lý sản phẩm trong dashboard (không tạo cửa sổ mới)
    create_product_table()
    if getattr(root, "_product_frame", None):
        root._product_frame.lift()
        return

    frame = Frame(root, bd=2, relief=RIDGE, bg="#ffffff")
    frame.place(x=200, y=102, width=1070, height=555)
    root._product_frame = frame

    header = Frame(frame, bg="#0b5377")
    header.place(x=0, y=0, relwidth=1, height=48)
    back_btn = Button(header, text="← Back", font=("Times New Roman", 12, "bold"), bg="white", relief=GROOVE,
                      command=lambda: _close_product_frame(root))
    back_btn.place(x=8, y=6, width=80, height=34)
    Label(header, text="Manage Product Details", font=("Times New Roman", 16, "bold"), bg="#0b5377", fg="white").place(x=110, y=10)

    # khung bên phải: tìm kiếm + danh sách
    right = Frame(frame, bg="#ffffff", bd=1, relief=FLAT)
    right.place(x=684, y=56, width=374, height=490)
    Label(right, text="Search Product", font=("Times New Roman", 12, "bold"), bg="#ffffff").pack(anchor="nw", pady=(8,2))

    # product_tree sẽ gán sau; lambdas tham chiếu biến này khi thực thi
    product_tree = None

    # khung tìm kiếm dùng grid để giữ kích thước nút ổn định
    search_frame = Frame(right, bg="#ffffff")
    search_frame.pack(fill=X, padx=6, pady=2)

    search_opt = ttk.Combobox(search_frame, values=["supplier", "name", "category"], width=12, state="readonly")
    search_opt.set("supplier")
    search_opt.grid(row=0, column=0, padx=(0,6), pady=2, sticky=W)

    search_val = Entry(search_frame)
    search_val.grid(row=0, column=1, padx=(0,6), pady=2, sticky=EW)

    search_btn_font = ("Times New Roman", 10)
    Button(search_frame, text="Search", width=10, font=search_btn_font,
           command=lambda: search_product(search_opt.get(), search_val.get(), product_tree)).grid(row=0, column=2, padx=(0,6), pady=2)
    Button(search_frame, text="Show All", width=12, font=search_btn_font,
           command=lambda: treeview_data(product_tree)).grid(row=0, column=3, padx=(0,0), pady=2)

    search_frame.grid_columnconfigure(1, weight=1)

    # khung chứa treeview + thanh cuộn (cả ngang và dọc)
    tv_frame = Frame(right)
    tv_frame.pack(fill=BOTH, expand=True, padx=6, pady=(6,8))

    # thanh cuộn ngang và dọc
    h_scroll = Scrollbar(tv_frame, orient=HORIZONTAL)
    v_scroll = Scrollbar(tv_frame, orient=VERTICAL)

    cols = ("Id","Category","Supplier","Name","Price","Quantity","Status")
    product_tree = ttk.Treeview(tv_frame, columns=cols, show="headings", height=18,
                                xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    # cấu hình header và kích thước cột (tăng width Name để cần cuộn nếu quá dài)
    for c in cols:
        product_tree.heading(c, text=c)
        if c == "Name":
            product_tree.column(c, width=220, anchor=CENTER)
        elif c == "Category":
            product_tree.column(c, width=120, anchor=CENTER)
        elif c == "Supplier":
            product_tree.column(c, width=140, anchor=CENTER)
        elif c == "Price":
            product_tree.column(c, width=100, anchor=CENTER)
        else:
            product_tree.column(c, width=80, anchor=CENTER)

    # đặt vị trí các widget trong tv_frame
    h_scroll.pack(side=BOTTOM, fill=X)
    v_scroll.pack(side=RIGHT, fill=Y)
    product_tree.pack(fill=BOTH, expand=True, side=LEFT)

    # nối command cho scrollbar
    h_scroll.config(command=product_tree.xview)
    v_scroll.config(command=product_tree.yview)

    # khung bên trái: form nhập liệu
    left = Frame(frame, bg="#f5f5f5", bd=1, relief=FLAT)
    left.place(x=12, y=56, width=660, height=490)

    lbl_font = ("Times New Roman", 12)
    lbl_x = 18
    entry_x = 220
    gap = 46
    y0 = 18

    Label(left, text="Category", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0)
    # combobox cho phép gõ (state normal) hoặc chọn từ danh sách đã nạp
    cat_cb = ttk.Combobox(left, values=[], state="normal", width=28)
    cat_cb.place(x=entry_x, y=y0-4)

    Label(left, text="Supplier", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap)
    sup_cb = ttk.Combobox(left, values=[], state="normal", width=28)
    sup_cb.place(x=entry_x, y=y0+gap-4)

    Label(left, text="Name", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap*2)
    name_e = Entry(left, width=30)
    name_e.place(x=entry_x, y=y0+gap*2-4)

    Label(left, text="Price", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap*3)
    price_e = Entry(left, width=30)
    price_e.place(x=entry_x, y=y0+gap*3-4)

    Label(left, text="Quantity", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap*4)
    qty_e = Entry(left, width=30)
    qty_e.place(x=entry_x, y=y0+gap*4-4)

    Label(left, text="Status", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap*5)
    status_cb = ttk.Combobox(left, values=["In Stock","Low Stock","Out of Stock","Active","Inactive"], state="readonly", width=28)
    status_cb.place(x=entry_x, y=y0+gap*5-4)
    status_cb.set("In Stock")

    Label(left, text="Description", font=lbl_font, bg="#f5f5f5").place(x=lbl_x, y=y0+gap*6)
    desc_txt = Text(left, width=46, height=5)
    desc_txt.place(x=entry_x, y=y0+gap*6-6)

    # nạp giá trị combobox từ DB
    _nap_du_lieu_comboboxes(cat_cb, sup_cb)

    # khi chọn item ở treeview sẽ điền dữ liệu vào form
    selected = {"id": None}
    def on_select(e):
        sel = product_tree.focus()
        if not sel:
            return
        vals = product_tree.item(sel, "values")
        selected["id"] = vals[0]
        cat_cb.set(vals[1])
        sup_cb.set(vals[2])
        name_e.delete(0, END); name_e.insert(0, vals[3])
        price_e.delete(0, END); price_e.insert(0, vals[4])
        qty_e.delete(0, END); qty_e.insert(0, vals[5])
        status_cb.set(vals[6])
        # nạp description từ DB (an toàn): cố gắng lấy description cho id
        try:
            connect_database = _get_db()
            if connect_database:
                c, conn = connect_database()
                if c and conn:
                    c.execute("USE inventory_system")
                    c.execute("SELECT description FROM product_data WHERE id=%s", (vals[0],))
                    row = c.fetchone()
                    desc_txt.delete("1.0", END)
                    if row and row[0]:
                        desc_txt.insert(END, row[0])
                    c.close(); conn.close()
        except Exception:
            pass

    product_tree.bind("<<TreeviewSelect>>", on_select)

    # nút thao tác; Clear sẽ reset combobox và các trường
    btn_font = ("Times New Roman", 10, "bold")
    btn_fg = "#0b5377"
    Button(left, text="Add", width=10, fg=btn_fg, font=btn_font,
           command=lambda: add_product(cat_cb.get(), sup_cb.get(), name_e.get(), price_e.get(), qty_e.get(), status_cb.get(), desc_txt.get("1.0","end"), product_tree)).place(x=60, y=410)
    Button(left, text="Update", width=10, fg=btn_fg, font=btn_font,
           command=lambda: update_product(selected["id"], cat_cb.get(), sup_cb.get(), name_e.get(), price_e.get(), qty_e.get(), status_cb.get(), desc_txt.get("1.0","end"), product_tree)).place(x=190, y=410)
    Button(left, text="Delete", width=10, fg=btn_fg, font=btn_font,
           command=lambda: delete_product(selected["id"], product_tree)).place(x=320, y=410)
    Button(left, text="Clear", width=10, fg=btn_fg, font=btn_font,
           command=lambda: [
               cat_cb.set(''),
               sup_cb.set(''),
               name_e.delete(0,END),
               price_e.delete(0,END),
               qty_e.delete(0,END),
               status_cb.set('In Stock'),
               desc_txt.delete("1.0","end")
           ]).place(x=450, y=410)

    # nạp dữ liệu ban đầu
    treeview_data(product_tree)

def _close_product_frame(root):
    # đóng khung quản lý sản phẩm
    f = getattr(root, "_product_frame", None)
    if f:
        try:
            f.destroy()
        except:
            pass
        root._product_frame = None