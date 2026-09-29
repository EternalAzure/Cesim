from typing import Literal

from .product import Product


class Market:
    def __init__(self, products:list[Product]) -> None:
        self.products:list[Product] = products
        self.products.sort(key=lambda p: p.price)

    # -- PRODUCTS -- #

    def products_by_design(self, design:Literal["Classic", "Avant garde", "Sport"]):
        return [p for p in self.products if p.design == design]


    # -- PRICES -- #
    def min_price(self) -> float:
        prices = []
        for product in self.products:
            prices.append(product.price)
        return min(prices)

    def max_price(self) -> float:
        prices = []
        for product in self.products:
            prices.append(product.price)
        return max(prices)
            
    def median_price(self) -> float:
        prices = []
        for product in self.products:
            prices.append(product.price)
        prices.sort()

        size = len(prices)
        if size % 2 == 0:
            result = (prices[size//2 - 1] + prices[size//2]) / 2
        else:
            result = prices[size//2]
        return result
    
    def average_price(self) -> float:
        prices = []
        for product in self.products:
            prices.append(product.price)
        return sum(prices) / len(prices)

    def low_downscale_products(self):
        average = self.average_price()
        results = [p for p in self.products if p.price < 0.75 * average]
        return results

    def downscale_products(self):
        average = self.average_price()
        results = [p for p in self.products if p.price < average and p.price >= average * 0.75]
        return results

    def upscale_products(self):
        average = self.average_price()
        results = [p for p in self.products if p.price > average and p.price <= average * 1.25]
        return results

    def high_upscale_products(self):
        average = self.average_price()
        results = [p for p in self.products if p.price > 1.25 * average]
        return results


    # -- SALES -- #

    def all_total_sales(self):
        result = 0
        for product in self.products:
            result += product.total_sales
        return round(result, 2)

    # Sales by focus group
    def h_sales(self):
        result = 0
        for product in self.products:
            result += product.households_sales
        return round(result, 2)

    def hh_sales(self):
        result = 0
        for product in self.products:
            result += product.high_end_households_sales
        return round(result, 2)

    def c_sales(self):
        result = 0
        for product in self.products:
            result += product.companies_sales
        return round(result, 2)

    def hc_sales(self):
        result = 0
        for product in self.products:
            result += product.high_end_companies_sales
        return round(result, 2)

    # Sales by design
    def all_design_sales(self, design:Literal["Classic", "Avant garde", "Sport"]):
        result = 0
        for product in self.products:
            if product.design == design:
                result += product.total_sales
        return round(result, 2)

    # Focus group design sales
    def group_design_sales(self, design:Literal["Classic", "Avant garde", "Sport"], group:Literal["H", "HH", "C", "HC"]):
        result = 0
        for product in self.products:
            if product.design == design:
                if group == "H":
                    result += product.households_sales
                elif group == "HH":
                    result += product.high_end_households_sales
                elif group == "C":
                    result += product.companies_sales
                elif group == "HC":
                    result += product.high_end_companies_sales
        return result

    # Sales by feature
    def all_feature_sales(self, feature:Literal["camera", "memory", "display", "resistance", "security"]):
        result = 0
        for product in self.products:
            if feature == "camera" and product.camera:
                result += product.total_sales
            elif feature == "memory" and product.memory:
                result += product.total_sales
            elif feature == "display" and product.display:
                result += product.total_sales
            elif feature == "resistance" and product.resistance:
                result += product.total_sales
            elif feature == "security" and product.security:
                result += product.total_sales
            
        return round(result, 2)

    def group_feature_sales(self, feature:Literal["camera", "memory", "display", "resistance", "security"], group:Literal["H", "HH", "C", "HC"]):
        result = 0
        for product in self.products:
            sales = 0
            if group == "H":
                sales = product.households_sales
            elif group == "HH":
                sales = product.high_end_households_sales
            elif group == "C":
                sales = product.companies_sales
            elif group == "HC":
                sales = product.high_end_companies_sales

            if feature == "camera" and product.camera:
                result += sales
            elif feature == "memory" and product.memory:
                result += sales
            elif feature == "display" and product.display:
                result += sales
            elif feature == "resistance" and product.resistance:
                result += sales
            elif feature == "security" and product.security:
                result += sales
            
        return round(result, 2)
    
    def group_design_feature(self, group:Literal["H", "HH", "C", "HC"]):
        result = {
            "Classic": {
                "camera": 0.0, 
                "memory": 0.0,
                "display": 0.0,
                "resistance": 0.0,
                "security": 0.0
            },
            "Avant garde": {
                "camera": 0.0, 
                "memory": 0.0,
                "display": 0.0,
                "resistance": 0.0,
                "security": 0.0
            },
            "Sport": {
                "camera": 0.0, 
                "memory": 0.0,
                "display": 0.0,
                "resistance": 0.0,
                "security": 0.0
            },
        }

        for product in self.products:
            sales = 0
            if group == "H":
                sales = product.households_sales
            if group == "HH":
                sales = product.high_end_households_sales
            if group == "C":
                sales = product.companies_sales
            if group == "HC":
                sales = product.high_end_companies_sales

            if product.design == "Classic":
                if product.camera:
                    result["Classic"]["camera"] += sales
                if product.memory:
                    result["Classic"]["memory"] += sales
                if product.display:
                    result["Classic"]["display"] += sales
                if product.resistance:
                    result["Classic"]["resistance"] += sales
                if product.security:
                    result["Classic"]["security"] += sales
            
            elif product.design == "Avant garde":
                if product.camera:
                    result["Avant garde"]["camera"] += sales
                if product.memory:
                    result["Avant garde"]["memory"] += sales
                if product.display:
                    result["Avant garde"]["display"] += sales
                if product.resistance:
                    result["Avant garde"]["resistance"] += sales
                if product.security:
                    result["Avant garde"]["security"] += sales
            
            elif product.design == "Sport":
                if product.camera:
                    result["Sport"]["camera"] += sales
                if product.memory:
                    result["Sport"]["memory"] += sales
                if product.display:
                    result["Sport"]["display"] += sales
                if product.resistance:
                    result["Sport"]["resistance"] += sales
                if product.security:
                    result["Sport"]["security"] += sales

        classic_sales = 0
        avant_sales = 0
        sport_sales = 0
        if group == "H":
            classic_sales = self.group_design_sales("Classic", "H")
            avant_sales = self.group_design_sales("Avant garde", "H")
            sport_sales = self.group_design_sales("Sport", "H")
        if group == "HH":
            classic_sales = self.group_design_sales("Classic", "HH")
            avant_sales = self.group_design_sales("Avant garde", "HH")
            sport_sales = self.group_design_sales("Sport", "HH")
        if group == "C":
            classic_sales = self.group_design_sales("Classic", "C")
            avant_sales = self.group_design_sales("Avant garde", "C")
            sport_sales = self.group_design_sales("Sport", "C")
        if group == "HC":
            classic_sales = self.group_design_sales("Classic", "HH")
            avant_sales = self.group_design_sales("Avant garde", "HH")
            sport_sales = self.group_design_sales("Sport", "HH")
            
        result["Classic"]["camera"] = round(result["Classic"]["camera"] / classic_sales * 100)
        result["Classic"]["memory"] = round(result["Classic"]["memory"] / classic_sales * 100)
        result["Classic"]["display"] = round(result["Classic"]["display"] / classic_sales * 100)
        result["Classic"]["resistance"] = round(result["Classic"]["resistance"] / classic_sales * 100)
        result["Classic"]["security"] = round(result["Classic"]["security"] / classic_sales * 100)
        
        result["Avant garde"]["camera"] = round(result["Avant garde"]["camera"] / avant_sales * 100)
        result["Avant garde"]["memory"] = round(result["Avant garde"]["memory"] / avant_sales * 100)
        result["Avant garde"]["display"] = round(result["Avant garde"]["display"] / avant_sales * 100)
        result["Avant garde"]["resistance"] = round(result["Avant garde"]["resistance"] / avant_sales * 100)
        result["Avant garde"]["security"] = round(result["Avant garde"]["security"] / avant_sales * 100)
        
        result["Sport"]["camera"] = round(result["Sport"]["camera"] / sport_sales * 100)
        result["Sport"]["memory"] = round(result["Sport"]["memory"] / sport_sales * 100)
        result["Sport"]["display"] = round(result["Sport"]["display"] / sport_sales * 100)
        result["Sport"]["resistance"] = round(result["Sport"]["resistance"] / sport_sales * 100)
        result["Sport"]["security"] = round(result["Sport"]["security"] / sport_sales * 100)

        return result


    def all_performance_per_euro_sales(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.performance_per_euro())

        sales = [p.total_sales for p in source]
        ppe = [p.performance_per_euro() for p in source]
        return sales, ppe

    def group_performance_per_euro_sales(self, group:Literal["H", "HH", "C", "HC"]):
        source = self.products.copy()
        source.sort(key=lambda p: p.performance_per_euro())

        if group == "H":
            sales = [p.households_market_share for p in source]
        elif group == "HH":
            sales = [p.high_end_households_market_share for p in source]
        elif group == "C":
            sales = [p.companies_market_share for p in source]
        elif group == "HC":
            sales = [p.high_end_companies_market_share for p in source]
        else: 
            raise ValueError(f"Invalid value for group {group=}")

        ppe = [p.performance_per_euro() for p in source]
        return sales, ppe


    def all_battery_per_euro_sales(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.battery_per_euro())

        sales = [p.total_sales for p in source]
        ppe = [p.battery_per_euro() for p in source]
        return sales, ppe

    def group_battery_per_euro_sales(self, group:Literal["H", "HH", "C", "HC"]):
        source = self.products.copy()
        source.sort(key=lambda p: p.battery_per_euro())

        if group == "H":
            sales = [p.households_market_share for p in source]
        elif group == "HH":
            sales = [p.high_end_households_market_share for p in source]
        elif group == "C":
            sales = [p.companies_market_share for p in source]
        elif group == "HC":
            sales = [p.high_end_companies_market_share for p in source]
        else:
            raise ValueError(f"Invalid value for group {group=}")

        ppe = [p.battery_per_euro() for p in source]
        return sales, ppe

        source = self.products.copy()
        source.sort(key=lambda p: p.battery_per_euro())

        sales = [p.high_end_companies_market_share for p in source]
        ppe = [p.battery_per_euro() for p in source]
        return sales, ppe