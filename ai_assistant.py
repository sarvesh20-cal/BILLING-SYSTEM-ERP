import customtkinter as ctk
from database_helper import DatabaseHelper


class AIAssistant(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.db = DatabaseHelper()

        title = ctk.CTkLabel(
            self,
            text="🤖 AI Inventory Assistant",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=15)

        self.entry = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Ask something... (e.g. show low stock)"
        )
        self.entry.pack(pady=10)

        ask_btn = ctk.CTkButton(
            self,
            text="Ask AI",
            command=self.process_question
        )
        ask_btn.pack(pady=5)

        self.output = ctk.CTkTextbox(
            self,
            width=700,
            height=400
        )
        self.output.pack(padx=20, pady=20, fill="both", expand=True)

    def process_question(self):

        question = self.entry.get().strip().lower()

        self.output.delete("1.0", "end")

        if question == "show low stock":

            products = self.db.get_low_stock()

            if not products:
                self.output.insert("end", "No low stock products found.")
                return

            self.output.insert("end", "📦 Low Stock Products\n\n")

            for p in products:
                self.output.insert(
                    "end",
                    f"{p['product_name']} - Stock: {p['stock_quantity']}\n"
                )

        elif question == "inventory value":

            value = self.db.get_inventory_value()

            self.output.insert(
                "end",
                f"💰 Total Inventory Value\n\n₹{value:,.2f}"
            )

        elif question == "highest profit":

            product = self.db.get_highest_profit()

            if product:
                self.output.insert(
                    "end",
                    f"""🏆 Highest Profit Product

Name : {product['product_name']}

Purchase Price : ₹{product['purchase_price']}

Selling Price : ₹{product['selling_price']}

Profit : ₹{product['profit']}
"""
                )

        elif question == "highest stock":

            product = self.db.get_highest_stock()

            if product:
                self.output.insert(
                    "end",
                    f"""📦 Highest Stock Product

Name : {product['product_name']}

Stock : {product['stock_quantity']}
"""
                )

        elif question == "out of stock":

            products = self.db.get_out_of_stock()

            if not products:
                self.output.insert("end", "No out-of-stock products.")
                return

            self.output.insert("end", "❌ Out Of Stock\n\n")

            for p in products:
                self.output.insert(
                    "end",
                    p["product_name"] + "\n"
                )

        elif question.startswith("find"):

            keyword = question.replace("find", "").strip()

            result = self.db.search_product(keyword)

            if not result:
                self.output.insert(
                    "end",
                    "No matching product found."
                )
                return

            for p in result:

                self.output.insert(
                    "end",
                    f"""
Product : {p['product_name']}
Stock : {p['stock_quantity']}
Selling Price : ₹{p['selling_price']}
Status : {p['status']}
-----------------------------
"""
                )

        else:

            self.output.insert(
                "end",
                """I can answer:

show low stock

inventory value

highest profit

highest stock

out of stock

find laptop

find soap

find milk
"""
            )