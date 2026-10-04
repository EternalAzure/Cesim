from dataclasses import dataclass
from typing import Literal

@dataclass
class Phone:
    price:float
    variable_unit_cost:float

    performance:int
    battery:int
    camera:bool
    memory:bool
    display:bool
    resistance:bool
    security:bool
    design:Literal["Classic", "Avant garde", "Sport"]

@dataclass
class Product:

    name:str
    brand:str
    price:float
    variable_unit_cost:float

    # Sales
    households_sales:float
    high_end_households_sales:float
    companies_sales:float
    high_end_companies_sales:float
    total_sales:float

    # Sales by distribution channel
    specialist:float
    generalist:float
    online:float
    
    # Market share %
    households_market_share: float
    high_end_households_market_share: float
    companies_market_share: float
    high_end_companies_market_share: float
    
    # Marketing
    advertizing:float
    channel_investments:float

    # Product characteristics
    performance:int
    battery:int
    camera:bool
    memory:bool
    display:bool
    resistance:bool
    security:bool
    design:str

    # Awareness & Intention
    households_awareness:float
    high_end_households_awareness:float
    companies_awareness:float
    high_end_companies_awareness:float

    households_intention:float
    high_end_households_intention:float
    companies_intention:float
    high_end_companies_intention:float


    def __post_init__(self):
        self.households_sales = round(self.households_sales, 2)
        self.high_end_households_sales = round(self.high_end_households_sales, 2)
        self.companies_sales = round(self.companies_sales, 2)
        self.high_end_companies_sales = round(self.high_end_companies_sales, 2)
        self.total_sales = round(self.total_sales, 2)
        
        self.margin = self.price - self.variable_unit_cost
        self.margin_percent = self.margin / self.variable_unit_cost
        self.performance_per_euro = self.performance / self.price
        self.battery_per_euro = self.battery / self.price
        self.total_awareness = self.households_awareness + self.high_end_households_awareness + self.companies_awareness + self.high_end_companies_awareness
        self.total_intentions = self.households_intention + self.high_end_households_intention + self.companies_intention + self.high_end_companies_intention
        self.profit = self.total_sales * self.margin

        self.audience = f"H{round(self.households_market_share)} HH{round(self.high_end_households_market_share)} C{round(self.companies_market_share)} HC{round(self.high_end_companies_market_share)}"



