from database import Database


class DatabaseHelper:

    def __init__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor(dictionary=True)

    # ----------------------------
    # Total Products
    # ----------------------------
    def get_total_products(self):
        self.cursor.execute(
            "SELECT COUNT(*) AS total FROM products"
        )
        return self.cursor.fetchone()["total"]

    # ----------------------------
    # Inventory Value
    # ----------------------------
    def get_inventory_value(self):
        self.cursor.execute("""
            SELECT
            SUM(stock_quantity * selling_price) AS total
            FROM products
        """)

        result = self.cursor.fetchone()

        if result["total"] is None:
            return 0

        return float(result["total"])

    # ----------------------------
    # Low Stock
    # ----------------------------
    def get_low_stock(self, limit=10):

        self.cursor.execute("""
            SELECT
            product_name,
            stock_quantity
            FROM products
            WHERE stock_quantity<=%s
            ORDER BY stock_quantity
        """, (limit,))

        return self.cursor.fetchall()

    # ----------------------------
    # Out Of Stock
    # ----------------------------
    def get_out_of_stock(self):

        self.cursor.execute("""
            SELECT
            product_name
            FROM products
            WHERE stock_quantity=0
        """)

        return self.cursor.fetchall()

    # ----------------------------
    # Highest Profit Product
    # ----------------------------
    def get_highest_profit(self):

        self.cursor.execute("""
            SELECT
            product_name,
            purchase_price,
            selling_price,
            (selling_price-purchase_price) AS profit
            FROM products
            ORDER BY profit DESC
            LIMIT 1
        """)

        return self.cursor.fetchone()

    # ----------------------------
    # Highest Stock Product
    # ----------------------------
    def get_highest_stock(self):

        self.cursor.execute("""
            SELECT
            product_name,
            stock_quantity
            FROM products
            ORDER BY stock_quantity DESC
            LIMIT 1
        """)

        return self.cursor.fetchone()

    # ----------------------------
    # Search Product
    # ----------------------------
    def search_product(self, keyword):

        search = "%" + keyword + "%"

        self.cursor.execute("""
            SELECT *
            FROM products
            WHERE product_name LIKE %s
            OR barcode LIKE %s
        """, (search, search))

        return self.cursor.fetchall()

    # ----------------------------
    # Close Connection
    # ----------------------------
    def close(self):

        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()