import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector  # <-- Thêm thư viện CSDL

# --- 1. CẤU HÌNH KẾT NỐI (SỬA TẠI ĐÂY) ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""  # <-- ĐIỀN MẬT KHẨU MYSQL CỦA BẠN VÀO ĐÂY
DB_NAME = "inventory_system"  # Tên CSDL của dự án


class Category:
    def __init__(self, root):
        self.root = root
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()

        self._setup_styles()
        self._build_ui()

        # --- THAY ĐỔI: Chuyển sang CSDL ---
        self._setup_database()  # Tự động tạo DB và Bảng
        self._load_data()  # Tải dữ liệu từ CSDL

    # -------------------- STYLE -------------------- #
    def _setup_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.map("Treeview", background=[('selected', '#0078D7')], foreground=[('selected', 'white')])

    # -------------------- UI (Giữ nguyên code của bạn) -------------------- #
    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root)
        main.grid(row=0, column=0, sticky="nsew")

        main.columnconfigure(0, weight=1, uniform="group")
        main.columnconfigure(1, weight=2, uniform="group")
        main.rowconfigure(0, weight=1)

        left = ttk.Frame(main, padding=20)
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        tk.Label(left, text="Ảnh minh họa\n(450x450)", font=("Arial", 16, "bold"),
                 bg="lightgray", fg="black", relief=tk.RIDGE, bd=2).grid(sticky="nsew")

        right = ttk.Frame(main, padding=20)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(3, weight=1)

        ttk.Label(right, text="QUẢN LÝ DANH MỤC SẢN PHẨM",
                  font=("Arial", 18, "bold")).grid(row=0, column=0, pady=10, sticky="n")

        self._build_form(right)
        self._build_buttons(right)
        self._build_table(right)

    def _build_form(self, parent):
        form = ttk.Frame(parent)
        form.grid(row=1, column=0, sticky="ew", pady=10)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Mã danh mục (ID)").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        ttk.Entry(form, textvariable=self.var_id, width=30).grid(row=0, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(form, text="Tên danh mục").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        ttk.Entry(form, textvariable=self.var_name, width=30).grid(row=1, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(form, text="Mô tả").grid(row=2, column=0, padx=5, pady=8, sticky="nw")
        self.txt_desc = tk.Text(form, font=("Arial", 12), height=4, bg="#f0f0f0", bd=0, relief=tk.FLAT)
        self.txt_desc.grid(row=2, column=1, padx=5, pady=8, sticky="ew")

    def _build_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=10)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        buttons = [
            ("➕ Thêm", "#4CAF50", "#45a049", self.add_category),
            ("📝 Cập nhật", "#FF9800", "#e68a00", self.update_category),
            ("🗑️ Xóa", "#F44336", "#d32f2f", self.delete_category),
            ("🔄 Làm mới", "#607D8B", "#546E7A", self.clear_form),
        ]

        for i, (text, bg, hover, cmd) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, font=("Arial", 12, "bold"),
                            bg=bg, fg="white", activebackground=hover,
                            relief=tk.RAISED, cursor="hand2", command=cmd)
            btn.grid(row=0, column=i, padx=5, pady=5, ipadx=8, ipady=5, sticky="ew")

            def on_enter(e, b=btn, h=hover): b.config(bg=h)

            def on_leave(e, b=btn, c=bg): b.config(bg=c)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def _build_table(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=3, column=0, sticky="nsew", pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        scrolly = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        self.tree = ttk.Treeview(frame, columns=("id", "name", "description"),
                                 yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.config(command=self.tree.yview)
        scrollx.config(command=self.tree.xview)
        scrolly.grid(row=0, column=1, sticky="ns")
        scrollx.grid(row=1, column=0, sticky="ew")
        self.tree.grid(row=0, column=0, sticky="nsew")

        for col, text, width in [("id", "ID", 80), ("name", "Tên danh mục", 160), ("description", "Mô tả", 280)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        self.tree["show"] = "headings"
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    # -------------------- LOGIC (ĐÃ NÂNG CẤP LÊN MYSQL) -------------------- #

    def _setup_database(self):
        """Tự động tạo CSDL và Bảng nếu chúng chưa tồn tại."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id INT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            """)
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi CSDL", f"Không thể thiết lập CSDL: {err}", parent=self.root)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def _load_data(self):
        """Lấy dữ liệu từ CSDL MySQL và hiển thị lên bảng"""
        self.tree.delete(*self.tree.get_children())
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM category")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    self.tree.insert('', tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {err}", parent=self.root)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def _get_form_data(self):
        return (
            self.var_id.get().strip(),
            self.var_name.get().strip(),
            self.txt_desc.get("1.0", tk.END).strip()
        )

    def _validate_form(self, id_val, name_val):
        if not id_val or not name_val:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Mã và Tên danh mục.", parent=self.root)
            return False
        if not id_val.isdigit():
            messagebox.showerror("Lỗi", "Mã danh mục phải là số nguyên.", parent=self.root)
            return False
        return True

    def add_category(self):
        id_val, name_val, desc_val = self._get_form_data()
        if not self._validate_form(id_val, name_val):
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM category WHERE id = %s", (id_val,))
            if cursor.fetchone():
                return messagebox.showerror("Lỗi", "Mã danh mục này đã tồn tại.", parent=self.root)

            query = "INSERT INTO category (id, name, description) VALUES (%s, %s, %s)"
            values = (int(id_val), name_val, desc_val)
            cursor.execute(query, values)

            conn.commit()
            self._load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã thêm danh mục mới.", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi thêm: {err}", parent=self.root)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update_category(self):
        id_val, name_val, desc_val = self._get_form_data()
        if not self._validate_form(id_val, name_val):
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            cursor = conn.cursor()

            query = "UPDATE category SET name = %s, description = %s WHERE id = %s"
            values = (name_val, desc_val, int(id_val))
            cursor.execute(query, values)

            conn.commit()
            if cursor.rowcount == 0:
                return messagebox.showerror("Lỗi", "Không tìm thấy mã danh mục để cập nhật.", parent=self.root)

            self._load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã cập nhật danh mục.", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật: {err}", parent=self.root)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def delete_category(self):
        id_val = self.var_id.get()
        if not id_val:
            return messagebox.showerror("Lỗi", "Vui lòng chọn danh mục để xóa.", parent=self.root)
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa danh mục này?", parent=self.root):
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            cursor = conn.cursor()

            query = "DELETE FROM category WHERE id = %s"
            cursor.execute(query, (int(id_val),))

            conn.commit()
            if cursor.rowcount == 0:
                return messagebox.showerror("Lỗi", "Không tìm thấy mã danh mục để xóa.", parent=self.root)

            self._load_data()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa danh mục.", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa: {err}", parent=self.root)
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.txt_desc.delete("1.0", tk.END)
        if self.tree.selection():  # Chỉ bỏ chọn nếu có mục đang được chọn
            self.tree.selection_remove(self.tree.selection())
        self.root.focus()

    def _on_select(self, _):
        selected = self.tree.focus()
        if not selected: return
        row = self.tree.item(selected)['values']
        if not row: return

        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.txt_desc.delete("1.0", tk.END)
        self.txt_desc.insert("1.0", str(row[2]))


# -------------------- CHẠY -------------------- #
if __name__ == "__main__":
    """
    Phần này dùng để chạy thử file category.py một cách độc lập.
    Khi bạn import file này vào dự án chính, đoạn mã này sẽ không chạy.
    """
    root = tk.Tk()
    root.title("Quản lý Danh mục (Responsive UI - Phiên bản MySQL)")
    root.geometry("1200x700+50+50")
    root.minsize(900, 600)
    root.configure(bg="white")

    app = Category(root)  # Khởi tạo Lớp

    root.mainloop()