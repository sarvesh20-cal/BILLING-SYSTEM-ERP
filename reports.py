import customtkinter as ctk
from tkinter import ttk

class ReportsPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Reports & Analytics",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=20)

        from_date = ctk.CTkEntry(
            filter_frame,
            placeholder_text="From Date"
        )
        from_date.pack(side="left", padx=10, pady=10)

        to_date = ctk.CTkEntry(
            filter_frame,
            placeholder_text="To Date"
        )
        to_date.pack(side="left", padx=10)

        generate = ctk.CTkButton(
            filter_frame,
            text="Generate Report"
        )
        generate.pack(side="left", padx=10)

        graph = ctk.CTkFrame(parent, height=300)
        graph.pack(fill="x", padx=20, pady=20)

        graph_label = ctk.CTkLabel(
            graph,
            text="Sales Graph Area"
        )
        graph_label.pack(pady=120)

        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Invoice",
            "Customer",
            "Amount",
            "Date"
        )

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill="both", expand=True)
