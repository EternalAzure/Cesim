from collections import namedtuple
from typing import Any, Literal
import copy
import numpy as np
import pandas as pd
import copy

from .product import Product


YLimit = namedtuple("YLimit", ["group", "design", "feature", "total"])


class MarketLocations:
    def __init__(self, europe:Market, asia:Market) -> None:
        self.europe = europe
        self.asia = asia
        self._nrounds = 2
        self._index = 0

    def __getitem__(self, key:Literal["europe", "asia"]):
        return self.__getattribute__(key)

    def __iter__(self):
        return self

    def __next__(self) -> Market:
        if self._index < self._nrounds:
            if self._index == 0:
                item = self.europe
            elif self._index == 1:
                item = self.asia
            else: raise IndexError()
            self._index += 1
            return item
        else:
            raise StopIteration
    

class MarketHistory:

    def __init__(self) -> None:
        self.europe: list[Market] = []
        self.asia: list[Market] = []
        self.columns = ("europe", "asia")
        self.rows = (1,2,3,4,5,6,7,8)
        self._index = 0
        self._nrounds = 6


    def add_round(self, europe:Market, asia:Market):
        self.europe.append(europe)
        self.asia.append(asia)

    def loc(self, row:int, column:str) -> Market:
        row -= 1
        if column.lower() == "europe":
            return copy.deepcopy(self.europe[row])
        if column.lower() == "asia":
            return copy.deepcopy(self.asia[row])
        raise ValueError()

    def row(self, index:int) -> tuple[Market, Market]:
        return (copy.deepcopy(self.europe[index]), copy.deepcopy(self.asia[index]))

    def column(self, name:str) -> list[Market]:
        if name == "europe":
            return copy.deepcopy(self.europe)
        elif name == "asia":
            return copy.deepcopy(self.asia)
        raise KeyError()

    def rounds(self):
        return self.IterRounds(copy.deepcopy(self.europe), copy.deepcopy(self.asia))

    class IterRounds:
        def __init__(self, europe:list[Market], asia:list[Market]) -> None:
            self._index = 0
            self._nrounds = 6
            self.europe = europe
            self.asia = asia

        def __iter__(self):
            return self

        def __next__(self) -> tuple[int, Market, Market]:
            if self._index < self._nrounds:
                item = (self._index+1, copy.deepcopy(self.europe[self._index]), copy.deepcopy(self.asia[self._index]))
                self._index += 1
                return item
            else:
                raise StopIteration


class Bins:

    def __init__(self, low:list[Product], mid:list[Product], high:list[Product]) -> None:
        self.low = Market(low)
        self.mid = Market(mid)
        self.high = Market(high)

class Companies:

    def __init__(self, 
                 pink:list[Product], green:list[Product], grey:list[Product], 
                 orange:list[Product], blue:list[Product], red:list[Product]) -> None:
        self.pink = Market(pink)
        self.green = Market(green)
        self.grey = Market(grey)
        self.orange = Market(orange)
        self.blue = Market(blue)
        self.red = Market(red)

    def __getitem__(self, key:str) -> Market:
        key = key.lower()
        if key not in ["pink", "green", "grey", "orange", "blue", "red"]:
            raise KeyError(f"No such company {key}")
        return self.__getattribute__(key)

class Groups:

    def __init__(self, 
                 households:Market, high_end_households:Market, companies:Market, 
                 high_end_companies:Market) -> None:
        self.households = households
        self.high_end_households =high_end_households
        self.companies = companies
        self.high_end_companies = high_end_companies

    def __getitem__(self, key:str) -> Market:
        key = key.lower()
        if key not in ["households", "high_end_households", "companies", "high_end_companies"]:
            raise KeyError(f"No such company {key}")
        return self.__getattribute__(key)

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
    def min_performance(self) -> int:
        return min([p.performance for p in self.products])

    def max_performance(self) -> int:
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

    def min_battery(self) -> int:
        return min([p.battery for p in self.products])

    def max_battery(self) -> int:
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

    # -- PPE & BPE -- #
    def average_ppe(self) -> float:
        return sum([p.performance_per_euro for p in self.products]) / len(self.products) 

    def average_bpe(self) -> float:
        return sum([p.battery_per_euro for p in self.products]) / len(self.products) 
    

