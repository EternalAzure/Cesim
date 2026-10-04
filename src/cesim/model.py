from typing import Any, Literal
from dataclasses import dataclass

from .product import Product, Phone
from .market import Market



class Forecast:

    def __init__(self, households_size:float, high_end_households_size:float, companies_size:float, high_end_companies_size:float) -> None:
        self.households_size = households_size
        self.high_end_households_size = high_end_households_size
        self.companies_size = companies_size
        self.high_end_companies_size = high_end_companies_size


@dataclass
class PreferenceDistribution:
    # -- DESIGN -- #
    h_sport:float
    h_avant_garde:float
    h_classic:float

    hh_sport:float
    hh_avant_garde:float
    hh_classic:float

    c_sport:float
    c_avant_garde:float
    c_classic:float

    hc_sport:float
    hc_avant_garde:float
    hc_classic:float

    # -- FEATURES -- #
    h_camera:float
    h_memory:float
    h_display:float
    h_resistance:float
    h_security:float

    hh_camera:float
    hh_memory:float
    hh_display:float
    hh_resistance:float
    hh_security:float

    c_camera:float
    c_memory:float
    c_display:float
    c_resistance:float
    c_security:float

    hc_camera:float
    hc_memory:float
    hc_display:float
    hc_resistance:float
    hc_security:float


    def design_multipliers(self, design:Literal["Classic", "Avant garde", "Sport"]):
        """Return h, hh, c, hc multipliers"""
        if design == "Classic": return self.h_classic, self.hh_classic, self.c_classic, self.hc_classic
        if design == "Avant garde": return self.h_avant_garde, self.hh_avant_garde, self.c_avant_garde, self.hc_avant_garde
        if design == "Sport": return self.h_sport, self.hh_sport, self.c_sport, self.hc_sport


@dataclass
class MarketDistribution:

    h_distribution:float
    hh_distribution:float
    c_distribution:float
    hc_distribution:float

@dataclass
class ManufacturingCosts:

    euro_performance_min:float
    euro_performance_max:float
    euro_battery_min:float
    euro_battery_max:float
    
    euro_camera:float
    euro_memory:float
    euro_display:float
    euro_resistance:float
    euro_security:float

    tech_performance:float
    tech_battery:float

    tech_camera:float
    tech_memory:float
    tech_display:float
    tech_resistance:float
    tech_security:float


@dataclass
class PriceModel:

    average_price:float
    h_average_price:float
    hh_average_price:float
    c_average_price:float
    hc_average_price:float

    price_slots:list[float]
    h_dispersion_to_slots:list[float]
    hh_dispersion_to_slots:list[float]
    c_dispersion_to_slots:list[float]
    hc_dispersion_to_slots:list[float]

    _average_price = 338.59


    @property
    def _original_average(self) -> float:
        return self._average_price


    def market_slot_index(self, price:float) -> int:
        """Market is divided into 11 parts on price scale.
        Returns nearest price bucket."""
        breakpoint()
        prices = [num * (self.average_price / self._original_average) for num in self.price_slots]
        correct_price_bucket = min(prices, key=lambda x:abs(x-price))
        return self.price_slots.index(correct_price_bucket)


class PriceSlot:

    def __init__(self, 
                 market_distribution:MarketDistribution, 
                 pref_distribution:PreferenceDistribution,
                 price_model:PriceModel,
                 manufacturing:ManufacturingCosts) -> None:
    
        self.products:list[Product] = []
        self.pref_distribution = pref_distribution
        self.market_distribution = market_distribution

        self.tech_floor = 0                 # How much specs the best phone has
        self.performance_floor = 0          # How much performance the best phone has
        self.battery_floor = 0              # How much battery the best phone has

        self.designs = set()                # Designs present in this slot
        self.features = set()               # Features present in thin slot

        self.occupancy_percent = 0          # Percentage of market covered by phones on this slot
        self.last_sales:float = 0           # Sales last round

        self.sales_forecast:float = 0       # Forecast

    def add_product(self, product:Product):
        self.products.append(product)

        if product.performance > self.performance_floor: self.performance_floor = product.performance
        if product.battery > self.battery_floor: self.battery_floor = product.battery
        if product.battery + product.performance > self.tech_floor: self.tech_floor = product.battery + product.performance

        self.designs.add(product.design)

        if product.camera: self.features.add("camera")
        if product.memory: self.features.add("memory")
        if product.display: self.features.add("display")
        if product.resistance: self.features.add("resistance")
        if product.security: self.features.add("security")

    def niche(self):
        pass


class AdvertizingModel:

    def __init__(self) -> None:

        # -- ADVERTIZING -- #
        self.money_to_awareness_h =  0.50  
        self.money_to_awareness_hh = 0.50  
        self.money_to_awareness_c =  0.50  
        self.money_to_awareness_hc = 0.50  

        self.awareness_to_intentions_h =    0.50
        self.awareness_to_intentions_hh =   0.50
        self.awareness_to_intentions_c =    0.50
        self.awareness_to_intentions_hc =   0.50

        self.intentions_to_sales_h =    0.50
        self.intentions_to_sales_hh =   0.50
        self.intentions_to_sales_c =    0.16
        self.intentions_to_sales_hc =   0.40

        self.channel_investment_effect = 0.01828 # rounds: 1.01166, 1.02456, 1.01862








