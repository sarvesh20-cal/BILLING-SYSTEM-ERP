import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import mysql.connector
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ProductsPage:

    def __init__(self, parent):

        # =========================================================
        # DATABASE CONNECTION
        # =========================================================
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                port=3306,
                database="billing_system"
            )

            self.cursor = self.connection.cursor()

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Could not connect to database.\n\n{err}"
            )
            return

        self.category_map = {}
        self.selected_product_id = None

# Image Variables
        self.image_path = ""
        self.image_photo = None

        # =========================================================
        # TITLE
        # =========================================================
        title = ctk.CTkLabel(
            parent,
            text="Product Management ERP",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=(20, 10))

        # =========================================================
        # FORM
        # =========================================================
        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20, pady=10)

        for column in range(4):
            form.grid_columnconfigure(column, weight=1)

        # PRODUCT NAME
        self.product_name = ctk.CTkEntry(
            form,
            placeholder_text="Product Name"
        )
        self.product_name.grid(
            row=0, column=0,
            padx=10, pady=10,
            sticky="ew"
        )

        # CATEGORY
        self.category = ctk.CTkComboBox(
            form,
            values=["Select Category"]
        )
        self.category.set("Select Category")
        self.category.grid(
            row=0, column=1,
            padx=10, pady=10,
            sticky="ew"
        )

        # BARCODE
        self.barcode = ctk.CTkEntry(
            form,
            placeholder_text="Barcode (Optional)"
        )
        self.barcode.grid(
            row=0, column=2,
            padx=10, pady=10,
            sticky="ew"
        )

        # UNIT
        self.unit = ctk.CTkComboBox(
            form,
            values=[
                "pcs",
                "kg",
                "gram",
                "litre",
                "box",
                "packet"
            ]
        )
        self.unit.set("pcs")
        self.unit.grid(
            row=0, column=3,
            padx=10, pady=10,
            sticky="ew"
        )

        # PURCHASE PRICE
        self.purchase_price = ctk.CTkEntry(
            form,
            placeholder_text="Purchase Price"
        )
        self.purchase_price.grid(
            row=1, column=0,
            padx=10, pady=10,
            sticky="ew"
        )

        # SELLING PRICE
        self.selling_price = ctk.CTkEntry(
            form,
            placeholder_text="Selling Price"
        )
        self.selling_price.grid(
            row=1, column=1,
            padx=10, pady=10,
            sticky="ew"
        )

        # GST
        self.gst = ctk.CTkEntry(
            form,
            placeholder_text="GST %"
        )
        self.gst.grid(
            row=1, column=2,
            padx=10, pady=10,
            sticky="ew"
        )

        # STOCK
        self.stock = ctk.CTkEntry(
            form,
            placeholder_text="Stock Quantity"
        )
        self.stock.grid(
            row=1, column=3,
            padx=10, pady=10,
            sticky="ew"
        )

        # DESCRIPTION
        self.description = ctk.CTkEntry(
            form,
            placeholder_text="Product Description (Optional)"
        )
        self.description.grid(
            row=2, column=0,
            columnspan=2,
            padx=10, pady=10,
            sticky="ew"
        )

        # STATUS
        self.status = ctk.CTkComboBox(
            form,
            values=[
                "Active",
                "Inactive"
            ]
        )
        self.status.set("Active")
        self.status.grid(
            row=2, column=2,
            padx=10, pady=10,
            sticky="ew"
        )

        # CLEAR BUTTON
        clear_btn = ctk.CTkButton(
            form,
            text="Clear Fields",
            height=38,
            command=self.clear_fields
        )
        clear_btn.grid(
            row=2, column=3,
            padx=10, pady=10,
            sticky="ew"
        )

        # IMAGE
        image_frame = ctk.CTkFrame(form)
        image_frame.grid(row=3,column=0,columnspan=2,padx=10,pady=10,sticky="w")

        self.image_label = ctk.CTkLabel(image_frame,text="No Image",width=120)
        self.image_label.pack(side="left",padx=5)

        ctk.CTkButton(image_frame,text="Choose Image",command=self.choose_image).pack(side="left",padx=10)

        




        # =========================================================
        # BUTTON FRAME
        # =========================================================
        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )
        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=(10, 15)
        )

        # SAVE
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Product",
            width=160,
            height=40,
            command=self.save_product
        )
        save_btn.pack(side="left", padx=10)

        # UPDATE
        update_btn = ctk.CTkButton(
            button_frame,
            text="Update Product",
            width=160,
            height=40,
            command=self.update_product
        )
        update_btn.pack(side="left", padx=10)

        # DELETE
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Product",
            width=160,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_product
        )
        delete_btn.pack(side="left", padx=10)

        # =========================================================
        # TABLE
        # =========================================================
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "ID",
            "Product",
            "Category",
            "Barcode",
            "Purchase",
            "Selling",
            "GST",
            "Stock",
            "Unit",
            "Status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=110,
                anchor="center"
            )

        self.tree.column("Product", width=160)
        self.tree.column("Category", width=140)

        # VERTICAL SCROLLBAR
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        # HORIZONTAL SCROLLBAR
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_product
        )

        # =========================================================
        # INITIAL DATA
        # =========================================================
        self.load_categories()
        self.load_products()

    # =============================================================
    # LOAD CATEGORIES
    # =============================================================
    def load_categories(self):

        try:
            self.cursor.execute(
                """
                SELECT category_id, category_name
                FROM categories
                ORDER BY category_name
                """
            )

            rows = self.cursor.fetchall()

            self.category_map.clear()
            category_names = []

            for category_id, category_name in rows:
                self.category_map[category_name] = category_id
                category_names.append(category_name)

            if category_names:
                self.category.configure(
                    values=category_names
                )
                self.category.set(
                    category_names[0]
                )
            else:
                self.category.configure(
                    values=["No Categories"]
                )
                self.category.set(
                    "No Categories"
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Category Error",
                f"Could not load categories.\n\n{err}"
            )

    # =============================================================
    # SAVE PRODUCT
    # =============================================================
    def save_product(self):

        product_name = self.product_name.get().strip()
        category_name = self.category.get().strip()
        barcode = self.barcode.get().strip()
        purchase_price = self.purchase_price.get().strip()
        selling_price = self.selling_price.get().strip()
        gst = self.gst.get().strip()
        stock = self.stock.get().strip()
        unit = self.unit.get().strip()
        description = self.description.get().strip()
        status = self.status.get().strip()
        image_path = self.image_path

        if product_name == "":
            messagebox.showwarning(
                "Validation",
                "Please enter Product Name."
            )
            self.product_name.focus()
            return

        if category_name not in self.category_map:
            messagebox.showwarning(
                "Validation",
                "Please select a valid Category."
            )
            return

        if selling_price == "":
            messagebox.showwarning(
                "Validation",
                "Please enter Selling Price."
            )
            self.selling_price.focus()
            return

        try:
            purchase_price = float(
                purchase_price if purchase_price else 0
            )

            selling_price = float(selling_price)

            gst = float(
                gst if gst else 0
            )

            stock = int(
                stock if stock else 0
            )

        except ValueError:
            messagebox.showwarning(
                "Invalid Data",
                "Price, GST and Stock must contain valid numbers."
            )
            return

        if (
            purchase_price < 0
            or selling_price < 0
            or gst < 0
            or stock < 0
        ):
            messagebox.showwarning(
                "Invalid Data",
                "Price, GST and Stock cannot be negative."
            )
            return

        category_id = self.category_map[
            category_name
        ]

        if barcode == "":
            barcode = None

        try:
            query = """
                INSERT INTO products
                (
                    category_id,
                    product_name,
                    barcode,
                    description,
                    purchase_price,
                    selling_price,
                    gst_percent,
                    stock_quantity,
                    unit,
                    status,
                   image_path
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                category_id,
                product_name,
                barcode,
                description,
                purchase_price,
                selling_price,
                gst,
                stock,
                unit,
                status,
                image_path
            )

            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo(
                "Success",
                "Product saved successfully."
            )

            self.clear_fields()
            self.load_products()

        except mysql.connector.IntegrityError as err:
            messagebox.showerror(
                "Save Error",
                "Product could not be saved.\n\n"
                "The barcode may already exist.\n\n"
                f"{err}"
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                str(err)
            )

    # =============================================================
    # LOAD PRODUCTS
    # =============================================================
    def load_products(self):

        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
                SELECT
                    p.product_id,
                    p.product_name,
                    COALESCE(c.category_name, ''),
                    COALESCE(p.barcode, ''),
                    p.purchase_price,
                    p.selling_price,
                    p.gst_percent,
                    p.stock_quantity,
                    p.unit,
                    p.status

                FROM products p

                LEFT JOIN categories c
                ON p.category_id = c.category_id

                ORDER BY p.product_id DESC
            """

            self.cursor.execute(query)
            products = self.cursor.fetchall()

            for product in products:
                self.tree.insert(
                    "",
                    "end",
                    values=product
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Load Error",
                f"Could not load products.\n\n{err}"
            )

    # =============================================================
    # SELECT PRODUCT
    # =============================================================
    def select_product(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        if not values:
            return

        self.selected_product_id = values[0]

        try:
            query = """
                SELECT
                    p.product_name,
                    c.category_name,
                    p.barcode,
                    p.purchase_price,
                    p.selling_price,
                    p.gst_percent,
                    p.stock_quantity,
                    p.unit,
                    p.description,
                    p.status
                    p.description,
                    p.status,
                    p.image_path

                FROM products p

                LEFT JOIN categories c
                ON p.category_id = c.category_id

                WHERE p.product_id = %s
            """

            self.cursor.execute(
                query,
                (self.selected_product_id,)
            )

            product = self.cursor.fetchone()
            self.image_path = product[10] if product[10] else ""

            if not product:
                return

            self.product_name.delete(0, "end")
            self.barcode.delete(0, "end")
            self.purchase_price.delete(0, "end")
            self.selling_price.delete(0, "end")
            self.gst.delete(0, "end")
            self.stock.delete(0, "end")
            self.description.delete(0, "end")

            self.product_name.insert(
                0,
                product[0] if product[0] else ""
            )

            self.category.set(
                product[1] if product[1]
                else "Select Category"
            )

            self.barcode.insert(
                0,
                product[2] if product[2] else ""
            )

            self.purchase_price.insert(
                0,
                product[3]
                if product[3] is not None else "0"
            )

            self.selling_price.insert(
                0,
                product[4]
                if product[4] is not None else "0"
            )

            self.gst.insert(
                0,
                product[5]
                if product[5] is not None else "0"
            )

            self.stock.insert(
                0,
                product[6]
                if product[6] is not None else "0"
            )

            self.unit.set(
                product[7] if product[7] else "pcs"
            )

            self.description.insert(
                0,
                product[8] if product[8] else ""
            )

            self.status.set(
                product[9] if product[9] else "Active"
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Selection Error",
                str(err)
            )

    # =============================================================
    # UPDATE PRODUCT
    # =============================================================
    def update_product(self):

        if self.selected_product_id is None:
            messagebox.showwarning(
                "Select Product",
                "Please select a product from the table first."
            )
            return

        product_name = self.product_name.get().strip()
        category_name = self.category.get().strip()
        barcode = self.barcode.get().strip()
        purchase_price = self.purchase_price.get().strip()
        selling_price = self.selling_price.get().strip()
        gst = self.gst.get().strip()
        stock = self.stock.get().strip()
        unit = self.unit.get().strip()
        description = self.description.get().strip()
        status = self.status.get().strip()

        if product_name == "":
            messagebox.showwarning(
                "Validation",
                "Product Name cannot be empty."
            )
            return

        if category_name not in self.category_map:
            messagebox.showwarning(
                "Validation",
                "Please select a valid Category."
            )
            return

        if selling_price == "":
            messagebox.showwarning(
                "Validation",
                "Selling Price cannot be empty."
            )
            return

        try:
            purchase_price = float(
                purchase_price if purchase_price else 0
            )

            selling_price = float(selling_price)

            gst = float(
                gst if gst else 0
            )

            stock = int(
                stock if stock else 0
            )

        except ValueError:
            messagebox.showwarning(
                "Invalid Data",
                "Price, GST and Stock must contain valid numbers."
            )
            return

        if (
            purchase_price < 0
            or selling_price < 0
            or gst < 0
            or stock < 0
        ):
            messagebox.showwarning(
                "Invalid Data",
                "Price, GST and Stock cannot be negative."
            )
            return

        category_id = self.category_map[
            category_name
        ]

        if barcode == "":
            barcode = None

        try:
            query = """
                UPDATE products

                SET
                    category_id = %s,
                    product_name = %s,
                    barcode = %s,
                    description = %s,
                    purchase_price = %s,
                    selling_price = %s,
                    gst_percent = %s,
                    stock_quantity = %s,
                    unit = %s,
                    status = %s

                WHERE product_id = %s
            """

            values = (
                category_id,
                product_name,
                barcode,
                description,
                purchase_price,
                selling_price,
                gst,
                stock,
                unit,
                status,
                self.selected_product_id
            )

            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo(
                "Success",
                "Product updated successfully."
            )

            self.clear_fields()
            self.load_products()

        except mysql.connector.IntegrityError as err:
            messagebox.showerror(
                "Update Error",
                "Product could not be updated.\n\n"
                "The barcode may already belong "
                "to another product.\n\n"
                f"{err}"
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                str(err)
            )

    # =============================================================
    # DELETE PRODUCT - STEP 3
    # =============================================================
    def delete_product(self):

        # No product selected
        if self.selected_product_id is None:

            messagebox.showwarning(
                "Select Product",
                "Please select a product from the table first."
            )
            return

        # Get product name for confirmation message
        product_name = self.product_name.get().strip()

        # Ask user before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n"
            f"{product_name}?\n\n"
            "This action cannot be undone."
        )

        # User clicked No
        if not confirm:
            return

        try:
            query = """
                DELETE FROM products
                WHERE product_id = %s
            """

            self.cursor.execute(
                query,
                (self.selected_product_id,)
            )

            self.connection.commit()

            messagebox.showinfo(
                "Deleted",
                f"{product_name} deleted successfully."
            )

            self.clear_fields()
            self.load_products()

        except mysql.connector.IntegrityError:
            messagebox.showerror(
                "Cannot Delete Product",
                "This product is already being used in "
                "another record, such as an invoice.\n\n"
                "Instead of deleting it, change its "
                "status to Inactive."
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Could not delete product.\n\n{err}"
            )

    # =============================================================
    # IMAGE HELPERS
    # =============================================================
    def choose_image(self):
        path=filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            self.image_path=path
            self.show_image(path)

    def show_image(self,path):
        try:
            img=Image.open(path)
            img.thumbnail((100,100))
            photo=ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo,text="")
            self.image_label.image=photo
        except Exception:
            self.image_label.configure(text="Invalid Image",image=None)

    # =============================================================
    # CLEAR FIELDS
    # =============================================================
    def clear_fields(self):

        self.product_name.delete(0, "end")
        self.barcode.delete(0, "end")
        self.purchase_price.delete(0, "end")
        self.selling_price.delete(0, "end")
        self.gst.delete(0, "end")
        self.stock.delete(0, "end")
        self.description.delete(0, "end")

        self.unit.set("pcs")
        self.status.set("Active")

        if self.category_map:
            first_category = list(
                self.category_map.keys()
            )[0]

            self.category.set(
                first_category
            )

        self.selected_product_id = None
        self.image_path=None
        if self.image_label:
            self.image_label.configure(text='No Image',image=None)
        self.image_path = None
        self.image_label = None

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)