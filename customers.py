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
            placeholder_text="Customer Name"
        )
        self.name.grid(row=0, column=0, padx=10, pady=10)

        self.phone = ctk.CTkEntry(
            form,
            placeholder_text="Phone"
        )
        self.phone.grid(row=0, column=1, padx=10, pady=10)

        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email"
        )
        self.email.grid(row=1, column=0, padx=10, pady=10)

        self.gst = ctk.CTkEntry(
            form,
            placeholder_text="GST Number"
        )
        self.gst.grid(row=1, column=1, padx=10, pady=10)

        # ==========================
        # BUTTONS
        # ==========================

        add_btn = ctk.CTkButton(
            form,
            text="Add",
            command=self.add_customer
        )
        add_btn.grid(row=2, column=0, padx=10, pady=10)

        update_btn = ctk.CTkButton(
            form,
            text="Update",
            command=self.update_customer
        )
        update_btn.grid(row=2, column=1, padx=10)

        delete_btn = ctk.CTkButton(
            form,
            text="Delete",
            command=self.delete_customer
        )
        delete_btn.grid(row=3, column=0, padx=10)

        clear_btn = ctk.CTkButton(
            form,
            text="Clear",
            command=self.clear_fields
        )
        clear_btn.grid(row=3, column=1, padx=10)

        # ==========================

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
                    gst_number
                FROM customers
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

        selected_row = self.tree.focus()

        contents = self.tree.item(selected_row)

        row = contents["values"]

        if row:

            self.selected_customer_id = row[0]

            self.clear_fields()

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

            return

        if not self.phone.get().isdigit():

            messagebox.showerror(
                "Error",
                "Phone number must contain digits only"
            )

            return

        if len(self.phone.get()) != 10:

            messagebox.showerror(
                "Error",
                "Phone number must be 10 digits"
            )

            return

        if "@" not in self.email.get():

            messagebox.showerror(
                "Error",
                "Invalid Email Address"
            )

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
                gst_number=%s
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
            self.load_customers(    )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================
    # CLEAR FIELDS
    # =====================================

    def clear_fields(self):

        self.name.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.gst.delete(0, "end")

        self.selected_customer_id = None