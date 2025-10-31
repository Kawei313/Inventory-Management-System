import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import os


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1e3a5f")

        self.products = [
            {"id": 1, "name": "A4 Paper Pack", "price": 500, "discount": 10},
            {"id": 2, "name": "Ballpoint Pens", "price": 200, "discount": 5},
            {"id": 3, "name": "Drill Machine", "price": 3000, "discount": 15},
            {"id": 4, "name": "Organic Apples", "price": 300, "discount": 5},
            {"id": 6, "name": "Fresh Spinach", "price": 150, "discount": 10},
            {"id": 8, "name": "Extension Cord", "price": 500, "discount": 5},
            {"id": 9, "name": "Cement", "price": 400, "discount": 5},
            {"id": 11, "name": "Surgical Masks", "price": 1500, "discount": 10},
            {"id": 13, "name": "Smartphone", "price": 15000, "discount": 10},
            {"id": 15, "name": "Office Chair", "price": 3500, "discount": 15},
            {"id": 17, "name": "Car Tyres", "price": 20000, "discount": 5},
            {"id": 19, "name": "T-Shirts", "price": 1000, "discount": 10},
        ]

        self.cart = []
        self.bill_no = None
        self.customer_name = ""
        self.customer_contact = ""
        self.bill_text = ""

        self.create_header()
        self.create_main_layout()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e3a5f", height=100)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Inventory Management System",
                 font=("Arial", 32, "bold"), bg="#1e3a5f", fg="white").pack(side=tk.LEFT, padx=20)

        tk.Button(header_frame, text="Logout", font=("Arial", 16, "bold"),
                  bg="#4a90d9", fg="white", padx=20, pady=5).pack(side=tk.RIGHT, padx=20)

        info_frame = tk.Frame(self.root, bg="#5a7a9f", height=40)
        info_frame.pack(fill=tk.X, padx=10)
        info_frame.pack_propagate(False)

        tk.Label(info_frame, text="Welcome Jane Smith", font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=20, pady=5)

        current_date = datetime.now().strftime("Date: %d/%m/%Y")
        tk.Label(info_frame, text=current_date, font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)

        current_time = datetime.now().strftime("Time: %I:%M %p")
        tk.Label(info_frame, text=current_time, font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)

    def create_main_layout(self):
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === PANED WINDOW: Cho phép kéo dãn ===
        paned = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True)

        # === LEFT: Products List (thu hẹp) ===
        left_frame = tk.Frame(paned, bg="white", relief=tk.RIDGE, bd=2)
        paned.add(left_frame)
        paned.paneconfigure(left_frame, stretch="always")  # Cho phép co giãn

        self.create_products_panel(left_frame)

        # === RIGHT: Calculator + Cart + Billing (mở rộng) ===
        right_frame = tk.Frame(paned, bg="white")
        paned.add(right_frame)
        paned.paneconfigure(right_frame, stretch="always")  # Cho phép co giãn

        # Chia right_frame thành 2 phần: Middle + Billing
        right_paned = tk.PanedWindow(right_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        right_paned.pack(fill=tk.BOTH, expand=True)

        # Middle: Calculator + Cart + Form
        middle_frame = tk.Frame(right_paned, bg="white")
        right_paned.add(middle_frame)
        right_paned.paneconfigure(middle_frame, stretch="always")

        # Billing Area
        billing_frame = tk.Frame(right_paned, bg="#f0f0c8", relief=tk.RIDGE, bd=2)
        right_paned.add(billing_frame)
        right_paned.paneconfigure(billing_frame, stretch="always")

        self.create_middle_panel(middle_frame)
        self.create_billing_panel(billing_frame)

    def create_products_panel(self, parent):
        tk.Label(parent, text="All Products", font=("Arial", 16, "bold"),
                 bg="#1e3a5f", fg="white", pady=10).pack(fill=tk.X)

        # Search
        search_frame = tk.Frame(parent, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Product Name", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=15)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", bg="#1e3a5f", fg="white",
                  command=self.search_product).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", bg="#1e3a5f", fg="white",
                  command=self.show_all_products).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.products_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Discount"),
                                          show="headings", yscrollcommand=scrollbar_y.set,
                                          xscrollcommand=scrollbar_x.set, height=20)
        self.products_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.config(command=self.products_tree.yview)
        scrollbar_x.config(command=self.products_tree.xview)

        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Discount", text="Discount (%)")

        self.products_tree.column("ID", width=40, anchor=tk.CENTER)
        self.products_tree.column("Name", width=140)
        self.products_tree.column("Price", width=80, anchor=tk.CENTER)
        self.products_tree.column("Discount", width=80, anchor=tk.CENTER)

        self.load_products()
        self.products_tree.bind("<<TreeviewSelect>>", self.on_product_select)

    def create_middle_panel(self, parent):
        # Customer Details
        cust_frame = tk.LabelFrame(parent, text="Customer Details", font=("Arial", 12, "bold"),
                                   bg="white", relief=tk.RIDGE, bd=2)
        cust_frame.pack(fill=tk.X, padx=5, pady=5)

        form = tk.Frame(cust_frame, bg="white")
        form.pack(padx=10, pady=10)

        tk.Label(form, text="Name", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(form, font=("Arial", 11), width=18)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Contact No.", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.contact_entry = tk.Entry(form, font=("Arial", 11), width=18)
        self.contact_entry.grid(row=0, column=3, padx=5, pady=5)

        # Calculator + Cart
        calc_cart_frame = tk.Frame(parent, bg="white")
        calc_cart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Calculator
        calc_frame = tk.LabelFrame(calc_cart_frame, text="Calculator", font=("Arial", 12, "bold"),
                                   bg="white", relief=tk.RIDGE, bd=2)
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

        self.calc_display = tk.Entry(calc_frame, font=("Arial", 18, "bold"), justify=tk.RIGHT,
                                     bd=5, relief=tk.SUNKEN)
        self.calc_display.pack(fill=tk.X, padx=8, pady=8)
        self.calc_display.insert(0, "0")

        btns = [['7', '8', '9', '+'], ['4', '5', '6', '-'],
                ['1', '2', '3', '*'], ['Ans', 'Clear', '0', '/']]

        btn_frame = tk.Frame(calc_frame, bg="white")
        btn_frame.pack(padx=8, pady=5)
        for r, row in enumerate(btns):
            for c, txt in enumerate(row):
                tk.Button(btn_frame, text=txt, font=("Arial", 14), width=6, height=2,
                          command=lambda x=txt: self.calc_click(x)).grid(row=r, column=c, padx=2, pady=2)

        # My Cart
        cart_frame = tk.LabelFrame(calc_cart_frame, text="My Cart  Total Products: 0", font=("Arial", 12, "bold"),
                                   bg="white", relief=tk.RIDGE, bd=2)
        cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=3)

        self.cart_total_label = tk.Label(cart_frame, text="Total Products: 0", font=("Arial", 10), bg="white")
        self.cart_total_label.pack(anchor=tk.E, padx=5)

        tree_frame = tk.Frame(cart_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.cart_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price"),
                                      show="headings", height=8,
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.config(command=self.cart_tree.yview)
        scroll_x.config(command=self.cart_tree.xview)

        self.cart_tree.heading("ID", text="ID")
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Price", text="Price")

        self.cart_tree.column("ID", width=40, anchor=tk.CENTER)
        self.cart_tree.column("Name", width=140)
        self.cart_tree.column("Price", width=100, anchor=tk.CENTER)

        tk.Button(cart_frame, text="Remove", bg="#d9534f", fg="white", font=("Arial", 10, "bold"),
                  command=self.remove_from_cart).pack(pady=3)

        # Add Product Form
        add_frame = tk.LabelFrame(parent, text="Add Product", font=("Arial", 12, "bold"),
                                  bg="white", relief=tk.RIDGE, bd=2)
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        form = tk.Frame(add_frame, bg="white")
        form.pack(padx=10, pady=10)

        tk.Label(form, text="Product Name", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_name_entry = tk.Entry(form, font=("Arial", 11), width=20, state="readonly")
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Price", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.price_entry = tk.Entry(form, font=("Arial", 11), width=12, state="readonly")
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Quantity", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.qty_entry = tk.Entry(form, font=("Arial", 11), width=8)
        self.qty_entry.grid(row=0, column=5, padx=5, pady=5)
        self.qty_entry.insert(0, "1")

        tk.Label(form, text="In stock: 0", font=("Arial", 11), bg="white", fg="red").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        btns = tk.Frame(form, bg="white")
        btns.grid(row=1, column=2, columnspan=4, pady=5)
        tk.Button(btns, text="Clear", bg="#1e3a5f", fg="white", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Add/Update Cart", bg="#1e3a5f", fg="white", command=self.add_to_cart).pack(side=tk.LEFT, padx=5)

    def create_billing_panel(self, parent):
        tk.Label(parent, text="Customer Billing Area", font=("Arial", 16, "bold"),
                 bg="#1e3a5f", fg="white", pady=10).pack(fill=tk.X)

        # Summary Boxes
        summary_frame = tk.Frame(parent, bg="#f0f0c8")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        self.bill_amount_box = tk.Label(summary_frame, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        self.bill_amount_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(self.bill_amount_box, text="Bill Amount (₹)", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        self.bill_amount_val = tk.Label(self.bill_amount_box, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white")
        self.bill_amount_val.pack()

        tax_box = tk.Label(summary_frame, text="10.0%", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        tax_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(tax_box, text="Tax", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        tk.Label(tax_box, text="10.0%", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white").pack()

        self.net_pay_box = tk.Label(summary_frame, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white", width=12, height=2, relief=tk.RAISED)
        self.net_pay_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        tk.Label(self.net_pay_box, text="Net Pay (₹)", font=("Arial", 10, "bold"), bg="#4a6c8c", fg="white").pack()
        self.net_pay_val = tk.Label(self.net_pay_box, text="0.0", font=("Arial", 14, "bold"), bg="#4a6c8c", fg="white")
        self.net_pay_val.pack()

        # Buttons
        btn_frame = tk.Frame(parent, bg="#f0f0c8")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Generate Bill", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"),
                  command=self.generate_bill).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Print", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"),
                  command=self.print_bill).pack(side=tk.LEFT, padx=10)

        # Bill Text Area (ẩn ban đầu)
        self.bill_text_area = tk.Text(parent, font=("Courier", 10), height=20, state=tk.DISABLED, bg="#fffbe6", wrap=tk.NONE)
        self.bill_text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.bill_text_area.pack_forget()

    def load_products(self):
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        for p in self.products:
            self.products_tree.insert("", tk.END, values=(p["id"], p["name"], p["price"], p["discount"]))

    def search_product(self):
        term = self.search_entry.get().lower()
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        for p in self.products:
            if term in p["name"].lower():
                self.products_tree.insert("", tk.END, values=(p["id"], p["name"], p["price"], p["discount"]))

    def show_all_products(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()

    def on_product_select(self, event):
        selected = self.products_tree.selection()
        if not selected: return
        item = self.products_tree.item(selected[0])
        name = item['values'][1]
        price = item['values'][2]

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

    def calc_click(self, val):
        current = self.calc_display.get()
        if val == "Clear":
            self.calc_display.delete(0, tk.END)
            self.calc_display.insert(0, "0")
        elif val == "Ans":
            try:
                res = eval(current)
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, str(res))
            except:
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, "Error")
        else:
            if current in ["0", "Error"]:
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
        product = next(p for p in self.products if p["name"] == name)
        disc_pct = product["discount"]
        final_price = (price * (100 - disc_pct) / 100) * qty

        for item in self.cart:
            if item["name"] == name:
                item["qty"] += qty
                item["final_price"] += final_price
                self.update_cart()
                self.clear_form()
                return

        self.cart.append({
            "id": product["id"],
            "name": name,
            "price": price,
            "discount": disc_pct,
            "qty": qty,
            "final_price": final_price
        })
        self.update_cart()
        self.clear_form()

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return
        for item in selected:
            values = self.cart_tree.item(item, 'values')
            name = values[1]
            self.cart = [p for p in self.cart if p["name"] != name]
        self.update_cart()

    def update_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)

        total = sum(p["price"] * p["qty"] for p in self.cart)
        total_disc = sum(p["price"] * p["qty"] * p["discount"] / 100 for p in self.cart)
        tax = total * 0.1
        net = total - total_disc + tax

        for p in self.cart:
            self.cart_tree.insert("", tk.END, values=(p["id"], p["name"], f"₹{p['final_price']:.1f}"))

        self.cart_total_label.config(text=f"Total Products: {len(self.cart)}")
        self.bill_amount_val.config(text=f"{total:.1f}")
        self.net_pay_val.config(text=f"{net:.1f}")

    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty!")
            return

        self.customer_name = self.name_entry.get().strip()
        self.customer_contact = self.contact_entry.get().strip()
        self.bill_no = random.randint(100000, 999999)

        # Tạo bill text
        bill_lines = [
            "StockApp-Inventory",
            "Phone No. 7905112734, Lucknow.226026",
            "-" * 50
        ]

        if self.customer_name:
            bill_lines.append(f"Customer Name: {self.customer_name}")
        if self.customer_contact:
            bill_lines.append(f"Phone no: {self.customer_contact}")

        bill_lines.append(f"Bill no: {self.bill_no}           Date: {datetime.now().strftime('%d/%m/%Y')}")
        bill_lines.append("-" * 50)
        bill_lines.append(f"{'Name':<13} {'Qty':>3} {'Price':>8} {'Discount':>12} {'Final Price':>12}")
        bill_lines.append("-" * 55)

        total = 0
        total_disc = 0
        for item in self.cart:
            subtotal = item["price"] * item["qty"]
            disc_amt = subtotal * item["discount"] / 100
            final = subtotal - disc_amt
            bill_lines.append(f"{item['name'][:12]:<13} {item['qty']:>3} ₹{item['price']:>6.1f}  {item['discount']}%={disc_amt:>5.1f}  ₹{final:>10.1f}")
            total += subtotal
            total_disc += disc_amt

        tax = total * 0.1
        net = total - total_disc + tax

        bill_lines.extend([
            "-" * 55,
            f"Bill Amount{'':>30} ₹{total:>8.1f}",
            f"Total Discount{'':>25} ₹{total_disc:>8.1f}",
            f"Tax{'':>38} ₹{tax:>8.1f}",
            f"Net Pay{'':>34} ₹{net:>8.1f}",
            "-" * 50
        ])

        self.bill_text = "\n".join(bill_lines)

        # Hiển thị bill
        self.bill_text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.bill_text_area.config(state=tk.NORMAL)
        self.bill_text_area.delete(1.0, tk.END)
        self.bill_text_area.insert(tk.END, self.bill_text)
        self.bill_text_area.config(state=tk.DISABLED)

        # Lưu file
        os.makedirs("bills", exist_ok=True)
        filename = f"bills/Bill_{self.bill_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.bill_text)

        messagebox.showinfo("Success", f"Bill #{self.bill_no} generated and saved!")

    def print_bill(self):
        if not self.bill_no:
            messagebox.showerror("Error", "Please generate bill first!")
            return
        messagebox.showinfo("Print", "Bill sent to printer!")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()