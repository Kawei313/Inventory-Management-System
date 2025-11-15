# sales.py - Sales Management & Revenue Statistics (SẠCH, ỔN ĐỊNH, KHÔNG LỖI)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from employees import connect_database


class SalesManagement:
    def __init__(self, parent_frame, on_back=None):
        self.parent = parent_frame
        self.on_back = on_back

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.create_layout()
        self.setup_default_dates()
        self.load_sales_data_in_range()

        self.parent.after(100, self.balance_panes)

    def balance_panes(self):
        total_width = self.parent.winfo_width()
        if total_width > 200:
            self.main_pane.sash_place(0, total_width // 2, 0)

    def create_layout(self):
        header = tk.Frame(self.parent, bg="#0f4d7d", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        if self.on_back:
            tk.Button(header, text="Back", bg="#dc3545", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT,
                      command=self.on_back).pack(side=tk.LEFT, padx=15, pady=10)

        tk.Label(header, text="Sales Management", font=("Arial", 18, "bold"), bg="#0f4d7d", fg="white")\
            .pack(side=tk.LEFT, padx=20, pady=10)

        tk.Button(header, text="Export Report", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT,
                  command=self.export_report).pack(side=tk.RIGHT, padx=20, pady=10)

        self.main_pane = tk.PanedWindow(self.parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6, bg="white")
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(self.main_pane, bg="white")
        self.main_pane.add(left_frame, stretch="always")

        stats_frame = tk.LabelFrame(left_frame, text="Revenue Statistics", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_stats_panel(stats_frame)

        list_frame = tk.LabelFrame(left_frame, text="Sales Invoices", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_sales_list(list_frame)

        right_frame = tk.Frame(self.main_pane, bg="white")
        self.main_pane.add(right_frame, stretch="always")

        details_frame = tk.LabelFrame(right_frame, text="Invoice Details", font=("Arial", 12, "bold"), bg="#f8f9fa", relief=tk.RIDGE, bd=2)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_bill_details(details_frame)

    def setup_default_dates(self):
        today = datetime.now()
        start_of_month = today.replace(day=1)
        self.from_date.set_date(start_of_month)
        self.to_date.set_date(today)

    def create_stats_panel(self, parent):
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(padx=12, pady=10, fill=tk.X)

        tk.Label(grid_frame, text="From:", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.from_date = DateEntry(grid_frame, width=12, date_pattern="dd-mm-yyyy", font=("Arial", 11), state="readonly")
        self.from_date.grid(row=0, column=1, padx=5, pady=5)
        self.from_date.bind("<<DateEntrySelected>>", lambda e: self.load_sales_data_in_range())

        tk.Label(grid_frame, text="To:", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.to_date = DateEntry(grid_frame, width=12, date_pattern="dd-mm-yyyy", font=("Arial", 11), state="readonly")
        self.to_date.grid(row=0, column=3, padx=5, pady=5)
        self.to_date.bind("<<DateEntrySelected>>", lambda e: self.load_sales_data_in_range())

        btn_frame = tk.Frame(grid_frame, bg="white")
        btn_frame.grid(row=0, column=4, columnspan=4, padx=10)
        tk.Button(btn_frame, text="Today", width=8, command=self.set_today).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="This Week", width=10, command=self.set_this_week).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="This Month", width=10, command=self.set_this_month).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Last Month", width=10, command=self.set_last_month).pack(side=tk.LEFT, padx=2)

        self.stats_labels = {}
        stats = [
            ("Daily Revenue", "₹0.00"),
            ("Monthly Revenue", "₹0.00"),
            ("Quarterly Revenue", "₹0.00"),
            ("Yearly Revenue", "₹0.00"),
            ("Total Invoices", "0")
        ]

        for i, (label, default) in enumerate(stats):
            r, c = divmod(i, 3)
            frame = tk.Frame(grid_frame, bg="#e3f2fd", relief=tk.RIDGE, bd=1, width=160, height=70)
            frame.grid(row=r + 1, column=c * 2, columnspan=2, padx=10, pady=8, sticky="nsew")
            frame.pack_propagate(False)
            tk.Label(frame, text=label, font=("Arial", 10, "bold"), bg="#e3f2fd").pack(pady=5)
            val_label = tk.Label(frame, text=default, font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1565c0")
            val_label.pack()
            self.stats_labels[label] = val_label

        for i in range(6):
            grid_frame.columnconfigure(i, weight=1)

    def set_today(self):
        today = datetime.now()
        self.from_date.set_date(today)
        self.to_date.set_date(today)
        self.load_sales_data_in_range()

    def set_this_week(self):
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        self.from_date.set_date(start)
        self.to_date.set_date(today)
        self.load_sales_data_in_range()

    def set_this_month(self):
        today = datetime.now()
        start = today.replace(day=1)
        self.from_date.set_date(start)
        self.to_date.set_date(today)
        self.load_sales_data_in_range()

    def set_last_month(self):
        today = datetime.now()
        first = today.replace(day=1)
        last_month_end = first - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        self.from_date.set_date(last_month_start)
        self.to_date.set_date(last_month_end)
        self.load_sales_data_in_range()

    def create_sales_list(self, parent):
        columns = ("invoice_no", "customer", "contact", "date", "total", "tax", "net_pay")
        self.sales_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        self.sales_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        widths = (110, 160, 130, 140, 110, 90, 110)
        for col, width in zip(columns, widths):
            self.sales_tree.heading(col, text=col.replace("_", " ").title())
            self.sales_tree.column(col, width=width, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.sales_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.configure(yscrollcommand=vsb.set)
        self.sales_tree.bind("<<TreeviewSelect>>", self.on_invoice_select)

    def create_bill_details(self, parent):
        info_frame = tk.Frame(parent, bg="#f8f9fa")
        info_frame.pack(fill=tk.X, padx=15, pady=10)

        self.info_labels = {}
        info_items = ["Customer", "Contact", "Invoice No", "Date"]
        for i, item in enumerate(info_items):
            tk.Label(info_frame, text=f"{item}:", font=("Arial", 11, "bold"), bg="#f8f9fa").grid(row=i, column=0, sticky=tk.W, padx=5, pady=4)
            lbl = tk.Label(info_frame, text="-", font=("Arial", 11), bg="#f8f9fa", anchor=tk.W, fg="#333")
            lbl.grid(row=i, column=1, sticky=tk.W, padx=5, pady=4)
            self.info_labels[item] = lbl

        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        item_columns = ("name", "qty", "price", "total")
        self.items_tree = ttk.Treeview(tree_frame, columns=item_columns, show="headings", height=10)
        self.items_tree.pack(fill=tk.BOTH, expand=True)

        item_widths = (280, 80, 110, 120)
        headers = ("Product Name", "Qty", "Price", "Total")
        for col, width, header in zip(item_columns, item_widths, headers):
            self.items_tree.heading(col, text=header)
            self.items_tree.column(col, width=width, anchor=tk.CENTER)

        total_frame = tk.Frame(parent, bg="#f8f9fa")
        total_frame.pack(fill=tk.X, padx=15, pady=12)

        self.total_labels = {}
        totals = ["Subtotal", "Tax", "Net Pay"]
        for i, t in enumerate(totals):
            tk.Label(total_frame, text=f"{t}:", font=("Arial", 11, "bold"), bg="#f8f9fa").grid(row=0, column=i, padx=25)
            val = tk.Label(total_frame, text="₹0.00", font=("Arial", 13, "bold"), bg="#f8f9fa", fg="#d32f2f")
            val.grid(row=1, column=i, padx=25)
            self.total_labels[t] = val

    def get_date_range(self):
        from_str = self.from_date.get()
        to_str = self.to_date.get()
        try:
            from_date = datetime.strptime(from_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            to_date = datetime.strptime(to_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            return from_date, to_date
        except ValueError:
            today = datetime.now().strftime("%Y-%m-%d")
            return today, today

    def load_sales_data_in_range(self):
        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            from_date, to_date = self.get_date_range()

            query = """
                SELECT invoice_no, customer_name, customer_contact, 
                       DATE_FORMAT(bill_date, '%%d/%%m/%%Y %%H:%%i'), total_amount, tax, net_pay
                FROM sales_data 
                WHERE DATE(bill_date) BETWEEN %s AND %s
                ORDER BY bill_date DESC
            """
            cursor.execute(query, (from_date, to_date))
            rows = cursor.fetchall()

            for row in self.sales_tree.get_children():
                self.sales_tree.delete(row)
            for row in rows:
                self.sales_tree.insert("", tk.END, values=row)

            self.update_statistics()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sales: {e}")
        finally:
            cursor.close()
            conn.close()

    def on_invoice_select(self, event):
        selected = self.sales_tree.selection()
        if not selected:
            return
        try:
            invoice_no = int(self.sales_tree.item(selected[0], "values")[0])
            self.load_invoice_details(invoice_no)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid invoice number.")

    def load_invoice_details(self, invoice_no):
        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            query = """
                SELECT customer_name, customer_contact, invoice_no,
                       DATE_FORMAT(bill_date, '%%d/%%m/%%Y %%H:%%i'), total_amount, tax, net_pay
                FROM sales_data WHERE invoice_no = %s
            """
            cursor.execute(query, (invoice_no,))
            header = cursor.fetchone()
            if not header:
                return

            total = float(header[4] or 0)
            tax = float(header[5] or 0)
            net_pay = float(header[6] or 0)

            self.info_labels["Customer"].config(text=header[0] or "Walk-in")
            self.info_labels["Contact"].config(text=header[1] or "-")
            self.info_labels["Invoice No"].config(text=header[2])
            self.info_labels["Date"].config(text=header[3])
            self.total_labels["Subtotal"].config(text=f"₹{total:.2f}")
            self.total_labels["Tax"].config(text=f"₹{tax:.2f}")
            self.total_labels["Net Pay"].config(text=f"₹{net_pay:.2f}")

            cursor.execute("SELECT product_name, quantity, price, final_price FROM sales_items WHERE invoice_no = %s", (invoice_no,))
            items = cursor.fetchall()
            for i in self.items_tree.get_children():
                self.items_tree.delete(i)
            for name, qty, price, total in items:
                self.items_tree.insert("", tk.END, values=(name, qty, f"₹{float(price):.2f}", f"₹{float(total):.2f}"))

        except Exception as e:
            messagebox.showerror("Error", f"Load details failed: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_statistics(self):
        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            from_date, to_date = self.get_date_range()
            query = """
                SELECT 
                    SUM(CASE WHEN DATE(bill_date) = CURDATE() THEN net_pay ELSE 0 END),
                    SUM(CASE WHEN MONTH(bill_date) = MONTH(CURDATE()) AND YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END),
                    SUM(CASE WHEN QUARTER(bill_date) = QUARTER(CURDATE()) AND YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END),
                    SUM(CASE WHEN YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END),
                    COUNT(*)
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
            """
            cursor.execute(query, (from_date, to_date))
            result = cursor.fetchone() or (0, 0, 0, 0, 0)
            daily, monthly, quarterly, yearly, count = result

            self.stats_labels["Daily Revenue"].config(text=f"₹{float(daily or 0):.2f}")
            self.stats_labels["Monthly Revenue"].config(text=f"₹{float(monthly or 0):.2f}")
            self.stats_labels["Quarterly Revenue"].config(text=f"₹{float(quarterly or 0):.2f}")
            self.stats_labels["Yearly Revenue"].config(text=f"₹{float(yearly or 0):.2f}")
            self.stats_labels["Total Invoices"].config(text=str(count))

        except Exception as e:
            messagebox.showerror("Error", f"Statistics error: {e}")
        finally:
            cursor.close()
            conn.close()

    def export_report(self):
        try:
            from_str = self.from_date.get()
            to_str = self.to_date.get()
            from_date, to_date = self.get_date_range()

            cursor, conn = connect_database()
            if not cursor:
                return

            cursor.execute("USE inventory_system")
            query = """
                SELECT invoice_no, customer_name, DATE_FORMAT(bill_date, '%%d/%%m/%%Y'), net_pay
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
                ORDER BY bill_date
            """
            cursor.execute(query, (from_date, to_date))
            sales = cursor.fetchall()
            total = sum(float(row[3]) for row in sales)

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save Report")
            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("═" * 70 + "\n")
                f.write("             SALES REVENUE REPORT\n")
                f.write(f"             From: {from_str}  To: {to_str}\n")
                f.write("═" * 70 + "\n\n")
                f.write(f"{'Invoice':<12} {'Customer':<22} {'Date':<12} {'Amount':>12}\n")
                f.write("─" * 70 + "\n")
                for inv, cust, date, amt in sales:
                    f.write(f"{inv:<12} {str(cust or 'Walk-in')[:21]:<22} {date:<12} ₹{float(amt):>10.2f}\n")
                f.write("─" * 70 + "\n")
                f.write(f"{'TOTAL':>46} ₹{total:>10.2f}\n")
                f.write("═" * 70 + "\n")
                f.write(f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

            messagebox.showinfo("Success", f"Report saved:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


def sales_form(parent_frame, on_back=None):
    SalesManagement(parent_frame, on_back)