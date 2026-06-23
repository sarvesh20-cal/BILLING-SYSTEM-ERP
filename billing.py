import customtkinter as ctk
from tkinter import ttk

class BillingPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Create Invoice",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=20)

        self.customer = ctk.CTkComboBox(
            top_frame,
            values=["Customer 1", "Customer 2"]
        )
        self.customer.pack(side="left", padx=10, pady=10)

        self.product_search = ctk.CTkEntry(
            top_frame,
            placeholder_text="Search Product"
        )
        self.product_search.pack(side="left", padx=10)

        add_btn = ctk.CTkButton(top_frame, text="Add Product")
        add_btn.pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = (
            "Product",
            "Qty",
            "Price",
            "GST",
            "Total"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)

        summary = ctk.CTkFrame(parent)
        summary.pack(fill="x", padx=20)

        subtotal = ctk.CTkLabel(summary, text="Subtotal : ₹5000")
        subtotal.pack(anchor="e", padx=20, pady=5)

        gst = ctk.CTkLabel(summary, text="GST : ₹900")
        gst.pack(anchor="e", padx=20, pady=5)

        total = ctk.CTkLabel(
            summary,
            text="Grand Total : ₹5900",
            font=("Segoe UI", 18, "bold")
        )
        total.pack(anchor="e", padx=20, pady=10)
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill="x", padx=20, pady=20)

        generate_btn = ctk.CTkButton(btn_frame, text="Generate Invoice")
        generate_btn.pack(side="left", padx=10)

        print_btn = ctk.CTkButton(btn_frame, text="Print")
        print_btn.pack(side="left", padx=10)

        email_btn = ctk.CTkButton(btn_frame, text="Email Invoice")
        email_btn.pack(side="left", padx=10)