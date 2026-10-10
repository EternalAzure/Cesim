import warnings
from enum import Enum
from pprint import pprint
from typing import Any, Literal, Generator
from dataclasses import dataclass
from multipledispatch import dispatch
from abc import ABC, abstractmethod

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper


from .loader import load_markets
from .market import Market, MarketHistory
from .product import Product, Phone, TrainingPhone



class ModelName(Enum):
    E6 = "E6"
    E65M_4M = "E65M+4M"
    E65M = "E65M"
    E65 = "E65"
    E6_4M = "E6_4M"
    E6_4 = "E6+4"
    E5_4 = "E5+4"
    E5_4M = "E5+4M"
    E5 = "E5"

    A6 = "E6"
    A65M_4M = "E65M+4M"
    A65M = "E65M"
    A65 = "E65"
    A6_4M = "E6_4M"
    A6_4 = "E6+4"
    A5_4 = "E5+4"
    A5_4M = "E5+4M"
    A5 = "E5"



class DemandModel:

    def __init__(self) -> None:
        self.data:MarketHistory = load_markets()

    # -- EUROPE -- #
    @property
    def E6(self) -> Engine:
        products = []
        products += self._training_data(6, "Europe")
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E65M_4M(self) -> Engine:
        products = []
        products += self._training_data(6, "Europe")
        products += self._training_data(6, "Europe", 5, multiply=True)
        products += self._round_4_training_data(6, "Europe", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E65M(self) -> Engine:
        products = []
        products += self._training_data(6, "Europe")
        products += self._training_data(6, "Europe", 5, multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E65(self) -> Engine:
        products = []
        products += self._training_data(6, "Europe")
        products += self._training_data(6, "Europe", 5, multiply=False)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E6_4M(self) -> Engine:
        products = []
        products += self._training_data(6, "Europe")
        products += self._round_4_training_data(6, "Europe", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E5_4(self) -> Engine:
        products = []
        products += self._training_data(5, "Europe")
        products += self._round_4_training_data(5, "Europe")
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E5_4M(self) -> Engine:
        products = []
        products += self._training_data(5, "Europe")
        products += self._round_4_training_data(5, "Europe", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def E5(self) -> Engine:
        products = []
        products += self._training_data(5, "Europe")
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    # -- ASIA -- #
    @property
    def A6(self) -> Engine:
        products = []
        products += self._training_data(6, "Asia")
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A65M_4M(self) -> Engine:
        products = []
        products += self._training_data(6, "Asia")
        products += self._training_data(6, "Asia", 5, multiply=True)
        products += self._round_4_training_data(6, "Asia", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A65M(self) -> Engine:
        products = []
        products += self._training_data(6, "Asia")
        products += self._training_data(6, "Asia", 5, multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A65(self) -> Engine:
        products = []
        products += self._training_data(6, "Asia")
        products += self._training_data(6, "Asia", 5, multiply=False)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A6_4M(self) -> Engine:
        products = []
        products += self._training_data(6, "Asia")
        products += self._round_4_training_data(6, "Asia", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A5_4(self) -> Engine:
        products = []
        products += self._training_data(5, "Asia")
        products += self._round_4_training_data(5, "Asia", multiply=False)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A5_4M(self) -> Engine:
        products = []
        products += self._training_data(5, "Asia")
        products += self._round_4_training_data(5, "Asia", multiply=True)
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine

    @property
    def A5(self) -> Engine:
        products = []
        products += self._training_data(5, "Asia")
        market = Market(products)
        engine =  Engine_v1()
        engine.train(market)
        return engine


    def _training_data(self, base_rnd:int, area:Literal["Europe", "Asia"], rnd:int|None=None, multiply:bool=False) -> list[Product]:
        """Returns products multiplied to match base_rnd averages"""
        base_market = self.data.loc(base_rnd, area)
        if rnd is None:
            return base_market.products
        
        market = self.data.loc(rnd, area)

        avg_price_base = base_market.stats.average_price()
        avg_battery_base = base_market.stats.average_battery()
        avg_perf_base = base_market.stats.average_performance()

        avg_price = market.stats.average_price()
        avg_battery = market.stats.average_battery()
        avg_perf = market.stats.average_performance()

        if multiply:
            for phone in market.products:
                phone.price = round(phone.performance * (avg_price_base / avg_price))
                phone.battery = round(phone.performance * (avg_battery_base / avg_battery))
                phone.performance = round(phone.performance * (avg_perf_base / avg_perf))
                
                phone.households_sales = round(phone.households_sales * (base_market.households().total / market.households().total))
                phone.he_households_sales = round(phone.he_households_sales * (base_market.households().total / market.households().total))
                phone.companies_sales = round(phone.companies_sales * (base_market.households().total / market.households().total))
                phone.he_companies_sales = round(phone.he_companies_sales * (base_market.households().total / market.households().total))

        return market.products


    def _round_4_training_data(self, base_rnd:int, area:Literal["Europe", "Asia"], multiply=False) -> list[Product]:
        base_market = self.data.loc(base_rnd, area)
        market = self.data.loc(4, area)
        phones = []

        price_multiplier = (base_market.stats.average_price() / market.stats.average_price())
        perf_multiplier = (base_market.stats.average_performance() / market.stats.average_performance())
        battery_multiplier = (base_market.stats.average_battery() / market.stats.average_battery())
        h_multiplier = (base_market.households().total / market.households().total)
        hh_multiplier = (base_market.he_households().total / market.he_households().total)
        c_multiplier = (base_market.companies().total / market.companies().total)
        hc_multiplier = (base_market.he_companies().total / market.he_companies().total)
        total_multiplier = (base_market.total / market.total)

        if not multiply:
            price_multiplier = 1
            perf_multiplier = 1
            battery_multiplier = 1
            h_multiplier = 1
            hh_multiplier = 1
            c_multiplier = 1
            hc_multiplier = 1
            total_multiplier = 1

        phone_eu = Phone(
            round(345 * price_multiplier),
            225.64,
            round(120 * perf_multiplier),
            round(115 * battery_multiplier),
            0,
            0,
            True,
            True,
            False,
            False,
            True,
            "Sport",
            households_sales=3.6 * h_multiplier,
            he_households_sales=2.5 * hh_multiplier,
            companies_sales=4.5 * c_multiplier,
            he_companies_sales=5.1 * hc_multiplier,
            total_sales=15.6 * total_multiplier,
            brand="Pink",
            warranty=24
        )# type: ignore

        phone_asia = Phone(
            425,
            253.98,
            140,
            120,
            0,
            0,
            True,
            True,
            True,
            False,
            True,
            "Avant garde",
            households_sales=0.4 * (base_market.households().total / market.households().total),
            he_households_sales=2.8 * (base_market.households().total / market.households().total),
            companies_sales=1.1 * (base_market.households().total / market.households().total),
            he_companies_sales=6.3 * (base_market.households().total / market.households().total),
            total_sales=10.8 * (base_market.households().total / market.households().total),
            brand="Pink",
            warranty=24
        ) # type:ignore

        if area == "Europe": phones.append(phone_eu)
        if area == "Asia": phones.append(phone_asia)

        return phones # type:ignore





class Engine(ABC):

    @abstractmethod
    def predict(self, product:Product|Phone) -> tuple[float, float, float, float, float]:
        """Returns predicted sales for a given phone."""

    @abstractmethod
    def train(self, market: Market):
        """Train this instance with the data you want"""

    @abstractmethod
    def test(self, test_product: Product) -> tuple[float, float, float, float, float]:
        """Removes predicted product from training data and yields results from predict"""


class Engine_v1(Engine):
    """
    Simple version.
    
    Log price
    Battery
    Performance
    Advertizing
    Log1p Channel
    Dummy Design
    Features
    No warranty
    +
    Constant

    y = np.log(df["sales"])
    """
        
    #price_elasticity = self.model.params["log_price"]

    def __init__(self) -> None:
        self.market:Market
        self.h_model: RegressionResultsWrapper
        self.hh_model: RegressionResultsWrapper
        self.c_model: RegressionResultsWrapper
        self.hc_model: RegressionResultsWrapper


    def train(self, market: Market):
        """Train this instance with the data you want"""
        self.market = market
        self.h_model = self._make_model([self._product_to_training_data(p) for p in market.households().products])
        self.hh_model = self._make_model([self._product_to_training_data(p) for p in market.he_households().products])
        self.c_model = self._make_model([self._product_to_training_data(p) for p in market.companies().products])
        self.hc_model = self._make_model([self._product_to_training_data(p) for p in market.he_companies().products])


    def predict(self, product:Product|Phone) -> tuple[float, float, float, float, float]: # type: ignore
        """Predict demand for a product in a given market with model of your choice"""
        hypothetical = self._hypothetical(product)

        h_demand = float(
            np.exp(self.h_model.predict(hypothetical).iloc[0])
        )
        hh_demand = float(
            np.exp(self.hh_model.predict(hypothetical).iloc[0])
        )
        c_demand = float(
            np.exp(self.c_model.predict(hypothetical).iloc[0])
        )
        hc_demand = float(
            np.exp(self.hc_model.predict(hypothetical).iloc[0])
        )
        total = h_demand + hh_demand + c_demand + hc_demand
        
        return h_demand, hh_demand, c_demand, hc_demand, total


    def test(self, test_product:Product):

        # Remove tested product from training
        reduced_training_data = self.market.products.copy()
        for idx in range(len(reduced_training_data)):
            if test_product == reduced_training_data[idx]: 
                reduced_training_data.pop(idx)
                break
        self.train(Market(reduced_training_data))

        # Get results
        results = self.predict(test_product)

        # Reset training
        self.train(self.market)

        return results
            

    def _make_model(self, products:list[TrainingPhone]):
        df = pd.DataFrame({
            "price": [p.price for p in products],
            "battery": [p.battery for p in products],
            "performance": [p.performance for p in products],

            "advertizing": [p.advertizing for p in products],
            "channel": [p.channel for p in products],
            
            "is_avant": [p.is_avant for p in products],
            "is_sport": [p.is_sport for p in products],

            "camera": [p.camera for p in products],
            "memory": [p.memory for p in products],
            "display": [p.display for p in products],
            "resistance": [p.resistance for p in products],
            "security": [p.security for p in products],

            "warranty": [p.warranty for p in products],
            "sales": [p.sales for p in products],
        })

        X = pd.DataFrame({
            "price": df["price"],
            "battery": df["battery"],
            "performance": df["performance"],

            "advertizing": df["advertizing"],
            "channel": df["channel"],

            "is_sport": df["is_avant"],
            "is_avant": df["is_sport"],

            "camera": df["camera"],
            "memory": df["memory"],
            "display": df["display"],
            "resistance": df["resistance"],
            "security": df["security"],

            #"warranty": df["warranty"],
        })

        X = sm.add_constant(X)
        y = np.log(df["sales"])


        return sm.OLS(y, X).fit()


    def _hypothetical(self, phone:Product|Phone):
        hypothetical = pd.DataFrame({
            "log_price": [np.log(phone.price)],
            "battery": [phone.battery],
            "performance": [phone.performance],
            "advertizing": [phone.advertizing],
            "log_channel": [np.log1p(phone.channel_investments)],
            
            "design_Avant_garde": [
                float(phone.design == "Avant garde")
            ],
            "design_Sport": [
                float(phone.design == "Sport")
            ],

            "camera": [int(phone.camera)],
            "memory": [int(phone.memory)],
            "display": [int(phone.display)],
            "resistance": [int(phone.resistance)],
            "security": [int(phone.security)],
            #"warranty": [int(phone.warranty)],
        })
        return sm.add_constant(hypothetical, has_constant="add")


    def _product_to_training_data(self, product:Product) -> TrainingPhone:

        return TrainingPhone(
            np.log(product.price),

            product.performance,
            product.battery,

            product.advertizing,
            np.log1p(product.channel_investments),

            int(product.camera),
            int(product.memory),
            int(product.display),
            int(product.resistance),
            int(product.security),

            float(product.design == "Avant garde"),
            float(product.design == "Sport"),

            product.total_sales,

            product.warranty,
        )