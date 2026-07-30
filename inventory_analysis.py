from database_helper import DatabaseHelper


class InventoryAnalysis:

    def __init__(self):
        self.db = DatabaseHelper()

    # -------------------------------------
    # Inventory Health Score
    # -------------------------------------
    def inventory_health_score(self):

        total = self.db.get_total_products()

        if total == 0:
            return 0

        low = len(self.db.get_low_stock())
        out = len(self.db.get_out_of_stock())

        score = 100 - ((low * 3) + (out * 5))

        if score < 0:
            score = 0

        return score

    # -------------------------------------
    # Inventory Status
    # -------------------------------------
    def inventory_status(self):

        score = self.inventory_health_score()

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Good"

        elif score >= 50:
            return "Average"

        return "Poor"

    # -------------------------------------
    # Inventory Value
    # -------------------------------------
    def inventory_value(self):

        return self.db.get_inventory_value()

    # -------------------------------------
    # Highest Profit Product
    # -------------------------------------
    def highest_profit_product(self):

        return self.db.get_highest_profit()

    # -------------------------------------
    # Highest Stock Product
    # -------------------------------------
    def highest_stock_product(self):

        return self.db.get_highest_stock()

    # -------------------------------------
    # Low Stock List
    # -------------------------------------
    def low_stock_products(self):

        return self.db.get_low_stock()

    # -------------------------------------
    # Out Of Stock
    # -------------------------------------
    def out_of_stock_products(self):

        return self.db.get_out_of_stock()

    # -------------------------------------
    # AI Suggestions
    # -------------------------------------
    def ai_suggestions(self):

        suggestions = []

        if len(self.db.get_out_of_stock()) > 0:
            suggestions.append(
                "Restock products that are out of stock."
            )

        if len(self.db.get_low_stock()) > 0:
            suggestions.append(
                "Increase inventory for low stock products."
            )

        if self.inventory_health_score() > 90:
            suggestions.append(
                "Inventory health is excellent."
            )

        if self.inventory_value() < 10000:
            suggestions.append(
                "Inventory value is low. Consider purchasing more products."
            )

        if len(suggestions) == 0:
            suggestions.append(
                "Inventory is performing well."
            )

        return suggestions

    # -------------------------------------
    # Dashboard Summary
    # -------------------------------------
    def dashboard_summary(self):

        return {

            "total_products":
                self.db.get_total_products(),

            "inventory_value":
                self.inventory_value(),

            "health_score":
                self.inventory_health_score(),

            "status":
                self.inventory_status(),

            "highest_profit":
                self.highest_profit_product(),

            "highest_stock":
                self.highest_stock_product(),

            "low_stock":
                self.low_stock_products(),

            "out_of_stock":
                self.out_of_stock_products(),

            "suggestions":
                self.ai_suggestions()

        }