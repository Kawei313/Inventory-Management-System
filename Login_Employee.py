import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import os
import mysql.connector
from mysql.connector import Error


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1e3a5f")

        # DB + Data
        self.connection = self.connect_to_db()
        self.products = self.load_products_from_db()
        self.cart = []
        self.bill_no = None
        self.customer_name = ""
        self.customer_contact = ""
        self.bill_text = ""

        # Giao diện
        self.create_header()
        self.create_main_layout()

    # ================================================
    # 1. KẾT NỐI DB
    # ================================================
    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='inventory_system',
                user='root',          # THAY USER CỦA BẠN
                password='123456'   # THAY PASSWORD
            )
            if conn.is_connected():
                print("Kết nối MySQL thành công!")
            return conn
        except Error as e:
            messagebox.showerror("DB Error", f"Không kết nối được DB:\n{e}")
            return None

    # ================================================
    # 2. LẤY SẢN PHẨM (KHÔNG CÓ discount)
    # ================================================
    def load_products_from_db(self):
        if not self.connection or not self.connection.is_connected():
            return []

        try:
            cur = self.connection.cursor(dictionary=True)
            sql = """
                SELECT id, name, price
                FROM product_data 
                WHERE status = 'In Stock'
                ORDER BY name
            """
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            for r in rows:
                r['price'] = float(r['price'])
                r['discount'] = 0  # Không có discount ở đây
            return rows
        except Error as e:
            messagebox.showerror("Query Error", f"Lỗi lấy sản phẩm:\n{e}")
            return []

    # ================================================
    # 3. HEADER
    # ================================================
    def create_header(self):
        header = tk.Frame(self.root, bg="#1e3a5f", height=100)
        header.pack(fill=tk.X, padx=10, pady=5)
        header.pack_propagate(False)

        tk.Label(header, text="Inventory Management System",
                 font=("Arial", 32, "bold"), bg="#1e3a5f", fg="white").pack(side=tk.LEFT, padx=20)

        tk.Button(header, text="Logout", font=("Arial", 16, "bold"),
                  bg="#4a90d9", fg="white", padx=20, pady=5).pack(side=tk.RIGHT, padx=20)

        info = tk.Frame(self.root, bg="#5a7a9f", height=40)
        info.pack(fill=tk.X, padx=10)
        info.pack_propagate(False)

        tk.Label(info, text="Welcome Jane Smith", font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=20, pady=5)

        tk.Label(info, text=datetime.now().strftime("Date: %d/%m/%Y"),
                 font=("Arial", 12), bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)
        tk.Label(info, text=datetime.now().strftime("Time: %I:%M %p"),
                 font=("Arial", 12), bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)

    # ================================================
    # 4. MAIN LAYOUT
    # ================================================
    def create_main_layout(self):
        main = tk.Frame(self.root, bg="white")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        paned1 = tk.PanedWindow(main, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        paned1.pack(fill=tk.BOTH, expand=True)

        # LEFT: Products
        left = tk.Frame(paned1, bg="white", relief=tk.RIDGE, bd=2)
        paned1.add(left)
        paned1.paneconfigure(left, stretch="always")
        self.create_products_panel(left)

        # RIGHT: Middle + Billing
        right = tk.Frame(paned1, bg="white")
        paned1.add(right)
        paned1.paneconfigure(right, stretch="always")

        paned2 = tk.PanedWindow(right, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        paned2.pack(fill=tk.BOTH, expand=True)

        middle = tk.Frame(paned2, bg="white")
        paned2.add(middle)
        paned2.paneconfigure(middle, stretch="always")
        self.create_middle_panel(middle)

        billing = tk.Frame(paned2, bg="#f0f0c8", relief=tk.RIDGE, bd=2)
        paned2.add(billing)
        paned2.paneconfigure(billing, stretch="always")
        self.create_billing_panel(billing)

    # ================================================
    # 5. PRODUCTS PANEL
    # ================================================
    def create_products_panel(self, parent):
        tk.Label(parent, text="All Products", font=("Arial", 16, "bold"),
                 bg="#1e3a5f", fg="white", pady=10).pack(fill=tk.X)

        sframe = tk.Frame(parent, bg="white")
        sframe.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(sframe, text="Product Name", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(sframe, font=("Arial", 12), width=15)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(sframe, text="Search", bg="#1e3a5f", fg="white", command=self.search_product).pack(side=tk.LEFT, padx=5)
        tk.Button(sframe, text="Show All", bg="#1e3a5f", fg="white", command=self.show_all_products).pack(side=tk.LEFT, padx=5)

        tree_fr = tk.Frame(parent)
        tree_fr.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        vsb = ttk.Scrollbar(tree_fr, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_fr, orient=tk.HORIZONTAL)

        self.products_tree = ttk.Treeview(tree_fr, columns=("ID", "Name", "Price"),
                                          show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=20)
        self.products_tree.pack(fill=tk.BOTH, expand=True)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        vsb.config(command=self.products_tree.yview)
        hsb.config(command=self.products_tree.xview)

        for col, w in zip(("ID", "Name", "Price"), (40, 160, 100)):
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=w, anchor=tk.CENTER)

        self.load_products()
        self.products_tree.bind("<<TreeviewSelect>>", self.on_product_select)

    def load_products(self):
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        for p in self.products:
            self.products_tree.insert("", tk.END, values=(p["id"], p["name"], f"₹{p['price']:.2f}"))

    def search_product(self):
        term = self.search_entry.get().strip().lower()
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        for p in self.products:
            if term in p["name"].lower():
                self.products_tree.insert("", tk.END, values=(p["id"], p["name"], f"₹{p['price']:.2f}"))

    def show_all_products(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()

    def on_product_select(self, event):
        sel = self.products_tree.selection()
        if not sel: return
        item = self.products_tree.item(sel[0])
        name = item['values'][1]
        price = float(item['values'][2].replace("₹", "").replace(",", ""))

        self.product_name_entry.config(state="normal")
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.insert(0, name)
        self.product_name_entry.config(state="readonly")

        self.price_entry.config(state="normal")
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, price)
        self.price_entry.config(state="readonly")

        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")

    # ================================================
    # 6. MIDDLE PANEL
    # ================================================
    def create_middle_panel(self, parent):
        # Customer
        cust = tk.LabelFrame(parent, text="Customer Details", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        cust.pack(fill=tk.X, padx=5, pady=5)
        f = tk.Frame(cust, bg="white")
        f.pack(padx=10, pady=10)
        tk.Label(f, text="Name", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(f, font=("Arial", 11), width=18)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(f, text="Contact No.", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.contact_entry = tk.Entry(f, font=("Arial", 11), width=18)
        self.contact_entry.grid(row=0, column=3, padx=5, pady=5)

        # Calculator + Cart
        cc = tk.Frame(parent, bg="white")
        cc.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Calculator
        calc = tk.LabelFrame(cc, text="Calculator", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        calc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        self.calc_display = tk.Entry(calc, font=("Arial", 18, "bold"), justify=tk.RIGHT, bd=5, relief=tk.SUNKEN)
        self.calc_display.pack(fill=tk.X, padx=8, pady=8)
        self.calc_display.insert(0, "0")
        btns = [['7', '8', '9', '+'], ['4', '5', '6', '-'], ['1', '2', '3', '*'], ['Ans', 'Clear', '0', '/']]
        bf = tk.Frame(calc, bg="white")
        bf.pack(padx=8, pady=5)
        for r, row in enumerate(btns):
            for c, txt in enumerate(row):
                tk.Button(bf, text=txt, font=("Arial", 14), width=6, height=2,
                          command=lambda x=txt: self.calc_click(x)).grid(row=r, column=c, padx=2, pady=2)

        # Cart
        cart = tk.LabelFrame(cc, text="My Cart  Total: 0", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        cart.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=3)
        self.cart_total_label = tk.Label(cart, text="Total Products: 0", font=("Arial", 10), bg="white")
        self.cart_total_label.pack(anchor=tk.E, padx=5)
        ctree_fr = tk.Frame(cart)
        ctree_fr.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        cvsb = ttk.Scrollbar(ctree_fr, orient=tk.VERTICAL)
        chsb = ttk.Scrollbar(ctree_fr, orient=tk.HORIZONTAL)
        self.cart_tree = ttk.Treeview(ctree_fr, columns=("ID", "Name", "Price"), show="headings", height=8,
                                      yscrollcommand=cvsb.set, xscrollcommand=chsb.set)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        cvsb.pack(side=tk.RIGHT, fill=tk.Y)
        chsb.pack(side=tk.BOTTOM, fill=tk.X)
        cvsb.config(command=self.cart_tree.yview)
        chsb.config(command=self.cart_tree.xview)
        for col, w in zip(("ID", "Name", "Price"), (40, 140, 100)):
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=w, anchor=tk.CENTER)
        tk.Button(cart, text="Remove", bg="#d9534f", fg="white", font=("Arial", 10, "bold"),
                  command=self.remove_from_cart).pack(pady=3)

        # Add Form
        add = tk.LabelFrame(parent, text="Add Product", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        add.pack(fill=tk.X, padx=5, pady=5)
        af = tk.Frame(add, bg="white")
        af.pack(padx=10, pady=10)
        tk.Label(af, text="Product Name", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_name_entry = tk.Entry(af, font=("Arial", 11), width=20, state="readonly")
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(af, text="Price", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.price_entry = tk.Entry(af, font=("Arial", 11), width=12, state="readonly")
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(af, text="Quantity", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.qty_entry = tk.Entry(af, font=("Arial", 11), width=8)
        self.qty_entry.grid(row=0, column=5, padx=5, pady=5)
        self.qty_entry.insert(0, "1")
        btns = tk.Frame(af, bg="white")
        btns.grid(row=1, column=2, columnspan=4, pady=5)
        tk.Button(btns, text="Clear", bg="#1e3a5f", fg="white", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Add to Cart", bg="#1e3a5f", fg="white", command=self.add_to_cart).pack(side=tk.LEFT, padx=5)

    # ================================================
    # 7. BILLING PANEL
    # ================================================
    def create_billing_panel(self, parent):
        tk.Label(parent, text="Customer Billing Area", font=("Arial", 16, "bold"),
                 bg="#1e3a5f", fg="white", pady=10).pack(fill=tk.X)

        sum_fr = tk.Frame(parent, bg="#f0f0c8")
        sum_fr.pack(fill=tk.X, padx=10, pady=10)

        self.bill_amount_box = tk.Label(sum_fr, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        self.bill_amount_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(self.bill_amount_box, text="Bill Amount (₹)", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        self.bill_amount_val = tk.Label(self.bill_amount_box, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white")
        self.bill_amount_val.pack()

        tax_box = tk.Label(sum_fr, text="10.0%", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        tax_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(tax_box, text="Tax", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        tk.Label(tax_box, text="10.0%", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white").pack()

        self.net_pay_box = tk.Label(sum_fr, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        self.net_pay_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(self.net_pay_box, text="Net Pay (₹)", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        self.net_pay_val = tk.Label(self.net_pay_box, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white")
        self.net_pay_val.pack()

        btn_fr = tk.Frame(parent, bg="#f0f0c8")
        btn_fr.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(btn_fr, text="Generate Bill", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"),
                  command=self.generate_bill).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_fr, text="Print", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"),
                  command=self.print_bill).pack(side=tk.LEFT, padx=10)

        self.bill_text_area = tk.Text(parent, font=("Courier", 10), height=20, state=tk.DISABLED, bg="#fffbe6", wrap=tk.NONE)
        self.bill_text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.bill_text_area.pack_forget()

    # ================================================
    # 8. CART & BILL
    # ================================================
    def calc_click(self, val):
        cur = self.calc_display.get()
        if val == "Clear":
            self.calc_display.delete(0, tk.END)
            self.calc_display.insert(0, "0")
        elif val == "Ans":
            try:
                res = eval(cur)
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, str(res))
            except:
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, "Error")
        else:
            if cur in ("0", "Error"):
                self.calc_display.delete(0, tk.END)
            self.calc_display.insert(tk.END, val)

    def clear_form(self):
        self.product_name_entry.config(state="normal")
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.config(state="readonly")
        self.price_entry.config(state="normal")
        self.price_entry.delete(0, tk.END)
        self.price_entry.config(state="readonly")
        self.qty_entry.delete(0, tk.END)

    def add_to_cart(self):
        name = self.product_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please select a product!")
            return
        try:
            qty = int(self.qty_entry.get())
            if qty <= 0: raise ValueError
        except:
            messagebox.showerror("Error", "Invalid quantity!")
            return

        price = float(self.price_entry.get())
        final_price = price * qty

        for item in self.cart:
            if item["name"] == name:
                item["qty"] += qty
                item["final_price"] += final_price
                self.update_cart()
                self.clear_form()
                return

        self.cart.append({
            "id": next(p["id"] for p in self.products if p["name"] == name),
            "name": name,
            "price": price,
            "discount": 0,
            "qty": qty,
            "final_price": final_price
        })
        self.update_cart()
        self.clear_form()

    def remove_from_cart(self):
        sel = self.cart_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select item to remove!")
            return
        for s in sel:
            name = self.cart_tree.item(s, 'values')[1]
            self.cart = [c for c in self.cart if c["name"] != name]
        self.update_cart()

    def update_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        total = sum(c["final_price"] for c in self.cart)
        tax = total * 0.1
        net = total + tax
        for c in self.cart:
            self.cart_tree.insert("", tk.END, values=(c["id"], c["name"], f"₹{c['final_price']:.2f}"))
        self.cart_total_label.config(text=f"Total Products: {len(self.cart)}")
        self.bill_amount_val.config(text=f"{total:.2f}")
        self.net_pay_val.config(text=f"{net:.2f}")

    def save_bill_to_db(self):
        if not self.cart: return
        try:
            cur = self.connection.cursor()
            total = sum(c["final_price"] for c in self.cart)
            tax = total * 0.1
            net = total + tax

            # sales_data
            cur.execute("""
                INSERT INTO sales_data (invoice_no, customer_name, customer_contact, total_amount, discount, tax, net_pay)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (self.bill_no, self.customer_name or None, self.customer_contact or None, total, 0, tax, net))

            # sales_items + update stock
            for item in self.cart:
                cur.execute("""
                    INSERT INTO sales_items (invoice_no, product_name, quantity, price, discount, final_price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.bill_no, item["name"], item["qty"], item["price"], 0, item["final_price"]))
                cur.execute("UPDATE product_data SET quantity = quantity - %s WHERE id = %s", (item["qty"], item["id"]))

            self.connection.commit()
            cur.close()
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("DB Error", f"Lỗi lưu bill:\n{e}")

    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty!")
            return

        self.customer_name = self.name_entry.get().strip()
        self.customer_contact = self.contact_entry.get().strip()
        self.bill_no = random.randint(100000, 999999)

        total = sum(c["final_price"] for c in self.cart)
        tax = total * 0.1
        net = total + tax

        lines = [
            "StockApp-Inventory", "Phone: 7905112734, Lucknow",
            "-" * 50,
            f"Customer: {self.customer_name or 'Walk-in'}",
            f"Contact: {self.customer_contact or '-'}",
            f"Bill: {self.bill_no}  Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "-" * 50,
            f"{'Item':<20} {'Qty':>4} {'Price':>10} {'Total':>12}",
            "-" * 50
        ]
        for item in self.cart:
            lines.append(f"{item['name'][:19]:<20} {item['qty']:>4} ₹{item['price']:>8.2f} ₹{item['final_price']:>10.2f}")
        lines.extend([
            "-" * 50,
            f"{'Total':>34} ₹{total:>10.2f}",
            f"{'Tax 10%':>34} ₹{tax:>10.2f}",
            f"{'Net Pay':>34} ₹{net:>10.2f}",
            "-" * 50
        ])
        self.bill_text = "\n".join(lines)

        self.bill_text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.bill_text_area.config(state=tk.NORMAL)
        self.bill_text_area.delete(1.0, tk.END)
        self.bill_text_area.insert(tk.END, self.bill_text)
        self.bill_text_area.config(state=tk.DISABLED)

        os.makedirs("bills", exist_ok=True)
        fn = f"bills/Bill_{self.bill_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(self.bill_text)

        self.save_bill_to_db()
        messagebox.showinfo("Success", f"Bill #{self.bill_no} saved to file & DB!")

    def print_bill(self):
        if not self.bill_no:
            messagebox.showerror("Error", "Generate bill first!")
            return
        messagebox.showinfo("Print", "Bill sent to printer!")


# ================================================
# CHẠY ỨNG DỤNG
# ================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()