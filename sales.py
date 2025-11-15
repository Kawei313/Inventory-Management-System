# sales.py - Sales Management & Revenue Statistics
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import os
from employees import connect_database


class SalesManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management")
        self.root.geometry("1400x700")
        self.root.configure(bg="white")

        self.create_layout()
        self.load_sales_data()

    def create_layout(self):
        # Header
        header = tk.Frame(self.root, bg="#0f4d7d", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="Sales Management", font=("Arial", 18, "bold"), bg="#0f4d7d", fg="white").pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(header, text="Export Report", bg="#1e3a5f", fg="white", font=("Arial", 12, "bold"),
                  command=self.export_report).pack(side=tk.RIGHT, padx=20, pady=10)

        # Main Panes
        main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Sales List + Stats
        left_frame = tk.Frame(main_pane, bg="white")
        main_pane.add(left_frame, stretch="always")

        # Stats Frame
        stats_frame = tk.LabelFrame(left_frame, text="Revenue Statistics", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        self.create_stats_panel(stats_frame)

        # Sales List
        list_frame = tk.LabelFrame(left_frame, text="Sales Invoices", font=("Arial", 12, "bold"), bg="white", relief=tk.RIDGE, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_sales_list(list_frame)

        # Right: Bill Details
        right_frame = tk.Frame(main_pane, bg="white")
        main_pane.add(right_frame, stretch="always")

        details_frame = tk.LabelFrame(right_frame, text="Invoice Details", font=("Arial", 12, "bold"), bg="#f0f0f0", relief=tk.RIDGE, bd=2)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_bill_details(details_frame)

    def create_stats_panel(self, parent):
        grid_frame = tk.Frame(parent, bg="white")
        grid_frame.pack(padx=10, pady=10)

        tk.Label(grid_frame, text="From:", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.from_date = DateEntry(
            grid_frame,
            width=12,
            background="white",
            date_pattern="dd-mm-yyyy",
            font=("Arial", 11),
            state="readonly"
        )
        self.from_date.grid(row=0, column=1, padx=5, pady=5)
        self.from_date.set_date(datetime.now())

        tk.Label(grid_frame, text="To:", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.to_date = DateEntry(
            grid_frame,
            width=12,
            date_pattern="dd-mm-yyyy",
            font=("Arial", 11),
            state="readonly"
        )
        self.to_date.grid(row=0, column=3, padx=5, pady=5)
        self.to_date.set_date(datetime.now())

        tk.Button(grid_frame, text="Refresh", bg="#1e3a5f", fg="white", command=self.update_statistics).grid(row=0, column=4, padx=5, pady=5)

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
            frame = tk.Frame(grid_frame, bg="#e8f4fc", relief=tk.RIDGE, bd=1)
            frame.grid(row=r + 1, column=c * 2, columnspan=2, padx=8, pady=8, sticky="ew")
            tk.Label(frame, text=label, font=("Arial", 10, "bold"), bg="#e8f4fc").pack()
            val_label = tk.Label(frame, text=default, font=("Arial", 14, "bold"), bg="#e8f4fc", fg="#1e3a5f")
            val_label.pack()
            self.stats_labels[label] = val_label

        grid_frame.columnconfigure((1, 3), weight=1)

    def create_sales_list(self, parent):
        columns = ("invoice_no", "customer", "contact", "date", "total", "tax", "net_pay")
        self.sales_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        self.sales_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        widths = (100, 150, 120, 130, 100, 80, 100)
        for col, width in zip(columns, widths):
            self.sales_tree.heading(col, text=col.replace("_", " ").title())
            self.sales_tree.column(col, width=width, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.sales_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.configure(yscrollcommand=vsb.set)

        self.sales_tree.bind("<<TreeviewSelect>>", self.on_invoice_select)

    def create_bill_details(self, parent):
        info_frame = tk.Frame(parent, bg="#f0f0f0")
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.info_labels = {}
        info_items = ["Customer", "Contact", "Invoice No", "Date"]
        for i, item in enumerate(info_items):
            tk.Label(info_frame, text=f"{item}:", font=("Arial", 11, "bold"), bg="#f0f0f0").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            lbl = tk.Label(info_frame, text="-", font=("Arial", 11), bg="#f0f0f0", anchor=tk.W, fg="#333")
            lbl.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.info_labels[item] = lbl

        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        item_columns = ("name", "qty", "price", "total")
        self.items_tree = ttk.Treeview(tree_frame, columns=item_columns, show="headings", height=10)
        self.items_tree.pack(fill=tk.BOTH, expand=True)

        item_widths = (200, 60, 100, 100)
        for col, width in zip(item_columns, item_widths):
            self.items_tree.heading(col, text=col.title())
            self.items_tree.column(col, width=width, anchor=tk.CENTER)

        total_frame = tk.Frame(parent, bg="#f0f0f0")
        total_frame.pack(fill=tk.X, padx=10, pady=5)

        self.total_labels = {}
        totals = ["Subtotal", "Tax", "Net Pay"]
        for i, t in enumerate(totals):
            tk.Label(total_frame, text=f"{t}:", font=("Arial", 11, "bold"), bg="#f0f0f0").grid(row=0, column=i, padx=10)
            val = tk.Label(total_frame, text="₹0.00", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#d32f2f")
            val.grid(row=1, column=i, padx=10)
            self.total_labels[t] = val

    def load_sales_data(self):
        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            date_format_str = "%d/%m/%Y %H:%i"
            cursor.execute("""
                SELECT invoice_no, customer_name, customer_contact, 
                       DATE_FORMAT(bill_date, %s), 
                       total_amount, tax, net_pay
                FROM sales_data 
                ORDER BY bill_date DESC
            """, (date_format_str,))
            rows = cursor.fetchall()

            for row in self.sales_tree.get_children():
                self.sales_tree.delete(row)

            for row in rows:
                self.sales_tree.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading sales: {e}")
        finally:
            cursor.close()
            conn.close()

    def on_invoice_select(self, event):
        selected = self.sales_tree.selection()
        if not selected:
            return

        raw_value = self.sales_tree.item(selected[0], "values")[0]
        print(f"[DEBUG] Giá trị thô từ Treeview: '{raw_value}' (type: {type(raw_value)})")

        try:
            invoice_no = int(raw_value)
            print(f"[DEBUG] invoice_no đã ép kiểu: {invoice_no}")
            self.load_invoice_details(invoice_no)
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Không thể ép kiểu invoice_no: {e}")
            messagebox.showerror("Error", "Invalid invoice number selected.")

    def load_invoice_details(self, invoice_no):
        print(f"[DEBUG] Bắt đầu load hóa đơn: {invoice_no}")

        cursor, conn = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")

            date_format_str = "%d/%m/%Y %H:%i"
            query = """
                SELECT customer_name, customer_contact, invoice_no,
                       DATE_FORMAT(bill_date, %s), total_amount, tax, net_pay
                FROM sales_data WHERE invoice_no = %s
            """
            params = (date_format_str, invoice_no)
            print(f"[DEBUG] Query: {query.strip()} | Params: {params}")
            cursor.execute(query, params)
            header = cursor.fetchone()

            if not header:
                print(f"[WARNING] Không tìm thấy hóa đơn #{invoice_no}")
                messagebox.showwarning("Not Found", f"Invoice #{invoice_no} not found.")
                return

            print(f"[DEBUG] Header từ DB: {header}")

            # Ép kiểu an toàn
            try:
                total = float(header[4]) if header[4] not in (None, '') else 0.0
                tax = float(header[5]) if header[5] not in (None, '') else 0.0
                net_pay = float(header[6]) if header[6] not in (None, '') else 0.0
                print(f"[DEBUG] total={total}, tax={tax}, net_pay={net_pay}")
            except (ValueError, TypeError) as e:
                print(f"[ERROR] Lỗi ép kiểu tiền: {e} | Dữ liệu: {header[4:7]}")
                total = tax = net_pay = 0.0

            # Cập nhật giao diện
            self.info_labels["Customer"].config(text=header[0] or "Walk-in")
            self.info_labels["Contact"].config(text=header[1] or "-")
            self.info_labels["Invoice No"].config(text=header[2])
            self.info_labels["Date"].config(text=header[3])
            self.total_labels["Subtotal"].config(text=f"₹{total:.2f}")
            self.total_labels["Tax"].config(text=f"₹{tax:.2f}")
            self.total_labels["Net Pay"].config(text=f"₹{net_pay:.2f}")

            # Load items
            cursor.execute("SELECT product_name, quantity, price, final_price FROM sales_items WHERE invoice_no = %s", (invoice_no,))
            items = cursor.fetchall()
            print(f"[DEBUG] Tìm thấy {len(items)} sản phẩm")

            for i in self.items_tree.get_children():
                self.items_tree.delete(i)
            for item in items:
                self.items_tree.insert("", tk.END, values=item)

        except Exception as e:
            print(f"[ERROR] Lỗi khi load hóa đơn: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load invoice details: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_statistics(self):
        try:
            from_str = self.from_date.get()
            to_str = self.to_date.get()
            from_date = datetime.strptime(from_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            to_date = datetime.strptime(to_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            cursor, conn = connect_database()
            if not cursor:
                return

            cursor.execute("USE inventory_system")
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN DATE(bill_date) = CURDATE() THEN net_pay ELSE 0 END) AS daily,
                    SUM(CASE WHEN MONTH(bill_date) = MONTH(CURDATE()) AND YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END) AS monthly,
                    SUM(CASE WHEN QUARTER(bill_date) = QUARTER(CURDATE()) AND YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END) AS quarterly,
                    SUM(CASE WHEN YEAR(bill_date) = YEAR(CURDATE()) THEN net_pay ELSE 0 END) AS yearly,
                    COUNT(*) AS total_invoices
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
            """, (from_date, to_date))

            result = cursor.fetchone()
            if result:
                daily, monthly, quarterly, yearly, count = result
                self.stats_labels["Daily Revenue"].config(text=f"₹{float(daily or 0):.2f}")
                self.stats_labels["Monthly Revenue"].config(text=f"₹{float(monthly or 0):.2f}")
                self.stats_labels["Quarterly Revenue"].config(text=f"₹{float(quarterly or 0):.2f}")
                self.stats_labels["Yearly Revenue"].config(text=f"₹{float(yearly or 0):.2f}")
                self.stats_labels["Total Invoices"].config(text=str(count or 0))

        except Exception as e:
            messagebox.showerror("Error", f"Statistics error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def export_report(self):
        try:
            from_str = self.from_date.get()
            to_str = self.to_date.get()
            from_date = datetime.strptime(from_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            to_date = datetime.strptime(to_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            cursor, conn = connect_database()
            if not cursor:
                return

            cursor.execute("USE inventory_system")
            cursor.execute("""
                SELECT invoice_no, customer_name, DATE_FORMAT(bill_date, '%d/%m/%Y'), net_pay
                FROM sales_data
                WHERE DATE(bill_date) BETWEEN %s AND %s
                ORDER BY bill_date
            """, (from_date, to_date))
            sales = cursor.fetchall()

            total = sum(float(row[3]) for row in sales)

            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Sales Report"
            )
            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("═" * 60 + "\n")
                f.write("          SALES REVENUE REPORT\n")
                f.write(f"         From: {from_str}  To: {to_str}\n")
                f.write("═" * 60 + "\n\n")
                f.write(f"{'Invoice':<12} {'Customer':<20} {'Date':<12} {'Amount':>12}\n")
                f.write("─" * 60 + "\n")
                for inv, cust, date, amt in sales:
                    f.write(f"{inv:<12} {str(cust or 'Walk-in')[:19]:<20} {date:<12} ₹{float(amt):>10.2f}\n")
                f.write("─" * 60 + "\n")
                f.write(f"{'TOTAL':>44} ₹{total:>10.2f}\n")
                f.write("═" * 60 + "\n")
                f.write(f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

            messagebox.showinfo("Success", f"Report exported to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


# =========================================
# CHẠY FORM
# =========================================
def sales_form(window):
    for widget in window.winfo_children():
        if widget.winfo_manager() == "pack":
            widget.pack_forget()

    sales_root = tk.Toplevel(window)
    sales_root.protocol("WM_DELETE_WINDOW", lambda: on_close(sales_root, window))
    app = SalesManagement(sales_root)


def on_close(sales_root, dashboard):
    sales_root.destroy()
    dashboard.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesManagement(root)
    root.mainloop()