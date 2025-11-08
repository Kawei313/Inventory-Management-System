import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# ================== KẾT NỐI DATABASE ==================
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # 🔹 Tài khoản MySQL
            password="123456",    # 🔹 Mật khẩu MySQL
            database="inventory_system"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Lỗi kết nối MySQL:\n{e}")
        return None


# ================== MỞ GIAO DIỆN USER ==================
def open_user_window(name, root):
    root.destroy()  # Đóng cửa sổ login
    import user_dashboard
    user_dashboard.open_user_dashboard(name)


# ================== HÀM ĐĂNG NHẬP ==================
def login(root, employee_entry, password_entry):
    emp_id = employee_entry.get()
    password = password_entry.get()

    if emp_id == "" or password == "":
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ Employee ID và Password!")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT name, usertype FROM employee_data WHERE empid=%s AND password=%s"
        cursor.execute(query, (emp_id, password))
        result = cursor.fetchone()

        if result:
            name, usertype = result
            messagebox.showinfo("Đăng nhập thành công", f"Xin chào {name} ({usertype})!")

            if usertype.lower() == "admin":
                root.destroy()
                import subprocess, sys, os
                python_exec = sys.executable
                subprocess.Popen([python_exec, os.path.join(os.path.dirname(__file__), "dashboard.py")])

            else:
                open_user_window(name, root)
        else:
            messagebox.showerror("Thất bại", "Sai Employee ID hoặc Password!")

        cursor.close()
        conn.close()


# ================== GIAO DIỆN LOGIN ==================
def open_login_window():
    root = tk.Tk()
    root.title("Login - Inventory Management System")
    root.geometry("900x550")
    root.configure(bg="white")

    # Thanh tiêu đề
    title_frame = tk.Frame(root, bg="#4A90E2", height=60)
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="Inventory Management System",
             bg="#4A90E2", fg="white", font=("Helvetica", 22, "bold")).pack(pady=10)

    # Khung trái (hình minh họa)
    left_frame = tk.Frame(root, bg="white", width=500, height=400)
    left_frame.place(x=40, y=120)
    try:
        img = Image.open("Background_log.png")
        img = img.resize((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        tk.Label(left_frame, image=img_tk, bg="white").pack()
        # giữ tham chiếu ảnh
        left_frame.image = img_tk
    except:
        tk.Label(left_frame, text="(Minh họa công việc nhóm)", bg="white",
                 fg="gray", font=("Arial", 12, "italic")).pack(pady=100)

    # Khung phải (form login)
    login_frame = tk.Frame(root, bg="#f0f0f0", width=320, height=400)
    login_frame.place(x=550, y=120)

    # Avatar
    try:
        avatar = Image.open("Avartar.png")
        avatar = avatar.resize((100, 100))
        avatar_tk = ImageTk.PhotoImage(avatar)
        tk.Label(login_frame, image=avatar_tk, bg="#f0f0f0").place(x=110, y=20)
        login_frame.image = avatar_tk
    except:
        tk.Label(login_frame, text="🙂", font=("Arial", 50), bg="#f0f0f0").place(x=130, y=25)

    # Các trường nhập
    tk.Label(login_frame, text="Employee Id", bg="#f0f0f0", font=("Arial", 11)).place(x=40, y=150)
    employee_entry = tk.Entry(login_frame, width=30)
    employee_entry.place(x=40, y=175)

    tk.Label(login_frame, text="Password", bg="#f0f0f0", font=("Arial", 11)).place(x=40, y=210)
    password_entry = tk.Entry(login_frame, width=30, show="*")
    password_entry.place(x=40, y=235)

    # Quên mật khẩu
    tk.Label(login_frame, text="Forgot Password?", fg="#4A90E2", bg="#f0f0f0",
             font=("Arial", 9, "underline"), cursor="hand2").place(x=180, y=265)

    # Nút đăng nhập
    tk.Button(login_frame, text="Login", bg="#4A90E2", fg="white",
              font=("Arial", 11, "bold"), width=20,
              command=lambda: login(root, employee_entry, password_entry)).place(x=60, y=300)

    root.mainloop()


# ================== CHẠY CHÍNH ==================
if __name__ == "__main__":
    open_login_window()
