from typing import Any, Literal
from dataclasses import dataclass
from pprint import pprint
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper
import pandas as pd
import numpy as np
from pprint import pprint
from multipledispatch import dispatch

import warnings
warnings.filterwarnings("ignore")

from .product import Product, Phone, TrainingPhone
from .market import Market, MarketHistory
from .loader import load_markets



class DemandModel:
        
    #price_elasticity = self.model.params["log_price"]

    def __init__(self) -> None:
        self.market:Market
        self.h_model: RegressionResultsWrapper
        self.hh_model: RegressionResultsWrapper
        self.c_model: RegressionResultsWrapper
        self.hc_model: RegressionResultsWrapper



    def data(self) -> MarketHistory:
        """Load market history for training"""
        return load_markets()

    def train(self, market: Market):
        """Train this instance with the data you want"""
        self.market = market
        self.h_model = self._make_model([self._product_to_training_data(p) for p in market.households().products])
        self.hh_model = self._make_model([self._product_to_training_data(p) for p in market.he_households().products])
        self.c_model = self._make_model([self._product_to_training_data(p) for p in market.companies().products])
        self.hc_model = self._make_model([self._product_to_training_data(p) for p in market.he_companies().products])
        return self.h_model, self.hh_model, self.c_model, self.hc_model

    def predict(self, product:Product): # type: ignore
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
 
    def test(self, markets:list[Market]):
        """Test model trained on test data"""
        market = markets[0]
        for index in range(len(market.products)):
            print(f"{index=}")
            training_set = market.products.copy()
            product = training_set.pop(index)
            test_market = Market(training_set)

            h, hh, c, hc = self.train(Market(training_set))
            
            h_demand = self.predict(product)
            hh_demand = self.predict(product)
            c_demand = self.predict(product)
            hc_demand = self.predict(product)
            total = h_demand+hh_demand+c_demand+hc_demand

            


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

            "warranty": df["warranty"],
        })

        X = sm.add_constant(X)
        y = np.log(df["sales"])


        return sm.OLS(y, X).fit()

    def predict_demand(self, phone:Phone|Product):

        def make_hypothetical():
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
            })
            return sm.add_constant(hypothetical, has_constant="add")

        h_X = make_hypothetical()
        hh_X = make_hypothetical()
        c_X = make_hypothetical()
        hc_X = make_hypothetical()
        

        h_demand = float(
            np.exp(self.h_model.predict(h_X).iloc[0])
        )

        hh_demand = float(
            np.exp(self.hh_model.predict(hh_X).iloc[0])
        )

        c_demand = float(
            np.exp(self.c_model.predict(c_X).iloc[0])
        )

        hc_demand = float(
            np.exp(self.hc_model.predict(hc_X).iloc[0])
        )

        total_demand = h_demand + hh_demand + c_demand + hc_demand

        return h_demand, hh_demand, c_demand, hc_demand, total_demand

    def __make_model(self, market:Market):
        
        df = pd.DataFrame({
            "price": [p.price for p in market.products],
            "battery": [p.battery for p in market.products],
            "performance": [p.performance for p in market.products],
            "advertizing": [p.advertizing for p in market.products],
            "channel investments": [p.channel_investments for p in market.products],
            
            "design": [p.design for p in market.products],
            
            "camera": [int(p.camera) for p in market.products],
            "memory": [int(p.memory) for p in market.products],
            "display": [int(p.display) for p in market.products],
            "resistance": [int(p.resistance) for p in market.products],
            "security": [int(p.security) for p in market.products],

            "sales": [p.total_sales for p in market.products],
        })

        design_dummies = pd.get_dummies(
            df["design"],
            prefix="design",
            drop_first=True,
            dtype=float
        )

        X = pd.DataFrame({
            "log_price": np.log(df["price"]),
            "battery": df["battery"],
            "performance": df["performance"],
            "advertizing": df["advertizing"],
            "log_channel": np.log1p(df["channel investments"]),

            "camera": df["camera"],
            "memory": df["memory"],
            "display": df["display"],
            "resistance": df["resistance"],
            "security": df["security"],
        })
        X = pd.concat([X, design_dummies], axis=1)
        X = sm.add_constant(X)
        y = np.log(df["sales"])

        return sm.OLS(y, X).fit()

    def _hypothetical(self, phone:Product):
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
            "warranty": [int(phone.warranty)],
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