class Simulation:

    manufacturing = ManufacturingCosts(
        euro_performance_min=0.08,
        euro_performance_max=1.08,
        euro_battery_min=0.09,    
        euro_battery_max=1.25,    
        euro_camera=9.77,
        euro_memory=9.77,
        euro_display=9.77,
        euro_resistance=9.77,
        euro_security=9.77,

        tech_camera=6,
        tech_memory=6,
        tech_display=1,
        tech_resistance=7,
        tech_security=2,

        tech_battery=0.25,
        tech_performance=0.25,  
    )

    preferences_europe = PreferenceDistribution(
        # -- DESIGN -- #
        h_sport = 0.772870196,
        h_avant_garde = 0.205001331,
        h_classic = 0.022128473,

        hh_sport = 0.607984746,
        hh_avant_garde = 0.362362506,
        hh_classic = 0.029652747,

        c_sport = 0.742393034,
        c_avant_garde = 0.216810224,
        c_classic = 0.040796742,

        hc_sport = 0.716051438,
        hc_avant_garde = 0.2324691,
        hc_classic = 0.051479462,

        # -- FEATURES -- #
        h_camera = 94.69,
        h_memory = 70.6,
        h_display = 32.28,
        h_resistance = 28.33,
        h_security = 70.33,

        hh_camera = 91.6,
        hh_memory = 70.39,
        hh_display = 18.15,
        hh_resistance = 26.14,
        hh_security = 79.93,

        c_camera = 86.6,
        c_memory = 61.84,
        c_display = 21.51,
        c_resistance = 31.08,
        c_security = 84.53,

        hc_camera = 76.64,
        hc_memory = 56.4,
        hc_display = 14.02,
        hc_resistance = 27.44,
        hc_security = 91.48,
    )

    price_model_europe = PriceModel(
        average_price = 338.59,
        h_average_price = 316,
        hh_average_price = 336,
        c_average_price = 338,
        hc_average_price = 360,

        price_slots = [265, 286, 308, 329, 350, 371, 393, 414, 435, 456, 478],
        h_dispersion_to_slots = [25, 22, 17, 14, 9, 6, 3, 2, 3, 1, 0],
        hh_dispersion_to_slots = [10, 19, 20, 14, 13, 8, 4, 3, 5, 2, 1],
        c_dispersion_to_slots = [12, 18, 16, 16, 11, 7, 5, 4, 5, 4, 2],
        hc_dispersion_to_slots = [5, 13, 14, 14, 12, 8, 8, 8, 7, 8, 3],
    )

    advertizing_model = AdvertizingModel()

    def play(self, phone:Phone) -> float:
        h_sales_forecast_eu = 2185.1
        hh_sales_forecast_eu = 1319.1
        c_sales_forecast_eu = 891
        hc_sales_forecast_eu = 1231.4

        h_sales_forecast_asia = 1706.7
        hh_sales_forecast_asia = 869.9
        c_sales_forecast_asia = 798
        hc_sales_forecast_asia = 941.3

        h_sales_forecast_per_price_slot = [round(h_sales_forecast_eu * percent) for percent in self.price_model_europe.h_dispersion_to_slots]
        hh_sales_forecast_per_price_slot = [round(hh_sales_forecast_eu * percent) for percent in self.price_model_europe.hh_dispersion_to_slots]
        c_sales_forecast_per_price_slot = [round(c_sales_forecast_eu * percent) for percent in self.price_model_europe.c_dispersion_to_slots]
        hc_sales_forecast_per_price_slot = [round(hc_sales_forecast_eu * percent) for percent in self.price_model_europe.hc_dispersion_to_slots]

        price_slot_index = self.price_model_europe.market_slot_index(phone.price)
        h_available_customers_based_on_price_slot: float = h_sales_forecast_per_price_slot[price_slot_index]
        hh_available_customers_based_on_price_slot: float = hh_sales_forecast_per_price_slot[price_slot_index]
        c_available_customers_based_on_price_slot: float = c_sales_forecast_per_price_slot[price_slot_index]
        hc_available_customers_based_on_price_slot: float = hc_sales_forecast_per_price_slot[price_slot_index]

        h_design_multiplier, hh_design_multiplier, c_design_multiplier, hc_design_multiplier = self.preferences_europe.design_multipliers(phone.design)
        h_available_customers_based_on_design: float = h_available_customers_based_on_price_slot * h_design_multiplier
        hh_available_customers_based_on_design: float = hh_available_customers_based_on_price_slot * hh_design_multiplier
        c_available_customers_based_on_design: float = c_available_customers_based_on_price_slot * c_design_multiplier
        hc_available_customers_based_on_design: float = hc_available_customers_based_on_price_slot * hc_design_multiplier




