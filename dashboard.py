import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import mysql.connector
from customers import CustomersPage
from products import ProductsPage


class Dashboard:

    def __init__(self, root):

        self.root = root

        # ==============================
        # MAIN LAYOUT
        # ==============================

        self.sidebar = ctk.CTkFrame(
            root,
            width=250,
            fg_color="#0F172A",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(
            root,
            fg_color="#F4F6F9"
        )
        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )
        # ==============================
        # SIDEBAR
        # ==============================

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Billing ERP",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        self.logo.pack(pady=30)

        self.create_sidebar_button(
            "🏠 Dashboard",
            self.show_dashboard)

        self.create_sidebar_button(
            "👤 Customers",
            self.open_customers
        )

        self.create_sidebar_button(
            "📦 Products",
            self.open_products
        )

        self.create_sidebar_button(
            "🧾 Billing",
            self.open_billing
        )

        self.create_sidebar_button(
            "📄 Invoices",
            self.open_invoices
        )

        self.create_sidebar_button(
            "📊 Reports",
            self.open_reports
        )

        self.create_sidebar_button(
            "⚙ Settings",
            self.open_settings
        )

        self.create_sidebar_button(
            "🚪 Logout",
            self.logout
        )

        # ==============================
        # HEADER
        # ==============================

        self.header = ctk.CTkFrame(
            self.main_frame,
            height=80,
            fg_color="white"
        )
        self.header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.header.pack_propagate(False)

        self.title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            text_color="#111827"
        )
        self.title.pack(
            side="left",
            padx=20
        )

        self.clock = ctk.CTkLabel(
            self.header,
            text="",
            font=("Segoe UI", 16),
            text_color="#6B7280"
        )
        self.clock.pack(
            side="right",
            padx=20
        )

        self.update_clock()

                # ==============================
        # CARDS SECTION
        # ==============================

        self.cards_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.cards_frame.pack(
            fill="x",
            padx=20
        )

        self.create_card(
            self.cards_frame,
            "Today's Sales",
            self.get_today_sales()
        )

        self.create_card(
            self.cards_frame,
            "Customers",
            self.get_customer_count()
        )

        self.create_card(
            self.cards_frame,
            "Products",
            self.get_product_count()
        )

        self.create_card(
            self.cards_frame,
            "Invoices",
            self.get_invoice_count()
        )

        # ==============================
        # SALES ANALYTICS SECTION
        # ==============================

        self.graph_frame = ctk.CTkFrame(
            self.main_frame,
            height=300,
            fg_color="white",
            corner_radius=15
        )

        self.graph_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.graph_frame.pack_propagate(False)

        graph_title = ctk.CTkLabel(
            self.graph_frame,
            text="Sales Analytics",
            font=("Segoe UI", 20, "bold")
        )

        graph_title.pack(pady=20)

        graph_placeholder = ctk.CTkLabel(
            self.graph_frame,
            text="Sales Graph Here",
            font=("Segoe UI", 18),
            text_color="gray"
        )

        graph_placeholder.pack(pady=80)

        # ==============================
        # RECENT INVOICES TABLE
        # ==============================

        self.table_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=15
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        table_title = ctk.CTkLabel(
            self.table_frame,
            text="Recent Invoices",
            font=("Segoe UI", 20, "bold")
        )

        table_title.pack(pady=20)

        columns = (
            "Invoice No",
            "Customer",
            "Amount",
            "Status",
            "Date"
        )

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:

            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_recent_invoices()

    def get_customer_count(self):

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM customers")

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return str(count)

        except Exception as e:
            print("Customer Error:", e)
            return "0"


    def get_product_count(self):

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return str(count)

        except Exception as e:
            print("Product Error:", e)
            return "0"


    def get_invoice_count(self):

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM invoices")

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return str(count)

        except Exception as e:
            print("Invoice Error:", e)
            return "0"


    def get_today_sales(self):

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()

            cursor.execute("""
                SELECT IFNULL(SUM(grand_total),0)
                FROM invoices
                WHERE DATE(invoice_date)=CURDATE()
            """)

            sales = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return f"₹{sales:,.0f}"

        except Exception as e:
            print("Sales Error:", e)
            return "₹0"
        
    def create_sidebar_button(self, text, command):

        btn = ctk.CTkButton(
        self.sidebar,
        text=text,
        width=220,
        height=45,
        fg_color="transparent",
        hover_color="#1E293B",
        anchor="w",
        font=("Segoe UI", 16),
        command=command
    )

        btn.pack(pady=5)

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=140,
            fg_color="white",
            corner_radius=15
        )

        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI",16),
            text_color="#6B7280"
        )

        title_label.pack(pady=(25,10))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI",28,"bold"),
            text_color="#111827"
        )

        value_label.pack()

    def update_clock(self):

        current_time = datetime.now().strftime(
            "%d-%m-%Y  %H:%M:%S"
        )

        self.clock.configure(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_clock
        )

    def load_recent_invoices(self):

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    invoice_number,
                    grand_total,
                    invoice_date
                FROM invoices
                ORDER BY invoice_id DESC
                LIMIT 10
            """)

            rows = cursor.fetchall()
            print(rows)

            for row in rows:

                invoice_no = row[0]
                amount = f"₹{row[1]}"
                date = row[2].strftime("%d-%m-%Y")

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        invoice_no,
                        "",
                        amount,
                        "",
                        date
                    )
                )

            cursor.close()
            conn.close()

        except Exception as e:

            print("Invoice Error:", e)




    def clear_main_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def open_customers(self):
        self.clear_main_frame()
        CustomersPage(
            self.root
    )


    def open_products(self):
        self.clear_main_frame()
        ProductsPage(
            self.root
    )

    def show_dashboard(self):
        self.clear_main_frame()
        Dashboard(
            self.root
    )
    def open_billing(self):
        print("Billing Clicked")    

    def open_invoices(self):
        print("Invoices Clicked")

    def open_reports(self):
        print("Reports Clicked")

    def open_settings(self):
        print("Settings Clicked")
    def logout(self):
        self.root.destroy()
    
        