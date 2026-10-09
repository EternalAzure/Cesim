from dataclasses import dataclass
from typing import Literal

@dataclass
class Phone:
    price:float
    variable_unit_cost:float

    performance:int
    battery:int
    advertizing:float
    channel_investments:float

    camera:bool
    memory:bool
    display:bool
    resistance:bool
    security:bool
    
    design:Literal["Classic", "Avant garde", "Sport"]

    households_sales:float = 0
    he_households_sales:float = 0
    companies_sales:float = 0
    he_companies_sales:float = 0
    total_sales:float = 0
    brand:str = "Pink"

@dataclass
class RelativeTrainingPhone:
    price:float                 # price / market average
    cost:float                  # cost / price

    performance:float           # performance / market average
    battery:float               # battery / market average
    ppe:float                   # performance / price
    bpe:float                   # battery / price

    advertizing:float           # ads / population
    channel:float               # channel investments / population
    
    camera:int                  # 1 = yes
    memory:int                  # 1 = yes
    display:int                 # 1 = yes
    resistance:int              # 1 = yes
    security:int                # 1 = yes
    
    design:Literal["Classic", "Avant garde", "Sport"]

    sales:float                 # sales / market total sales
    brand_competition:float     # brands / 6
    product_competition:float   # products / 30

    warranty:int                # warranty

@dataclass
class TrainingPhone:
    price:float                 # price / market average

    performance:float           # performance / market average
    battery:float               # battery / market average

    advertizing:float           # ads / population
    channel:float               # channel investments / population
    
    camera:int                  # 1 = yes
    memory:int                  # 1 = yes
    display:int                 # 1 = yes
    resistance:int              # 1 = yes
    security:int                # 1 = yes
    
    is_avant:float
    is_sport:float

    sales:float                 # sales / market total sales

    warranty:int                # warranty

@dataclass
class Product:

    name:str
    brand:str
    price:float
    variable_unit_cost:float

    # Sales
    households_sales:float
    he_households_sales:float
    companies_sales:float
    he_companies_sales:float
    total_sales:float

    # Sales by distribution channel
    specialist:float
    generalist:float
    online:float
    
    # Market share %
    households_market_share: float
    he_households_market_share: float
    companies_market_share: float
    he_companies_market_share: float
    
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
    he_households_awareness:float
    companies_awareness:float
    he_companies_awareness:float

    households_intention:float
    he_households_intention:float
    companies_intention:float
    he_companies_intention:float

    # Warranty
    warranty:int


    def __post_init__(self):
        self.households_sales = round(self.households_sales, 2)
        self.he_households_sales = round(self.he_households_sales, 2)
        self.companies_sales = round(self.companies_sales, 2)
        self.he_companies_sales = round(self.he_companies_sales, 2)
        self.total_sales = round(self.total_sales, 2)
        
        self.margin = self.price - self.variable_unit_cost
        self.margin_percent = self.margin / self.variable_unit_cost
        self.performance_per_euro = self.performance / self.price
        self.battery_per_euro = self.battery / self.price
        self.total_awareness = self.households_awareness + self.he_households_awareness + self.companies_awareness + self.he_companies_awareness
        self.total_intentions = self.households_intention + self.he_households_intention + self.companies_intention + self.he_companies_intention
        self.profit = self.total_sales * self.margin

        self.audience = f"H{round(self.households_market_share)} HH{round(self.he_households_market_share)} C{round(self.companies_market_share)} HC{round(self.he_companies_market_share)}"



    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__): return False
        return self.name == value.name and self.brand == value.brand

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)