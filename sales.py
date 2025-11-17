# sales.py - Sales Management & Revenue Statistics (CALLBACK FIXED)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from employees import connect_database


class SalesManagement:
    def __init__(self, parent_frame, on_back=None):
        self.parent = parent_frame
        self.on_back = on_back
        self.is_destroyed = False
        self.after_ids = []  # Track all scheduled callbacks

        # Create database tables first
        self.create_sales_tables()

        # Clear parent frame AFTER checking database
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Build UI
        self.create_layout()
        self.setup_default_dates()

        # Load data after UI is completely ready
        self.parent.update_idletasks()
        self.schedule_callback(150, self.initial_load)

    def schedule_callback(self, delay, func):
        """Schedule a callback and track it"""
        after_id = self.parent.after(delay, func)
        self.after_ids.append(after_id)
        return after_id

    def cancel_all_callbacks(self):
        """Cancel all scheduled callbacks"""
        for after_id in self.after_ids:
            try:
                self.parent.after_cancel(after_id)
            except:
                pass
        self.after_ids.clear()

    def initial_load(self):
        """Initial data load with error handling"""
        if self.is_destroyed:
            return
        try:
            self.load_sales_data_in_range()
            self.schedule_callback(200, self.balance_panes)
        except Exception as e:
            print(f"Initial load error: {e}")

    def create_sales_tables(self):
        """Ensure sales tables exist"""
        cursor, conn = connect_database()
        if not cursor:
            return
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
            cursor.execute("USE inventory_system")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_data (
                    invoice_no INT PRIMARY KEY AUTO_INCREMENT,
                    customer_name VARCHAR(100),
                    customer_contact VARCHAR(20),
                    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_amount DECIMAL(10,2),
                    tax DECIMAL(10,2),
                    net_pay DECIMAL(10,2)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_items (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    invoice_no INT,
                    product_name VARCHAR(100),
                    quantity INT,
                    price DECIMAL(10,2),
                    final_price DECIMAL(10,2),
                    FOREIGN KEY (invoice_no) REFERENCES sales_data(invoice_no) ON DELETE CASCADE
                )
            """)
            conn.commit()
        except Exception as e:
            print(f"Database setup error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def balance_panes(self):
        """Balance panes with safety checks"""
        if self.is_destroyed:
            return
        try:
            if hasattr(self, 'main_pane') and self.main_pane.winfo_exists():
                total_width = self.parent.winfo_width()
                if total_width > 200:
                    self.main_pane.sash_place(0, total_width // 2, 0)
        except:
            pass

    def create_layout(self):
        # Header
        header = tk.Frame(self.parent, bg="#0f4d7d", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        if self.on_back:
            tk.Button(header, text="Back", bg="#dc3545", fg="white",
                      font=("Arial", 11, "bold"), relief=tk.FLAT,
                      command=self.safe_back, cursor="hand2").pack(side=tk.LEFT, padx=10, pady=8)

        tk.Label(header, text="Sales Management", font=("Arial", 16, "bold"),
                 bg="#0f4d7d", fg="white").pack(side=tk.LEFT, padx=15, pady=8)

        tk.Button(header, text="Export Report", bg="#1e3a5f", fg="white",
                  font=("Arial", 11, "bold"), relief=tk.FLAT,
                  command=self.export_report, cursor="hand2").pack(side=tk.RIGHT, padx=15, pady=8)

        # Main content pane
        self.main_pane = tk.PanedWindow(self.parent, orient=tk.HORIZONTAL,
                                        sashrelief=tk.RAISED, sashwidth=5, bg="white")
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # LEFT PANEL
        left_frame = tk.Frame(self.main_pane, bg="white")
        self.main_pane.add(left_frame, stretch="always")

        # Statistics panel
        stats_frame = tk.LabelFrame(left_frame, text="Revenue Statistics",
                                    font=("Arial", 11, "bold"), bg="white",
                                    relief=tk.GROOVE, bd=2)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_stats_panel(stats_frame)

        # Sales list
        list_frame = tk.LabelFrame(left_frame, text="Sales Invoices",
                                   font=("Arial", 11, "bold"), bg="white",
                                   relief=tk.GROOVE, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.create_sales_list(list_frame)

        # RIGHT PANEL
        right_frame = tk.Frame(self.main_pane, bg="white")
        self.main_pane.add(right_frame, stretch="always")

        details_frame = tk.LabelFrame(right_frame, text="Invoice Details",
                                      font=("Arial", 11, "bold"), bg="#f8f9fa",
                                      relief=tk.GROOVE, bd=2)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_bill_details(details_frame)

    def safe_back(self):
        """Safely go back and destroy the frame"""
        try:
            self.is_destroyed = True
            self.cancel_all_callbacks()

            # Unbind all events
            if hasattr(self, 'from_date'):
                try:
                    self.from_date.unbind("<<DateEntrySelected>>")
                except:
                    pass
            if hasattr(self, 'to_date'):
                try:
                    self.to_date.unbind("<<DateEntrySelected>>")
                except:
                    pass
            if hasattr(self, 'sales_tree'):
                try:
                    self.sales_tree.unbind("<<TreeviewSelect>>")
                except:
                    pass

            # Clear all widgets
            for widget in self.parent.winfo_children():
                widget.destroy()

            # Call back function
            if self.on_back:
                self.on_back()
        except Exception as e:
            print(f"Back navigation error: {e}")

    def setup_default_dates(self):
        today = datetime.now()
        start_of_month = today.replace(day=1)
        self.from_date.set_date(start_of_month)
        self.to_date.set_date(today)

    def create_stats_panel(self, parent):
        # Date filter row
        filter_frame = tk.Frame(parent, bg="white")
        filter_frame.pack(padx=8, pady=8, fill=tk.X)

        tk.Label(filter_frame, text="From:", font=("Arial", 10, "bold"),
                 bg="white").grid(row=0, column=0, padx=3, pady=3, sticky=tk.E)
        self.from_date = DateEntry(filter_frame, width=11, date_pattern="dd-mm-yyyy",
                                   font=("Arial", 9), state="readonly")
        self.from_date.grid(row=0, column=1, padx=3, pady=3)
        self.from_date.bind("<<DateEntrySelected>>", lambda e: self.on_date_change())

        tk.Label(filter_frame, text="To:", font=("Arial", 10, "bold"),
                 bg="white").grid(row=0, column=2, padx=3, pady=3, sticky=tk.E)
        self.to_date = DateEntry(filter_frame, width=11, date_pattern="dd-mm-yyyy",
                                 font=("Arial", 9), state="readonly")
        self.to_date.grid(row=0, column=3, padx=3, pady=3)
        self.to_date.bind("<<DateEntrySelected>>", lambda e: self.on_date_change())

        # Quick filter buttons
        btn_frame = tk.Frame(filter_frame, bg="white")
        btn_frame.grid(row=0, column=4, padx=5)

        tk.Button(btn_frame, text="Today", width=7, font=("Arial", 9),
                  command=self.set_today, cursor="hand2").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="This Week", width=9, font=("Arial", 9),
                  command=self.set_this_week, cursor="hand2").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="This Month", width=9, font=("Arial", 9),
                  command=self.set_this_month, cursor="hand2").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Last Month", width=9, font=("Arial", 9),
                  command=self.set_last_month, cursor="hand2").pack(side=tk.LEFT, padx=2)

        # Statistics cards
        cards_frame = tk.Frame(parent, bg="white")
        cards_frame.pack(padx=8, pady=(0, 8), fill=tk.X)

        self.stats_labels = {}
        stats = [
            ("Daily Revenue", "₹0.00", "#e3f2fd", "#1565c0"),
            ("Monthly Revenue", "₹0.00", "#fff3e0", "#e65100"),
            ("Quarterly Revenue", "₹0.00", "#f3e5f5", "#6a1b9a"),
            ("Yearly Revenue", "₹0.00", "#e8f5e9", "#2e7d32"),
            ("Total Invoices", "0", "#fce4ec", "#c2185b")
        ]

        for i, (label, default, bg, fg) in enumerate(stats):
            col = i % 3
            row = i // 3

            card = tk.Frame(cards_frame, bg=bg, relief=tk.RAISED, bd=1)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            tk.Label(card, text=label, font=("Arial", 9, "bold"),
                     bg=bg, fg="#333").pack(pady=(8, 2))
            val_label = tk.Label(card, text=default, font=("Arial", 13, "bold"),
                                 bg=bg, fg=fg)
            val_label.pack(pady=(0, 8))
            self.stats_labels[label] = val_label

        for i in range(3):
            cards_frame.columnconfigure(i, weight=1)

    def on_date_change(self):
        """Handle date change and reset invoice details"""
        if self.is_destroyed:
            return
        try:
            self.reset_invoice_details()
            self.load_sales_data_in_range()
        except Exception as e:
            print(f"Date change error: {e}")

    def reset_invoice_details(self):
        """Clear all invoice detail fields"""
        if self.is_destroyed:
            return
        try:
            self.info_labels["Customer"].config(text="-")
            self.info_labels["Contact"].config(text="-")
            self.info_labels["Invoice No"].config(text="-")
            self.info_labels["Date"].config(text="-")

            self.total_labels["Subtotal"].config(text="₹0.00")
            self.total_labels["Tax"].config(text="₹0.00")
            self.total_labels["Net Pay"].config(text="₹0.00")

            for i in self.items_tree.get_children():
                self.items_tree.delete(i)
        except:
            pass

    def set_today(self):
        if self.is_destroyed:
            return
        today = datetime.now()
        self.from_date.set_date(today)
        self.to_date.set_date(today)
        self.on_date_change()

    def set_this_week(self):
        if self.is_destroyed:
            return
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        self.from_date.set_date(start)
        self.to_date.set_date(today)
        self.on_date_change()

    def set_this_month(self):
        if self.is_destroyed:
            return
        today = datetime.now()
        start = today.replace(day=1)
        self.from_date.set_date(start)
        self.to_date.set_date(today)
        self.on_date_change()

    def set_last_month(self):
        if self.is_destroyed:
            return
        today = datetime.now()
        first = today.replace(day=1)
        last_month_end = first - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        self.from_date.set_date(last_month_start)
        self.to_date.set_date(last_month_end)
        self.on_date_change()

    def create_sales_list(self, parent):
        # Treeview container
        tree_container = tk.Frame(parent)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("invoice_no", "customer", "contact", "date", "total", "tax", "net_pay")
        self.sales_tree = ttk.Treeview(tree_container, columns=columns,
                                       show="headings", height=12)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.sales_tree.xview)
        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure columns
        widths = (100, 140, 110, 130, 100, 80, 100)
        headers = ("Invoice No", "Customer", "Contact", "Date", "Total", "Tax", "Net Pay")
        for col, width, header in zip(columns, widths, headers):
            self.sales_tree.heading(col, text=header)
            self.sales_tree.column(col, width=width, anchor=tk.CENTER)

        self.sales_tree.bind("<<TreeviewSelect>>", self.on_invoice_select)

    def create_bill_details(self, parent):
        # Customer info
        info_frame = tk.Frame(parent, bg="#f8f9fa")
        info_frame.pack(fill=tk.X, padx=10, pady=8)

        self.info_labels = {}
        info_items = ["Customer", "Contact", "Invoice No", "Date"]
        for i, item in enumerate(info_items):
            tk.Label(info_frame, text=f"{item}:", font=("Arial", 10, "bold"),
                     bg="#f8f9fa", width=12, anchor=tk.W).grid(row=i, column=0,
                                                               sticky=tk.W, padx=5, pady=3)
            lbl = tk.Label(info_frame, text="-", font=("Arial", 10),
                           bg="#f8f9fa", anchor=tk.W, fg="#333")
            lbl.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)
            self.info_labels[item] = lbl

        # Items table
        tk.Label(parent, text="Products:", font=("Arial", 10, "bold"),
                 bg="#f8f9fa", anchor=tk.W).pack(padx=10, pady=(8, 2))

        tree_frame = tk.Frame(parent, bg="#f8f9fa")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

        item_columns = ("name", "qty", "price", "total")
        self.items_tree = ttk.Treeview(tree_frame, columns=item_columns,
                                       show="headings", height=10)

        vsb2 = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=vsb2.set)
        vsb2.pack(side=tk.RIGHT, fill=tk.Y)
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        item_widths = (230, 70, 100, 110)
        headers = ("Product Name", "Qty", "Price", "Total")
        for col, width, header in zip(item_columns, item_widths, headers):
            self.items_tree.heading(col, text=header)
            self.items_tree.column(col, width=width, anchor=tk.CENTER)

        # Totals
        total_frame = tk.Frame(parent, bg="#f8f9fa")
        total_frame.pack(fill=tk.X, padx=10, pady=8)

        self.total_labels = {}
        totals = [("Subtotal", "#1976d2"), ("Tax", "#f57c00"), ("Net Pay", "#d32f2f")]
        for i, (t, color) in enumerate(totals):
            tk.Label(total_frame, text=f"{t}:", font=("Arial", 10, "bold"),
                     bg="#f8f9fa").grid(row=0, column=i * 2, padx=15, sticky=tk.E)
            val = tk.Label(total_frame, text="₹0.00", font=("Arial", 12, "bold"),
                           bg="#f8f9fa", fg=color)
            val.grid(row=0, column=i * 2 + 1, padx=5, sticky=tk.W)
            self.total_labels[t] = val

        total_frame.columnconfigure(1, weight=1)
        total_frame.columnconfigure(3, weight=1)
        total_frame.columnconfigure(5, weight=1)

    def get_date_range(self):
        """Get and validate date range"""
        if self.is_destroyed:
            return None, None
        try:
            from_str = self.from_date.get()
            to_str = self.to_date.get()

            from_dt = datetime.strptime(from_str, "%d-%m-%Y")
            to_dt = datetime.strptime(to_str, "%d-%m-%Y")

            if from_dt > to_dt:
                messagebox.showerror("Error", "Start date cannot be after end date!")
                return None, None

            return from_dt.strftime("%Y-%m-%d"), to_dt.strftime("%Y-%m-%d")
        except:
            today = datetime.now().strftime("%Y-%m-%d")
            return today, today

    def load_sales_data_in_range(self):
        if self.is_destroyed:
            return

        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            date_range = self.get_date_range()
            if date_range[0] is None:
                return

            from_date, to_date = date_range
            cursor.execute("USE inventory_system")

            query = """
                SELECT invoice_no, customer_name, customer_contact, 
                       DATE_FORMAT(bill_date, '%%d/%%m/%%Y %%H:%%i'), 
                       total_amount, tax, net_pay
                FROM sales_data 
                WHERE DATE(bill_date) BETWEEN %s AND %s
                ORDER BY bill_date DESC
            """
            cursor.execute(query, (from_date, to_date))
            rows = cursor.fetchall()

            if self.is_destroyed:
                return

            # Clear and insert
            for row in self.sales_tree.get_children():
                self.sales_tree.delete(row)

            for row in rows:
                self.sales_tree.insert("", tk.END, values=row)

            # Update statistics
            self.update_statistics(cursor, from_date, to_date)

        except:
            pass
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def on_invoice_select(self, event):
        if self.is_destroyed:
            return

        selected = self.sales_tree.selection()
        if not selected:
            return

        try:
            values = self.sales_tree.item(selected[0], "values")
            if not values or len(values) == 0:
                return

            invoice_no = int(values[0])
            self.load_invoice_details(invoice_no)
        except:
            pass

    def load_invoice_details(self, invoice_no):
        if self.is_destroyed:
            return

        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")

            query = """
                SELECT customer_name, customer_contact, invoice_no,
                       DATE_FORMAT(bill_date, '%%d/%%m/%%Y %%H:%%i'), 
                       total_amount, tax, net_pay
                FROM sales_data WHERE invoice_no = %s
            """
            cursor.execute(query, (invoice_no,))
            header = cursor.fetchone()

            if not header or self.is_destroyed:
                return

            self.info_labels["Customer"].config(text=header[0] or "Walk-in")
            self.info_labels["Contact"].config(text=header[1] or "-")
            self.info_labels["Invoice No"].config(text=str(header[2]))
            self.info_labels["Date"].config(text=header[3])

            total = float(header[4] or 0)
            tax = float(header[5] or 0)
            net_pay = float(header[6] or 0)

            self.total_labels["Subtotal"].config(text=f"₹{total:.2f}")
            self.total_labels["Tax"].config(text=f"₹{tax:.2f}")
            self.total_labels["Net Pay"].config(text=f"₹{net_pay:.2f}")

            cursor.execute("""
                SELECT product_name, quantity, price, final_price 
                FROM sales_items 
                WHERE invoice_no = %s
            """, (invoice_no,))
            items = cursor.fetchall()

            if self.is_destroyed:
                return

            for i in self.items_tree.get_children():
                self.items_tree.delete(i)

            for name, qty, price, final in items:
                self.items_tree.insert("", tk.END, values=(
                    name, qty, f"₹{float(price):.2f}", f"₹{float(final):.2f}"
                ))

        except:
            pass
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_statistics(self, cursor, from_date, to_date):
        """Update statistics based on selected date range"""
        if self.is_destroyed:
            return
        try:
            cursor.execute("""
                SELECT COALESCE(SUM(net_pay), 0)
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
            """, (from_date, to_date))
            total_revenue = float(cursor.fetchone()[0])

            cursor.execute("""
                SELECT COUNT(*)
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
            """, (from_date, to_date))
            count = int(cursor.fetchone()[0])

            if self.is_destroyed:
                return

            self.stats_labels["Daily Revenue"].config(text=f"₹{total_revenue:.2f}")
            self.stats_labels["Monthly Revenue"].config(text=f"₹{total_revenue:.2f}")
            self.stats_labels["Quarterly Revenue"].config(text=f"₹{total_revenue:.2f}")
            self.stats_labels["Yearly Revenue"].config(text=f"₹{total_revenue:.2f}")
            self.stats_labels["Total Invoices"].config(text=str(count))

        except:
            pass

    def export_report(self):
        if self.is_destroyed:
            return
        try:
            date_range = self.get_date_range()
            if date_range[0] is None:
                return

            from_date, to_date = date_range
            from_str = self.from_date.get()
            to_str = self.to_date.get()

            cursor, conn = connect_database()
            if not cursor:
                messagebox.showerror("Error", "Cannot connect to database")
                return

            cursor.execute("USE inventory_system")
            query = """
                SELECT invoice_no, customer_name, 
                       DATE_FORMAT(bill_date, '%%d/%%m/%%Y'), net_pay
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
                ORDER BY bill_date
            """
            cursor.execute(query, (from_date, to_date))
            sales = cursor.fetchall()

            if not sales:
                messagebox.showinfo("Info", "No data in this range")
                return

            total = sum(float(row[3] or 0) for row in sales)

            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Save Report"
            )

            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("          SALES REVENUE REPORT\n")
                f.write(f"          From: {from_str}  To: {to_str}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"{'Invoice':<12} {'Customer':<22} {'Date':<12} {'Amount':>12}\n")
                f.write("-" * 70 + "\n")

                for inv, cust, date, amt in sales:
                    customer = str(cust or 'Walk-in').replace('"', '').replace("'", "")[:21]
                    f.write(f"{inv:<12} {customer:<22} {date:<12} Rs{float(amt):>10.2f}\n")

                f.write("-" * 70 + "\n")
                f.write(f"{'TOTAL':>46} Rs{total:>10.2f}\n")
                f.write("=" * 70 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

            messagebox.showinfo("Success", f"Exported!\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()


def sales_form(parent_frame, on_back=None):
    """Initialize sales management form"""
    try:
        SalesManagement(parent_frame, on_back)
    except Exception as e:
        print(f"Sales form error: {e}")
        messagebox.showerror("Error", "Failed to load Sales Management")