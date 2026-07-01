import customtkinter as ctk
from tkinter import ttk

class ProductsPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Product Management",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20)

        self.product_name = ctk.CTkEntry(form, placeholder_text="Product Name")
        self.product_name.grid(row=0, column=0, padx=10, pady=10)

        self.price = ctk.CTkEntry(form, placeholder_text="Selling Price")
        self.price.grid(row=0, column=1, padx=10, pady=10)

        self.stock = ctk.CTkEntry(form, placeholder_text="Stock Quantity")
        self.stock.grid(row=1, column=0, padx=10, pady=10)

        self.gst = ctk.CTkEntry(form, placeholder_text="GST %")
        self.gst.grid(row=1, column=1, padx=10, pady=10)

        save_btn = ctk.CTkButton(form, text="Save Product")
        save_btn.grid(row=2, column=0, pady=20)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = (
            "ID",
            "Product",
            "Price",
            "Stock",
            "GST"
        )

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill="both", expand=True)
