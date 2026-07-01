import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import mysql.connector

from customers import CustomersPage
from products import ProductsPage


class Dashboard:

    def __init__(self, root):

        self.root = root
        self.sidebar_expanded = True

        # =====================================
        # WINDOW
        # =====================================

        self.root.title("Billing ERP")

        # =====================================
        # SIDEBAR
        # =====================================

        self.sidebar = ctk.CTkFrame(
            root,
            width=250,
            fg_color="#0F172A",
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # =====================================
        # MAIN FRAME
        # =====================================

        self.main_frame = ctk.CTkFrame(
            root,
            fg_color="#F4F6F9"
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # =====================================
        # HEADER
        # =====================================

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

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Billing ERP Dashboard",
            font=("Segoe UI", 28, "bold")
        )

        self.title_label.pack(
            side="left",
            padx=20
        )

        self.clock = ctk.CTkLabel(
            self.header,
            text="",
            font=("Segoe UI", 16)
        )

        self.clock.pack(
            side="right",
            padx=20
        )

        # =====================================
        # CONTENT FRAME
        # =====================================

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#F4F6F9"
        )

        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # =====================================
        # SIDEBAR CONTENT
        # =====================================

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Billing ERP",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        )

        self.logo.pack(pady=20)

        self.menu_btn = ctk.CTkButton(
            self.sidebar,
            text="☰ Menu",
            width=220,
            command=self.toggle_sidebar
        )

        self.menu_btn.pack(pady=10)

        self.dashboard_btn = self.create_sidebar_button(
            "🏠 Dashboard",
            self.show_dashboard
        )

        self.customer_btn = self.create_sidebar_button(
            "👤 Customers",
            self.open_customers
        )

        self.products_btn = self.create_sidebar_button(
            "📦 Products",
            self.open_products
        )

        self.billing_btn = self.create_sidebar_button(
            "🧾 Billing",
            self.open_billing
        )

        self.invoices_btn = self.create_sidebar_button(
            "📄 Invoices",
            self.open_invoices
        )

        self.reports_btn = self.create_sidebar_button(
            "📊 Reports",
            self.open_reports
        )

        self.settings_btn = self.create_sidebar_button(
            "⚙ Settings",
            self.open_settings
        )

        self.logout_btn = self.create_sidebar_button(
            "🚪 Logout",
            self.logout
        )

        self.update_clock()

        self.show_dashboard()


    # =====================================
    # COMMON FUNCTIONS
    # =====================================

    def create_sidebar_button(self, text, command):

        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            width=220,
            height=45,
            fg_color="transparent",
            hover_color="#1E293B",
            anchor="w",
            command=command
        )

        btn.pack(pady=5)

        return btn


    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()


    def update_clock(self):

        self.clock.configure(
            text=datetime.now().strftime(
                "%d-%m-%Y  %H:%M:%S"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )
    
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

            cursor.execute(
                "SELECT COUNT(*) FROM customers"
            )

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return count
        
        except Exception as e:

            print("Customer Error:", e)
            return 0
    

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

            cursor.execute(
                "SELECT COUNT(*) FROM products"
            )

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return count

        except Exception as e: 
            
            print("Product Error:", e)
            return 0
    

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

            cursor.execute(
                "SELECT COUNT(*) FROM invoices"
        )

            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return count

        except Exception as e:

            print("Invoice Error:", e)
            return 0
        
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
            SELECT
            IFNULL(
                SUM(grand_total),
                0
            )
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
        
    
    def show_dashboard(self):

        self.clear_content()

    # ==========================
    # DASHBOARD TITLE
    # ==========================

        title = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard Overview",
            font=("Segoe UI", 26, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        refresh_btn = ctk.CTkButton(
            self.content_frame,
            text="🔄 Refresh Dashboard",
            command=self.show_dashboard
        )

        refresh_btn.pack(
            anchor="e",
            padx=20,
            pady=5
        )

    # ==========================
    # CARDS
    # ==========================

        cards_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=10
        )

        self.create_dashboard_card(
            cards_frame,
            "Today's Sales",
            self.get_today_sales()
        )

        self.create_dashboard_card(
            cards_frame,
            "Customers",
            self.get_customer_count()
        )

        self.create_dashboard_card(
            cards_frame,
            "Products",
            self.get_product_count()
        )

        self.create_dashboard_card(
            cards_frame,
            "Invoices",
            self.get_invoice_count()
        )

    # ==========================
    # RECENT INVOICES
    # ==========================

        table_frame = ctk.CTkFrame(
            self.content_frame
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        heading = ctk.CTkLabel(
            table_frame,
            text="Recent Invoices",
            font=("Segoe UI", 22, "bold")
        )

        heading.pack(pady=10)

        columns = (
            "Invoice No",
            "Amount",
            "Date"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:

            tree.heading(
                col,
                text=col
        )

            tree.column(
                col,
                width=250
        )

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_recent_invoices(tree)
     


    def create_dashboard_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            width=220,
            height=120
        )

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16)
        ).pack(pady=10)

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold")
        ).pack()


    def load_recent_invoices(self, tree):

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

            for row in rows:

                tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        f"₹{row[1]}",
                        str(row[2])
                    )
                )

            cursor.close()
            conn.close()

        except Exception as e:

            print(e)
    


    def toggle_sidebar(self):

        if self.sidebar_expanded:

            self.sidebar.configure(width=80)
            self.sidebar.update_idletasks()

            self.logo.configure(text="ERP")
            self.menu_btn.configure(text="☰")

            self.dashboard_btn.configure(text="🏠", width=60)
            self.customer_btn.configure(text="👤",width=60)
            self.products_btn.configure(text="📦", width=60)
            self.billing_btn.configure(text="🧾", width=60)
            self.invoices_btn.configure(text="📄", width=60)
            self.reports_btn.configure(text="📊", width=60)
            self.settings_btn.configure(text="⚙", width=60)
            self.logout_btn.configure(text="🚪", width=60)

            self.sidebar_expanded = False

        else:

            self.sidebar.configure(width=250)
            self.sidebar.update_idletasks()

            self.logo.configure(text="Billing ERP")
            
            self.menu_btn.configure(text = "☰ Menu")

            self.dashboard_btn.configure(text="🏠 Dashboard", width=220)
            self.customer_btn.configure(text="👤 Customers", width=220)
            self.products_btn.configure(text="📦 Products", width=220)
            self.billing_btn.configure(text="🧾 Billing", width=220)
            self.invoices_btn.configure(text="📄 Invoices", width=220)
            self.reports_btn.configure(text="📊 Reports", width=220)
            self.settings_btn.configure(text="⚙ Settings", width=220)
            self.logout_btn.configure(text="🚪 Logout", width=220)

            self.sidebar_expanded = True


    def open_customers(self):

        self.clear_content()

        CustomersPage(
            self.content_frame
        )


    def open_products(self):

        self.clear_content()

        ProductsPage(
            self.content_frame
        )


    def open_billing(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content_frame,
            text="Billing Module",
            font=("Segoe UI", 30, "bold")
        )

        label.pack(pady=50)


    def open_invoices(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content_frame,
            text="Invoices Module",
            font=("Segoe UI", 30, "bold")
        )

        label.pack(pady=50)


    def open_reports(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content_frame,
            text="Reports Module",
            font=("Segoe UI", 30, "bold")
        )

        label.pack(pady=50)


    def open_settings(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content_frame,
            text="Settings Module",
            font=("Segoe UI", 30, "bold")
        )

        label.pack(pady=50)


    def logout(self):

        self.root.destroy()


if __name__ == "__main__":

    root = ctk.CTk()

    root.geometry("1500x850")
    root.minsize(1200, 700)

    Dashboard(root)

    root.mainloop()
