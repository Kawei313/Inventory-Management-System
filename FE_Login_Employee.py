import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1e3a5f")

        # Data storage
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
        self.customer_name = ""
        self.customer_contact = ""
        self.calculator_display = "0"

        self.create_header()
        self.create_main_layout()

    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg="#1e3a5f", height=100)
        header_frame.pack(fill=tk.X, padx=10, pady=5)

        # Title
        title_label = tk.Label(header_frame, text="Inventory Management System",
                               font=("Arial", 32, "bold"), bg="#1e3a5f", fg="white")
        title_label.pack(side=tk.LEFT, padx=20)

        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", font=("Arial", 16, "bold"),
                               bg="#4a90d9", fg="white", padx=20, pady=5)
        logout_btn.pack(side=tk.RIGHT, padx=20)

        # Info bar
        info_frame = tk.Frame(self.root, bg="#5a7a9f", height=40)
        info_frame.pack(fill=tk.X, padx=10)

        tk.Label(info_frame, text="Welcome Jane Smith", font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=20, pady=5)

        current_date = datetime.now().strftime("Date: %d/%m/%Y")
        tk.Label(info_frame, text=current_date, font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)

        current_time = datetime.now().strftime("Time: %I:%M %p")
        tk.Label(info_frame, text=current_time, font=("Arial", 12),
                 bg="#5a7a9f", fg="white").pack(side=tk.LEFT, padx=100)

    def create_main_layout(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel - All Products
        self.create_products_panel(main_frame)

        # Middle Panel - Customer Details & Calculator
        self.create_middle_panel(main_frame)

        # Right Panel - Billing Area
        self.create_billing_panel(main_frame)

    def create_products_panel(self, parent):
        left_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header
        header = tk.Label(left_frame, text="All Products", font=("Arial", 16, "bold"),
                          bg="#1e3a5f", fg="white", pady=10)
        header.pack(fill=tk.X)

        # Search section
        search_frame = tk.Frame(left_frame, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Product Name", font=("Arial", 12, "bold"),
                 bg="white").pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", padx=15, command=self.search_product).pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Show All", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", padx=15, command=self.show_all_products).pack(side=tk.LEFT, padx=5)

        # Products table
        table_frame = tk.Frame(left_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        self.products_tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Price", "Discount"),
                                          show="headings", yscrollcommand=scrollbar.set, height=20)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.products_tree.yview)

        # Configure columns
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Discount", text="Discount (%)")

        self.products_tree.column("ID", width=50, anchor=tk.CENTER)
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=100, anchor=tk.CENTER)
        self.products_tree.column("Discount", width=100, anchor=tk.CENTER)

        # Load products
        self.load_products()

    def create_middle_panel(self, parent):
        middle_frame = tk.Frame(parent, bg="white")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Customer Details
        customer_frame = tk.LabelFrame(middle_frame, text="Customer Details",
                                       font=("Arial", 14, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        customer_frame.pack(fill=tk.X, padx=5, pady=5)

        details_frame = tk.Frame(customer_frame, bg="white")
        details_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(details_frame, text="Name", font=("Arial", 12, "bold"),
                 bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(details_frame, font=("Arial", 12), width=15)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(details_frame, text="Contact No.", font=("Arial", 12, "bold"),
                 bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.contact_entry = tk.Entry(details_frame, font=("Arial", 12), width=15)
        self.contact_entry.grid(row=0, column=3, padx=5, pady=5)

        # Calculator
        calc_frame = tk.LabelFrame(middle_frame, text="Calculator",
                                   font=("Arial", 14, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.calc_display = tk.Entry(calc_frame, font=("Arial", 24, "bold"),
                                     justify=tk.RIGHT, bd=5, relief=tk.SUNKEN)
        self.calc_display.pack(fill=tk.X, padx=10, pady=10)
        self.calc_display.insert(0, "0")

        buttons_frame = tk.Frame(calc_frame, bg="white")
        buttons_frame.pack(padx=10, pady=10)

        buttons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['Ans', 'Clear', '0', '/']
        ]

        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                btn = tk.Button(buttons_frame, text=btn_text, font=("Arial", 16, "bold"),
                                width=8, height=2, command=lambda x=btn_text: self.calc_click(x))
                btn.grid(row=i, column=j, padx=2, pady=2)

        # Product selection
        product_frame = tk.LabelFrame(middle_frame, text="Add Product to Cart",
                                      font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        product_frame.pack(fill=tk.X, padx=5, pady=5)

        form_frame = tk.Frame(product_frame, bg="white")
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(form_frame, text="Product Name", font=("Arial", 11, "bold"),
                 bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = tk.Entry(form_frame, font=("Arial", 11), width=15)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Price", font=("Arial", 11, "bold"),
                 bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame, font=("Arial", 11), width=12)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity", font=("Arial", 11, "bold"),
                 bg="white").grid(row=0, column=4, padx=5, pady=5)
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 11), width=12)
        self.quantity_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(form_frame, text="In stock: 0", font=("Arial", 11),
                 bg="white", fg="red").grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        btn_frame = tk.Frame(product_frame, bg="white")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Clear", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", width=15, command=self.clear_product_form).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Add/Update Cart", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", width=15, command=self.add_to_cart).pack(side=tk.LEFT, padx=5)

    def create_billing_panel(self, parent):
        right_frame = tk.Frame(parent, bg="#f0f0c8")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header
        header = tk.Label(right_frame, text="Customer Billing Area", font=("Arial", 16, "bold"),
                          bg="#1e3a5f", fg="white", pady=10)
        header.pack(fill=tk.X)

        # Company info
        info_frame = tk.Frame(right_frame, bg="#f0f0c8")
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(info_frame, text="StockApp-Inventory", font=("Arial", 12, "bold"),
                 bg="#f0f0c8").pack()
        tk.Label(info_frame, text="Phone No. 7905112734, Lucknow.226026", font=("Arial", 10),
                 bg="#f0f0c8").pack()

        # Customer info display
        customer_info_frame = tk.Frame(right_frame, bg="#f0f0c8")
        customer_info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.bill_customer_name = tk.Label(customer_info_frame, text="Customer Name: ",
                                           font=("Arial", 10), bg="#f0f0c8", anchor=tk.W)
        self.bill_customer_name.pack(fill=tk.X)

        self.bill_customer_phone = tk.Label(customer_info_frame, text="Phone no: ",
                                            font=("Arial", 10), bg="#f0f0c8", anchor=tk.W)
        self.bill_customer_phone.pack(fill=tk.X)

        bill_info_frame = tk.Frame(customer_info_frame, bg="#f0f0c8")
        bill_info_frame.pack(fill=tk.X)

        self.bill_no_label = tk.Label(bill_info_frame, text="Bill no: ",
                                      font=("Arial", 10), bg="#f0f0c8", anchor=tk.W)
        self.bill_no_label.pack(side=tk.LEFT)

        self.bill_date_label = tk.Label(bill_info_frame,
                                        text=f"Date: {datetime.now().strftime('%d/%m/%Y')}",
                                        font=("Arial", 10), bg="#f0f0c8", anchor=tk.E)
        self.bill_date_label.pack(side=tk.RIGHT)

        # Cart table
        cart_label = tk.Label(right_frame, text="My Cart  Total Products: 0",
                              font=("Arial", 12, "bold"), bg="#f0f0c8")
        cart_label.pack(fill=tk.X, padx=10, pady=5)

        cart_frame = tk.Frame(right_frame, bg="#f0f0c8")
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(cart_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cart_tree = ttk.Treeview(cart_frame, columns=("Name", "Qty", "Price", "Discount", "Final"),
                                      show="headings", yscrollcommand=scrollbar.set, height=10)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.cart_tree.yview)

        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Discount", text="Discount")
        self.cart_tree.heading("Final", text="Final Price")

        self.cart_tree.column("Name", width=150)
        self.cart_tree.column("Qty", width=50, anchor=tk.CENTER)
        self.cart_tree.column("Price", width=80, anchor=tk.CENTER)
        self.cart_tree.column("Discount", width=100, anchor=tk.CENTER)
        self.cart_tree.column("Final", width=100, anchor=tk.CENTER)

        # Summary
        summary_frame = tk.Frame(right_frame, bg="#f0f0c8")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(summary_frame, text="Bill Amount", font=("Arial", 11, "bold"),
                 bg="#f0f0c8").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.bill_amount_label = tk.Label(summary_frame, text="₹0.0", font=("Arial", 11),
                                          bg="#f0f0c8", anchor=tk.E)
        self.bill_amount_label.grid(row=0, column=1, sticky=tk.E, pady=2)

        tk.Label(summary_frame, text="Total Discount", font=("Arial", 11, "bold"),
                 bg="#f0f0c8").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.total_discount_label = tk.Label(summary_frame, text="₹0.0", font=("Arial", 11),
                                             bg="#f0f0c8", anchor=tk.E)
        self.total_discount_label.grid(row=1, column=1, sticky=tk.E, pady=2)

        tk.Label(summary_frame, text="Tax", font=("Arial", 11, "bold"),
                 bg="#f0f0c8").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.tax_label = tk.Label(summary_frame, text="₹0.0", font=("Arial", 11),
                                  bg="#f0f0c8", anchor=tk.E)
        self.tax_label.grid(row=2, column=1, sticky=tk.E, pady=2)

        tk.Label(summary_frame, text="Net Pay", font=("Arial", 11, "bold"),
                 bg="#f0f0c8").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.net_pay_label = tk.Label(summary_frame, text="₹0.0", font=("Arial", 11, "bold"),
                                      bg="#f0f0c8", anchor=tk.E)
        self.net_pay_label.grid(row=3, column=1, sticky=tk.E, pady=2)

        summary_frame.columnconfigure(1, weight=1)

        # Summary boxes
        boxes_frame = tk.Frame(right_frame, bg="#f0f0c8")
        boxes_frame.pack(fill=tk.X, padx=10, pady=5)

        bill_box = tk.Frame(boxes_frame, bg="#4a6c8c", relief=tk.RAISED, bd=2)
        bill_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        tk.Label(bill_box, text="Bill Amount (₹)", font=("Arial", 11, "bold"),
                 bg="#4a6c8c", fg="white").pack(pady=5)
        self.bill_amount_box = tk.Label(bill_box, text="35430.0", font=("Arial", 14, "bold"),
                                        bg="#4a6c8c", fg="white")
        self.bill_amount_box.pack(pady=5)

        tax_box = tk.Frame(boxes_frame, bg="#4a6c8c", relief=tk.RAISED, bd=2)
        tax_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        tk.Label(tax_box, text="Tax\n10.0%", font=("Arial", 11, "bold"),
                 bg="#4a6c8c", fg="white").pack(pady=10)

        net_box = tk.Frame(boxes_frame, bg="#4a6c8c", relief=tk.RAISED, bd=2)
        net_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        tk.Label(net_box, text="Net Pay (₹)", font=("Arial", 11, "bold"),
                 bg="#4a6c8c", fg="white").pack(pady=5)
        self.net_pay_box = tk.Label(net_box, text="38973.0", font=("Arial", 14, "bold"),
                                    bg="#4a6c8c", fg="white")
        self.net_pay_box.pack(pady=5)

        # Action buttons
        btn_frame = tk.Frame(right_frame, bg="#f0f0c8")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Generate Bill", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", width=15, command=self.generate_bill).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Print", font=("Arial", 12, "bold"),
                  bg="#1e3a5f", fg="white", width=15, command=self.print_bill).pack(side=tk.LEFT, padx=5)

    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        for product in self.products:
            self.products_tree.insert("", tk.END, values=(
                product["id"], product["name"], product["price"], product["discount"]
            ))

    def search_product(self):
        search_term = self.search_entry.get().lower()
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        for product in self.products:
            if search_term in product["name"].lower():
                self.products_tree.insert("", tk.END, values=(
                    product["id"], product["name"], product["price"], product["discount"]
                ))

    def show_all_products(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()

    def calc_click(self, value):
        current = self.calc_display.get()

        if value == "Clear":
            self.calc_display.delete(0, tk.END)
            self.calc_display.insert(0, "0")
        elif value == "Ans":
            try:
                result = eval(current)
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, str(result))
            except:
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, "Error")
        else:
            if current == "0" or current == "Error":
                self.calc_display.delete(0, tk.END)
                self.calc_display.insert(0, value)
            else:
                self.calc_display.insert(tk.END, value)

    def clear_product_form(self):
        self.product_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def add_to_cart(self):
        try:
            name = self.product_name_entry.get()
            price = float(self.price_entry.get())
            qty = int(self.quantity_entry.get())

            # Find product to get discount
            product = next((p for p in self.products if p["name"].lower() == name.lower()), None)
            discount = product["discount"] if product else 0

            discount_amount = price * (discount / 100)
            final_price = (price - discount_amount) * qty

            self.cart.append({
                "name": name,
                "qty": qty,
                "price": price,
                "discount": discount,
                "final_price": final_price
            })

            self.update_cart_display()
            self.clear_product_form()
            messagebox.showinfo("Success", "Product added to cart!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid values!")

    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total_amount = 0
        total_discount = 0

        for item in self.cart:
            discount_str = f"{item['discount']}%={item['price'] * item['discount'] / 100:.1f}"
            self.cart_tree.insert("", tk.END, values=(
                item["name"], item["qty"], f"₹{item['price']:.1f}",
                discount_str, f"₹{item['final_price']:.1f}"
            ))

            subtotal = item["price"] * item["qty"]
            total_amount += subtotal
            total_discount += subtotal - item["final_price"]

        tax = total_amount * 0.10
        net_pay = (total_amount - total_discount) + tax

        self.bill_amount_label.config(text=f"₹{total_amount:.1f}")
        self.total_discount_label.config(text=f"₹{total_discount:.1f}")
        self.tax_label.config(text=f"₹{tax:.1f}")
        self.net_pay_label.config(text=f"₹{net_pay:.1f}")

        self.bill_amount_box.config(text=f"{total_amount:.1f}")
        self.net_pay_box.config(text=f"{net_pay:.1f}")

    def generate_bill(self):
        name = self.name_entry.get()
        contact = self.contact_entry.get()

        if not name or not contact:
            messagebox.showerror("Error", "Please enter customer details!")
            return

        if not self.cart:
            messagebox.showerror("Error", "Cart is empty!")
            return

        self.bill_customer_name.config(text=f"Customer Name: {name}")
        self.bill_customer_phone.config(text=f"Phone no: {contact}")

        import random
        bill_no = random.randint(1000000, 9999999)
        self.bill_no_label.config(text=f"Bill no: {bill_no}")

        messagebox.showinfo("Success", f"Bill #{bill_no} generated successfully!")

    def print_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "No bill to print!")
            return
        messagebox.showinfo("Print", "Bill sent to printer!")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()