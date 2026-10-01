from collections import namedtuple
from typing import Any, Literal
import copy

from .product import Product

YLimit = namedtuple("YLimit", ["group", "design", "feature", "total"])

class Stats:

    def __init__(self, products: list[Product]) -> None:
        self.products = products.copy()

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
    
    def average_price(self) -> float:
        prices = []
        total_sales = 0
        for product in self.products:
            prices.append(product.price * product.total_sales)
            total_sales += product.total_sales
        return sum(prices) / total_sales

    # -- PERFORMANCE & BATTERY -- #
    def min_performance(self) -> float:
        return min([p.performance for p in self.products])

    def max_performance(self) -> float:
        return max([p.performance for p in self.products])
            
    def median_performance(self) -> float:
        performance = []
        for product in self.products:
            performance.append(product.price)
        performance.sort()

        size = len(performance)
        if size % 2 == 0:
            result = (performance[size//2 - 1] + performance[size//2]) / 2
        else:
            result = performance[size//2]
        return result
    
    def average_performance(self) -> float:
        return sum([p.performance for p in self.products]) / len(self.products)

    def low_performance(self) -> float:
        return (self.min_performance() + self.average_performance()) / 2

    def high_performance(self) -> float:
        return (self.max_performance() + self.average_performance()) / 2

    def min_battery(self) -> float:
        return min([p.battery for p in self.products])

    def max_battery(self) -> float:
        return max([p.battery for p in self.products])
            
    def median_battery(self) -> float:
        battery = []
        for product in self.products:
            battery.append(product.price)
        battery.sort()

        size = len(battery)
        if size % 2 == 0:
            result = (battery[size//2 - 1] + battery[size//2]) / 2
        else:
            result = battery[size//2]
        return result
    
    def average_battery(self) -> float:
        return sum([p.battery for p in self.products]) / len(self.products)

    def low_battery(self) -> float:
        return (self.min_battery() + self.average_battery()) / 2

    def high_battery(self) -> float:
        return (self.max_battery() + self.average_battery()) / 2
    

class Market:

    def __init__(self, products:list[Product]) -> None:
        self.total: float = sum([p.total_sales for p in products])
        self.products = products
        self.products.sort(key=lambda p: p.price)
        self.stats: Stats = Stats(self.products.copy())

    # -- GROUP -- #
    def households(self) -> Market:
        return Market([self._only_household_sales(p) for p in self.products if p.households_sales > 0])
    
    def high_end_households(self) -> Market:
        return Market([self._only_high_end_household_sales(p) for p in self.products if p.high_end_households_sales > 0])
    
    def companies(self) -> Market:
        return Market([self._only_companies_sales(p) for p in self.products if p.companies_sales > 0])

    def high_end_companies(self) -> Market:
        return Market([self._only_high_end_companies_sales(p) for p in self.products if p.high_end_companies_sales > 0])

    # -- DESIGN -- #
    def classic(self) -> Market:
        return Market([p for p in self.products if p.design == "Classic"])
        
    def avant_garde(self) -> Market:
        return Market([p for p in self.products if p.design == "Avant garde"])
        
    def sport(self) -> Market:
        return Market([p for p in self.products if p.design == "Sport"])

    # -- FEATURE -- #
    def camera(self) -> Market:
        return Market([p for p in self.products if p.camera])
        
    def memory(self) -> Market:
        return Market([p for p in self.products if p.memory])
        
    def display(self) -> Market:
        return Market([p for p in self.products if p.display])
        
    def resistance(self) -> Market:
        return Market([p for p in self.products if p.resistance])
        
    def security(self) -> Market:
        return Market([p for p in self.products if p.security])

    # -- GRAPH -- #
    def y_lim(self) -> YLimit:
        """Returns largest sales numbers by main metrics"""
        largest_group_total: float = max([
            sum([p.households_sales for p in self.products]),
            sum([p.high_end_households_sales for p in self.products]),
            sum([p.companies_sales for p in self.products]),
            sum([p.high_end_companies_sales for p in self.products]),
        ])

        largest_design_total: float = max([
            sum([p.total_sales for p in self.products if p.design == "Classic"]),
            sum([p.total_sales for p in self.products if p.design == "Avant garde"]),
            sum([p.total_sales for p in self.products if p.design == "Sport"])
        ])

        largest_feature_total: float = max([
            sum([p.total_sales for p in self.products if p.camera]),
            sum([p.total_sales for p in self.products if p.memory]),
            sum([p.total_sales for p in self.products if p.display]),
            sum([p.total_sales for p in self.products if p.resistance]),
            sum([p.total_sales for p in self.products if p.security]),
        ])

        largest_product_total: float = max([p.total_sales for p in self.products])

        return YLimit(largest_group_total, largest_design_total, largest_feature_total, largest_product_total)

    def bestseller(self, group:Literal["H", "HH", "C", "HC"]|None=None):
        phones = self.products.copy()
        phones.sort(key=lambda p: p.total_sales)
        if group == "H":
            phones.sort(key=lambda p: p.households_sales)
        if group == "HH":
            phones.sort(key=lambda p: p.high_end_households_sales)
        if group == "C":
            phones.sort(key=lambda p: p.companies_sales)
        if group == "HC":
            phones.sort(key=lambda p: p.high_end_companies_sales)
        return phones[-1]


    def _only_household_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.households_sales
        new_product.high_end_households_sales = 0
        new_product.companies_sales = 0
        new_product.high_end_companies_sales = 0
        return new_product

    def _only_high_end_household_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.high_end_households_sales
        new_product.households_sales = 0
        new_product.companies_sales = 0
        new_product.high_end_companies_sales = 0
        return new_product

    def _only_companies_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.companies_sales
        new_product.households_sales = 0
        new_product.high_end_households_sales = 0
        new_product.high_end_companies_sales = 0
        return new_product

    def _only_high_end_companies_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.high_end_companies_sales
        new_product.households_sales = 0
        new_product.high_end_households_sales = 0
        new_product.companies_sales = 0
        return new_product