class Market:

    def __init__(self, products:list[Product]) -> None:
        self.total: float = sum([p.total_sales for p in products])
        self.products = products
        self.products.sort(key=lambda p: p.price)
        self.stats: Stats = Stats(self.products.copy())
        self.brands: list[str] = list(set([p.brand for p in self.products]))

    # -- GROUP -- #
    def group(self) -> Groups:
        return Groups(
            households=self.households(), 
            high_end_households=self.he_households(), 
            companies=self.companies(), 
            high_end_companies=self.he_companies()
        )

    def households(self) -> Market:
        return Market([self._only_household_sales(p) for p in self.products if p.households_sales > 0])
    
    def he_households(self) -> Market:
        return Market([self._only_high_end_household_sales(p) for p in self.products if p.he_households_sales > 0])
    
    def companies(self) -> Market:
        return Market([self._only_companies_sales(p) for p in self.products if p.companies_sales > 0])

    def he_companies(self) -> Market:
        return Market([self._only_high_end_companies_sales(p) for p in self.products if p.he_companies_sales > 0])

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


    # -- SPECS -- #
    def performance(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.performance)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    def battery(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.battery)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    # -- ECONOMIC -- #
    def popularity(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.total_sales)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    def advertized(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.advertizing)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    def aware(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.total_awareness)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    def profitable(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.profit)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)

    def price(self):
        source = self.products.copy()
        source.sort(key=lambda p: p.price)
        low = source[:len(source) // 3]
        mid = source[len(source) // 3:-len(source) // 3]
        high = source[-len(source) // 3:]
        return Bins(low=low, mid=mid, high=high)


    # -- COMPANY -- #
    def brand(self):
        source = self.products.copy()
        pink = [p for p in source if p.brand == "Pink"]
        green = [p for p in source if p.brand == "Green"]
        grey = [p for p in source if p.brand == "Grey"]
        orange = [p for p in source if p.brand == "Orange"]
        blue = [p for p in source if p.brand == "Blue"]
        red = [p for p in source if p.brand == "Red"]

        return Companies(pink=pink, green=green, grey=grey, orange=orange, blue=blue, red=red)

    
    # -- GRAPH -- #
    def y_lim(self) -> YLimit:
        """Returns largest sales numbers by main metrics"""
        largest_group_total: float = max([
            sum([p.households_sales for p in self.products]),
            sum([p.he_households_sales for p in self.products]),
            sum([p.companies_sales for p in self.products]),
            sum([p.he_companies_sales for p in self.products]),
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
            phones.sort(key=lambda p: p.he_households_sales)
        if group == "C":
            phones.sort(key=lambda p: p.companies_sales)
        if group == "HC":
            phones.sort(key=lambda p: p.he_companies_sales)
        return phones[-1]


    def _only_household_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.households_sales
        new_product.he_households_sales = 0
        new_product.companies_sales = 0
        new_product.he_companies_sales = 0
        return new_product

    def _only_high_end_household_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.he_households_sales
        new_product.households_sales = 0
        new_product.companies_sales = 0
        new_product.he_companies_sales = 0
        return new_product

    def _only_companies_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.companies_sales
        new_product.households_sales = 0
        new_product.he_households_sales = 0
        new_product.he_companies_sales = 0
        return new_product

    def _only_high_end_companies_sales(self, product:Product) -> Product:
        new_product = copy.deepcopy(product)
        new_product.total_sales = product.he_companies_sales
        new_product.households_sales = 0
        new_product.he_households_sales = 0
        new_product.companies_sales = 0
        return new_product

