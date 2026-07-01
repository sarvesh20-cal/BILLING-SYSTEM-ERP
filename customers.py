import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector


class CustomersPage:

    def __init__(self, parent):

        self.selected_customer_id = None

        title = ctk.CTkLabel(
            parent,
            text="Customer Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        # ==========================
        # FORM
        # ==========================

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        self.name = ctk.CTkEntry(
            form,
            placeholder_text="Customer Name",
            width=250
        )
        self.name.grid(row=0, column=0, padx=10, pady=10)

        self.phone = ctk.CTkEntry(
            form,
            placeholder_text="Phone",
            width=250
        )
        self.phone.grid(row=0, column=1, padx=10, pady=10)

        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email",
            width=250
        )
        self.email.grid(row=1, column=0, padx=10, pady=10)

        self.gst = ctk.CTkEntry(
            form,
            placeholder_text="GST Number",
            width=250
        )
        self.gst.grid(row=1, column=1, padx=10, pady=10)

        # ==========================
        # BUTTONS
        # ==========================

        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add Customer",
            command=self.add_customer,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="✏ Update Customer",
            command=self.update_customer,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🗑 Delete Customer",
            command=self.delete_customer,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🔄 Clear Fields",
            command=self.clear_fields,
            width=150
        ).pack(side="left", padx=5)

        # ==========================
        # TABLE
        # ==========================

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "GST"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=180,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.get_data
        )

        self.load_customers()

    # =====================================
    # ADD CUSTOMER
    # =====================================

    def add_customer(self):

        if not self.validate_fields():
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()

            query = """
            INSERT INTO customers
            (
                customer_name,
                phone,
                email,
                GST_number
            )
            VALUES (%s,%s,%s,%s)
            """

            values = (
                self.name.get(),
                self.phone.get(),
                self.email.get(),
                self.gst.get()
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Customer Added Successfully"
            )

            self.clear_fields()
            self.load_customers()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================
    # LOAD CUSTOMERS
    # =====================================

    def load_customers(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

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
                    customer_id,
                    customer_name,
                    phone,
                    email,
                    GST_number
                FROM customers
                ORDER BY customer_id DESC
            """)

            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=row
                )

            cursor.close()
            conn.close()

        except Exception as e:
            print(e)

    # =====================================
    # SELECT ROW
    # =====================================

    def get_data(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        row = self.tree.item(selected[0])["values"]

        if row:

            self.selected_customer_id = row[0]

            print("Selected Customer ID =", self.selected_customer_id)

            self.name.delete(0, "end")
            self.phone.delete(0, "end")
            self.email.delete(0, "end")
            self.gst.delete(0, "end")

            self.name.insert(0, row[1])
            self.phone.insert(0, row[2])
            self.email.insert(0, row[3])
            self.gst.insert(0, row[4])
    # =====================================
    # UPDATE CUSTOMER
    # =====================================

    def update_customer(self):

        if self.selected_customer_id is None:

            messagebox.showerror(
                "Error",
                "Please select a customer first"
            )
            return

        if not self.validate_fields():
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            cursor = conn.cursor()

            query = """
            UPDATE customers
            SET
                customer_name=%s,
                phone=%s,
                email=%s,
                GST_number=%s
            WHERE customer_id=%s
            """

            values = (
                self.name.get(),
                self.phone.get(),
                self.email.get(),
                self.gst.get(),
                self.selected_customer_id
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Customer Updated Successfully"
            )

            self.clear_fields()
            self.load_customers()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================
    # DELETE CUSTOMER
    # =====================================

    def delete_customer(self):

        if self.selected_customer_id is None:

            messagebox.showerror(
                "Error",
                "Please select a customer first"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this customer?"
        )

        if not confirm:
            return

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
                "DELETE FROM customers WHERE customer_id=%s",
                (self.selected_customer_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Customer Deleted Successfully"
            )

            self.clear_fields()
            self.load_customers()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================
    # VALIDATION
    # =====================================

    def validate_fields(self):

        if (
            self.name.get().strip() == "" or
            self.phone.get().strip() == "" or
            self.email.get().strip() == "" or
            self.gst.get().strip() == ""
        ):

            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return False

        if not self.phone.get().isdigit():

            messagebox.showerror(
                "Error",
                "Phone number must contain digits only"
            )
            return False

        if len(self.phone.get()) != 10:

            messagebox.showerror(
                "Error",
                "Phone number must be 10 digits"
            )
            return False

        if "@" not in self.email.get():

            messagebox.showerror(
                "Error",
                "Invalid Email Address"
            )
            return False

        return True

    # =====================================
    # CLEAR FIELDS
    # =====================================

    def clear_fields(self):

        self.name.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.gst.delete(0, "end")

        self.selected_customer_id = None
