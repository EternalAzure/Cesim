import os
import copy
import random
from pprint import pprint
from typing import Any, Literal
from dataclasses import dataclass

import pyfiglet
import numpy as np
import pandas as pd
from tqdm import tqdm
from pprint import pprint
import statsmodels.api as sm
from contextlib import suppress
from simple_term_menu import TerminalMenu


from .product import Product, Phone
from .demand_model import DemandModel
from .market import Market, MarketHistory


class OverTechLimit(Exception):
    """Raised when phone exceeds tech limit"""


class SalesForecast:

    def __init__(self, households:float, high_end_households:float, companies:float, high_end_companies:float) -> None:
        self.households = households
        self.high_end_households = high_end_households
        self.companies = companies
        self.high_end_companies = high_end_companies


@dataclass
class ManufacturingCosts:
    perf_max:int
    battery_max:int

    base_cost:float

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

    def cost(self, phone:Phone):
        if self.is_over_tech_limit(phone): raise OverTechLimit("Over tech limit")
        cost = self.base_cost
        cost += self.euro_camera if phone.camera else 0
        cost += self.euro_memory if phone.memory else 0
        cost += self.euro_display if phone.display else 0
        cost += self.euro_resistance if phone.resistance else 0
        cost += self.euro_security if phone.security else 0
        cost += self._battery_cost(phone.battery)
        cost += self._perf_cost(phone.performance)
        return round(cost, 2)

    def is_over_tech_limit(self, phone:Phone):
        if phone.performance > self.perf_max: return True
        if phone.battery > self.battery_max: return True

        cost = 0
        cost += self.tech_camera if phone.camera else 0
        cost += self.tech_memory if phone.memory else 0
        cost += self.tech_display if phone.display else 0
        cost += self.tech_resistance if phone.resistance else 0
        cost += self.tech_security if phone.security else 0
        cost += phone.battery * self.tech_battery
        cost += phone.performance * self.tech_performance
        return cost > 100

    def _perf_cost(self, perf:int):
        if perf > self.perf_max: raise ValueError("Perf over max limit")
        x = [1,     2,    20,    35,   45,  50,    80,   110,  140,  170,  200,  230,  235]
        y = [0.07, 0.12, 0.13,  0.19, 0.17, 0.21, 0.27,  0.34, 0.43, 0.53, 0.65, 0.78, 0.8]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        return sum([p(x) for x in range(2, perf+1)])

    def _battery_cost(self, battery:int):
        if battery > self.battery_max: raise ValueError("Battery over max limit")
        x = [1,     2,    20,   35,   45,   50,   80,  110,   140,  170,  200,  230,  235]
        y = [0.09, 0.12, 0.16, 0.19, 0.22, 0.23, 0.31, 0.39, 0.49,  0.61, 0.74, 0.89, 0.93]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        return sum([p(x) for x in range(2, battery+1)])


class AdvertizingModel:

    def __init__(self, rounds:list[Market]) -> None:
        self.rounds = rounds
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

    def sales(self, money:float) -> float:
        """Kun datasta poistaa kaiken metelin jäljelle jää vain kaksi vakiokerrointa"""

        awareness = money * 0.3784200511324188
        intentions = awareness * 0.19653215763684906

        return intentions

    def awareness(self, round_:int):
        y_h = self.money_to_awareness([m.households() for m in self.rounds])
        y_hh = self.money_to_awareness([m.he_households() for m in self.rounds])
        y_c = self.money_to_awareness([m.companies() for m in self.rounds])
        y_hc = self.money_to_awareness([m.he_companies() for m in self.rounds])
        # Tismalleen sama tulos joka kohderyhmälle
        x = range(1, len(self.rounds)+1)

        z = np.polyfit(x, y_h, 1)
        p = np.poly1d(z)
        h_awareness:float = p(round_)

        z = np.polyfit(x, y_hh, 1)
        p = np.poly1d(z)
        hh_awareness:float = p(round_)

        z = np.polyfit(x, y_c, 1)
        p = np.poly1d(z)
        c_awareness:float = p(round_)

        z = np.polyfit(x, y_hc, 1)
        p = np.poly1d(z)
        hc_awareness:float = p(round_)

        deceleration_curve_x = [self.rounds[i].total for i in range(len(self.rounds))]
        deceleration_curve_y = []
        deceleration_curve_y.append(self._calc_k(self.rounds[0].total, self.rounds[1].total, p(0), p(1)))
        deceleration_curve_y.append(self._calc_k(self.rounds[1].total, self.rounds[2].total, p(1), p(2)))
        deceleration_curve_y.append(self._calc_k(self.rounds[2].total, self.rounds[3].total, p(2), p(3)))
        deceleration_curve_y.append(self._calc_k(self.rounds[3].total, self.rounds[4].total, p(3), p(4)))
        # Euroopassa väki kasvaa 975 joten markkinoinnin tehokkuus kasvaa 0.012136982765525103 per käytetty euro
        # Yhteensä 0.3784200511324188 per euro

        return 0.3784200511324188, 0.3784200511324188, 0.3784200511324188, 0.3784200511324188

    def _intentions(self, round_:int):
        y_h = self.awareness_to_intention([m.households() for m in self.rounds])
        y_hh = self.awareness_to_intention([m.he_households() for m in self.rounds])
        y_c = self.awareness_to_intention([m.companies() for m in self.rounds])
        y_hc = self.awareness_to_intention([m.he_companies() for m in self.rounds])

        x = range(1, len(self.rounds)+1)

        z = np.polyfit(x, y_h, 1)
        p = np.poly1d(z)
        h_intentions = p(round_)

        z = np.polyfit(x, y_hh, 1)
        p = np.poly1d(z)
        hh_intentions = p(round_)

        z = np.polyfit(x, y_c, 1)
        p = np.poly1d(z)
        c_intentions = p(round_)

        z = np.polyfit(x, y_hc, 1)
        p = np.poly1d(z)
        hc_intentions = p(round_)

        return h_intentions, hh_intentions, c_intentions, hc_intentions

    def money_to_awareness(self, rounds:list[Market]) -> list[float]:
        multipliers:list[list[float]] = []
        for round in rounds:
            money_to_awareness_multipliers = [
                self._money_to_awareness(round.brand().red.products),
                self._money_to_awareness(round.brand().blue.products),
                self._money_to_awareness(round.brand().orange.products),
                self._money_to_awareness(round.brand().grey.products),
                self._money_to_awareness(round.brand().pink.products),
                self._money_to_awareness(round.brand().green.products),
            ]
            multipliers.append(money_to_awareness_multipliers)

        all_values = [x for lst in multipliers for x in lst]
        inliers = self._remove_outliers(all_values, 4)

        median_values = [
            float(np.nanmedian([x for x in lst if x in inliers]))
            for lst in multipliers
        ]

        return median_values

    def _money_to_awareness(self, products:list[Product]):
        x = [p.advertizing for p in products]
        y = [p.total_awareness for p in products]
        if not x: return np.nan
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope

    def awareness_to_intention(self, rounds:list[Market]) -> list[float]:
        multipliers:list[list[float]] = []
        for round in rounds:
            awareness_to_intention_multipliers = [
                self._awareness_to_intentions(round.brand().red.products),
                self._awareness_to_intentions(round.brand().blue.products),
                self._awareness_to_intentions(round.brand().orange.products),
                self._awareness_to_intentions(round.brand().grey.products),
                self._awareness_to_intentions(round.brand().pink.products),
                self._awareness_to_intentions(round.brand().green.products),
            ]
            multipliers.append(awareness_to_intention_multipliers)

        all_values = [x for lst in multipliers for x in lst]
        inliers = self._remove_outliers(all_values, 4)

        median_values = [
            float(np.nanmedian([x for x in lst if x in inliers]))
            for lst in multipliers
        ]

        return median_values

    def _awareness_to_intentions(self, products:list[Product]):
        x = [p.total_awareness for p in products]
        y = [p.total_intentions for p in products]
        if not x: return np.nan
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope
    
    def _calc_k(self, x1, x2, y1, y2):
        """kulmakerroin"""
        if x1 == x2: return np.nan
        k = (y2-y1) / (x2-x1)
        return k

    def _remove_outliers(self,
        y: list[float],
        threshold: float = 4,
    ) -> list[float]:
        """
        Remove possible outliers from y using a robust MAD-based z-score.

        Parameters
        ----------
        y : list[float]
            Values to filter.
        threshold : float
            Robust z-score threshold. 5.0 is a conservative default.

        Returns
        -------
        list[float]
            Values with possible outliers removed.
        """

        if len(y) < 3:
            return y.copy()
        if np.count_nonzero(~np.isnan(y)) < 3:
            return y.copy()


        y_arr = np.asarray(y, dtype=float)

        median = np.nanmedian(y_arr)
        mad = np.nanmedian(np.abs(y_arr - median))

        # If all values are identical, there are no outliers.
        if mad == 0:
            return y.copy()

        robust_z = np.abs(y_arr - median) / (1.4826 * mad)
        return y_arr[robust_z <= threshold].tolist()



class Simulation:

    def __init__(self) -> None:

        self.manufacturing = ManufacturingCosts(
            perf_max=235,
            battery_max=235,
            base_cost=97.56,

            euro_performance_min=0.06,
            euro_performance_max=0.8,
            euro_battery_min=0.07,    
            euro_battery_max=0.93,    
            euro_camera=9.7,
            euro_memory=9.7,
            euro_display=9.7,
            euro_resistance=9.7,
            euro_security=9.7,

            tech_camera=4,
            tech_memory=5,
            tech_display=1,
            tech_resistance=5,
            tech_security=1,

            tech_battery=0.213,
            tech_performance=0.213,  
        )

    def main(self):
        # -- INTRO -- #
        os.system("clear")
        ascii_banner = pyfiglet.figlet_format("TelePink!")
        print(ascii_banner)
        print("Keep calm and scroll on", end="\n\n\n\n")

        # -- SIMULATION LOOP -- #
        options = ["Quit", "Test", "Generate"]
        terminal_menu = TerminalMenu(options)

        while True:
            entry_index = terminal_menu.show()
            if entry_index == 0:
                return
            elif entry_index == 1:
                return
            elif entry_index == 2:
                return


    def train_models(self, rnd:int, include:list[int]=[]):
        """Creates and trains models for europe and asia."""
        self.model_europe = DemandModel()
        self.model_asia = DemandModel()
        eu_data, asia_data = self.training_data(rnd, include)
        self.model_europe.train(Market(eu_data))
        self.model_asia.train(Market(asia_data))

        return self.model_europe, self.model_asia


    def generate_phones(self, rnd:int):
        eu_very_best_phones = []
        asia_very_best_phones = []

        #eu, asia = self.find_best_phones(rnd, 150, 200)
        #eu_best_200 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        #asia_best_200 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        #eu_very_best_phones.append(sorted(eu_best_200, key=lambda x: x["profit"])[-1])
        #asia_very_best_phones.append(sorted(asia_best_200, key=lambda x: x["profit"])[-1])
        
        eu, asia = self.find_best_phones(rnd, 201, 250)
        eu_best_250 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        asia_best_250 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        eu_very_best_phones.append(sorted(eu_best_250, key=lambda x: x["profit"])[-1])
        asia_very_best_phones.append(sorted(asia_best_250, key=lambda x: x["profit"])[-1])

        eu, asia = self.find_best_phones(rnd, 251, 300)
        eu_best_300 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        asia_best_300 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        eu_very_best_phones.append(sorted(eu_best_300, key=lambda x: x["profit"])[-1])
        asia_very_best_phones.append(sorted(asia_best_300, key=lambda x: x["profit"])[-1])

        eu, asia = self.find_best_phones(rnd, 301, 350)
        eu_best_350 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        asia_best_350 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        eu_very_best_phones.append(sorted(eu_best_350, key=lambda x: x["profit"])[-1])
        asia_very_best_phones.append(sorted(asia_best_350, key=lambda x: x["profit"])[-1])
  
        eu, asia = self.find_best_phones(rnd, 351, 400)
        eu_best_400 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        asia_best_400 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        eu_very_best_phones.append(sorted(eu_best_400, key=lambda x: x["profit"])[-1])
        asia_very_best_phones.append(sorted(asia_best_400, key=lambda x: x["profit"])[-1])
  
        eu, asia = self.find_best_phones(rnd, 401, 450)
        eu_best_450 = [self.optimize_advertizing(phone["phone"], rnd)[0] for phone in eu]
        asia_best_450 = [self.optimize_advertizing(phone["phone"], rnd)[1] for phone in asia]
        eu_very_best_phones.append(sorted(eu_best_450, key=lambda x: x["profit"])[-1])
        asia_very_best_phones.append(sorted(asia_best_450, key=lambda x: x["profit"])[-1])


        return eu_very_best_phones, asia_very_best_phones


    def find_best_phones(self, rnd:int, min_price:float=70, max_price:float=800, top:int=3):
        europe, asia = self.train_models(rnd)

        phones_eu:list[dict] = []
        phones_asia:list[dict] = []
        print("Optimizing Features")
        iterations = 0
        while len(phones_eu) < 300 and iterations < 50000:
            iterations += 1 # KILL SWITCH
            print(f"\rIterations: {iterations:6}  Phones: {len(phones_eu)}", end="")
            phone = self.create_random_phone()
            phone.price = round(phone.cost * 1.60)
            margin = phone.price - phone.cost
            if phone.price < min_price: continue
            if phone.price > max_price: continue


            h, hh, c, hc, total = europe.predict(phone)
            phone.households_sales = round(h)
            phone.he_households_sales = round(hh)
            phone.companies_sales = round(c)
            phone.he_companies_sales = round(hc)
            phone.total_sales = round(total)
            profit = round(total*margin)
            phones_eu.append({"phone": phone, "margin%": round(margin/phone.cost*100), "sales k": round(total), "profit": profit})

            h, hh, c, hc, total = asia.predict(phone)
            phone.households_sales = round(h)
            phone.he_households_sales = round(hh)
            phone.companies_sales = round(c)
            phone.he_companies_sales = round(hc)
            phone.total_sales = round(total)
            profit = round(total*margin)
            phones_asia.append({"phone": phone, "margin%": round(margin/phone.cost*100), "sales k": round(total), "profit": profit})
        print("")
        phones_eu.sort(key=lambda p: (p["profit"], p["margin%"]))
        phones_eu.reverse()
        phones_asia.sort(key=lambda p: (p["profit"], p["margin%"]))
        phones_asia.reverse()

        print(f"Generated {len(phones_eu)} phones")
        print(f"Took {top} best phones for Europe and Asia")
   
        return phones_eu[:top], phones_asia[:top]


    def optimize_advertizing(self, phone:Phone, rnd:int):
        europe, asia = self.train_models(rnd)

        phones_eu:list[dict] = []
        phones_asia:list[dict] = []
        print("Optimizing Advertizing")
        for _ in tqdm(range(1000)):
            new_phone = copy.deepcopy(phone)

            # ACCECTABLE METRICS
            operating_margin_limit = 17
            return_on_sales_limit = 22

            # GENERATE MARGIN
            unit_margin_percent = (random.randint(0, 15) + 155)
            new_phone.price = round(new_phone.cost * unit_margin_percent / 100)
            margin = new_phone.price - new_phone.cost

            # SPENT MARGIN ON ADVERTIZING
            ad_budget = round(random.uniform(0.067, 1.0) * 15000)
            new_phone.advertizing = ad_budget
            channel_investments = round(random.uniform(0.01, 1.0) * 4000)
            new_phone.channel_investments = channel_investments

            new_phone_eu = copy.deepcopy(new_phone)
            new_phone_asia = copy.deepcopy(new_phone)
            # ----  ----  ----  ---- #

            # PREDICT DEMAND, EUROPE
            h, hh, c, hc, total_eu = europe.predict(new_phone_eu)
            new_phone_eu.households_sales = round(h)
            new_phone_eu.he_households_sales = round(hh)
            new_phone_eu.companies_sales = round(c)
            new_phone_eu.he_companies_sales = round(hc)
            new_phone_eu.total_sales = round(total_eu)

            # CALCULATE PROFIT
            revenue_eu = round(total_eu * new_phone_eu.price)
            operating_costs_eu = round(total_eu * new_phone_eu.cost + ad_budget + channel_investments)
            profit_eu = round(revenue_eu - operating_costs_eu)
            operating_margin_eu = round(profit_eu / operating_costs_eu * 100)
            return_on_sales_eu = round(profit_eu / total_eu * 100)

            # ADD TO BE SORTED
            if operating_margin_eu >= operating_margin_limit or return_on_sales_eu >= return_on_sales_limit:
                if round(total_eu) != new_phone_eu.total_sales:
                    breakpoint()
                phones_eu.append({"phone": new_phone_eu, "operating_margin%": operating_margin_eu, "sales k": round(new_phone_eu.total_sales), "profit": profit_eu})

            # --- ---- ---- ---- #

            # PREDICT DEMAND, ASIA
            h, hh, c, hc, asia_total = asia.predict(new_phone_asia)
            new_phone_asia.households_sales = round(h)
            new_phone_asia.he_households_sales = round(hh)
            new_phone_asia.companies_sales = round(c)
            new_phone_asia.he_companies_sales = round(hc)
            new_phone_asia.total_sales = round(asia_total)
            
            # CALCULATE PROFIT
            revenue_asia = round(asia_total * new_phone_asia.price)
            operating_costs_asia = round(asia_total * new_phone_asia.cost + ad_budget + channel_investments)
            profit_asia = round(revenue_asia - operating_costs_asia)
            operating_margin = round(profit_asia / operating_costs_asia * 100)
            return_on_sales = round(profit_asia / asia_total * 100)

            # ADD TO BE SORTED
            if operating_margin >= operating_margin_limit or return_on_sales >= return_on_sales_limit:
                if round(asia_total) != new_phone_asia.total_sales:
                    breakpoint()
                phones_asia.append({"phone": new_phone_asia, "operating_margin%": operating_margin, "sales k": round(new_phone_asia.total_sales), "profit": profit_asia})

        phones_eu.sort(key=lambda p: (p["profit"]))
        phones_eu.reverse()
        phones_asia.sort(key=lambda p: (p["profit"]))
        phones_asia.reverse()

        best_eu = phones_eu[0] if len(phones_eu) > 0 else []
        best_asia = phones_asia[0] if len(phones_asia) > 0 else []
        return best_eu, best_asia


    def create_random_phone(self):
        """Returned phone is within tech limits and cost is calculated."""
        limit = 100
        for _ in range(limit):
            perf = random.randint(80, 235)
            battery = random.randint(80, 235)
            camera = bool(random.randint(0, 1))
            memory = bool(random.randint(0, 1))
            display = bool(random.randint(0, 1))
            resistance = bool(random.randint(0, 1))
            security = bool(random.randint(0, 1))
            design = random.randint(1, 3)
            if design == 1: design = "Classic"
            elif design == 2: design = "Avant garde"
            else: design = "Sport"

            ads = 2000
            channels = 1000

            price = 0
            cost = 0

            phone = Phone(
                price,
                cost,
                perf,
                battery,
                ads,
                channels,
                camera,
                memory,
                display,
                resistance,
                security,
                design
            )
            with suppress(OverTechLimit):
                phone.cost = self.manufacturing.cost(phone)
                return phone


        raise Exception(f"Could not randomly create valid phone in {limit} tries")
        

    def test_model_europe(self, test_rnd:int, train_rnd:int, include:list[int]=[]):
        self.train_models(train_rnd, include)

        actual_sales = []
        predicted_sales = []
        total_error = []
        h_error = []
        hh_error = []
        c_error = []
        hc_error = []

        test_set:list[Product] = self.model_europe.data().loc(test_rnd, "europe").products
        for index in range(len(test_set)):
            products = test_set.copy()
            test_product = products.pop(index)
            self.model_europe.train(Market(products))
            
            h, hh, c, hc, total = self.model_europe.predict(test_product)
            
            actual_sales.append(test_product.total_sales)
            predicted_sales.append(total)

            total_error.append(abs(round((total - test_product.total_sales) / test_product.total_sales * 100)))
            h_error.append(abs(round((h - test_product.households_sales) / test_product.households_sales * 100)))
            hh_error.append(abs(round((hh - test_product.he_households_sales) / test_product.he_households_sales * 100)))
            c_error.append(abs(round((c - test_product.companies_sales) / test_product.companies_sales * 100)))
            hc_error.append(abs(round((hc - test_product.he_companies_sales) / test_product.he_companies_sales * 100)))

        # PRINT RESULTS #
        total_error.sort()
        h_error.sort()
        hh_error.sort()
        c_error.sort()
        hc_error.sort()
        for error_idx in range(len(total_error)):
            print(f"{total_error[error_idx]:4} {h_error[error_idx]:4} {hh_error[error_idx]:4} {c_error[error_idx]:4} {hc_error[error_idx]:4}")

        correlation = np.corrcoef(
            actual_sales,
            predicted_sales
        )[0, 1]
        print(f"{correlation=}")
    
        print("MAX")
        print(max(total_error))
        print("")
    
        print("MIN")
        print(min(total_error))
        print("")

        print("AVERAGE")
        print(f"{"All:":4}{sum(total_error) / len(total_error):>4}")
        print(f"{"H:":4}{sum(h_error) / len(h_error):>4}")
        print(f"{"HH:":4}{sum(hh_error) / len(hh_error):>4}")
        print(f"{"C:":4}{sum(c_error) / len(c_error):>4}")
        print(f"{"HC:":4}{sum(hc_error) / ( len(hc_error)):>4}")
        print("")
    
        print("MEDIAN")
        print(np.median(total_error))
        print(np.median(h_error))
        print(np.median(hh_error))
        print(np.median(c_error))
        print(np.median(hc_error))
        print("")


    def test_model_europe_chunks(self, rnd:int=5):
        self.train_models(5)

        test_set:list[Product] = self.model_europe.data().loc(6, "europe").products
        test_chunks = self.chunks(test_set, 3)
        for chunk in test_chunks:
            chunk_actual_sales = []
            chunk_predicted_sales = []
            chunk_total_error = []
            chunk_h_error = []
            chunk_hh_error = []
            chunk_c_error = []
            chunk_hc_error = []
            for test_product in chunk:
                
                h, hh, c, hc, total = self.model_europe.predict(test_product)
                
                chunk_actual_sales.append(test_product.total_sales)
                chunk_predicted_sales.append(total)

                chunk_total_error.append(abs(round((total - test_product.total_sales) / test_product.total_sales * 100)))
                chunk_h_error.append(abs(round((h - test_product.households_sales) / test_product.households_sales * 100)))
                chunk_hh_error.append(abs(round((hh - test_product.he_households_sales) / test_product.he_households_sales * 100)))
                chunk_c_error.append(abs(round((c - test_product.companies_sales) / test_product.companies_sales * 100)))
                chunk_hc_error.append(abs(round((hc - test_product.he_companies_sales) / test_product.he_companies_sales * 100)))

            pprint(sorted(chunk_total_error))
            correlation = np.corrcoef(
                chunk_actual_sales,
                chunk_predicted_sales
            )[0, 1]
            print(f"{correlation=}")

            print("AVERAGE")
            print(f"{sum(chunk_total_error) / len(chunk_total_error):>4}")
            print("")
        
            print("MEDIAN")
            print(np.median(chunk_total_error))
            print("")
        
            print("MAX")
            print(max(chunk_total_error))
            print("")
        
            print("MIN")
            print(min(chunk_total_error))
            print("")


    def chunks(self, xs, n):
        n = max(1, n)
        return (xs[i:i+n] for i in range(0, len(xs), n))
    

    def training_data(self, rnd:int, iclude:list[int]=[]):
        data = self.model_europe.data()

        # Create
        eu = data.loc(rnd, "europe")
        asia = data.loc(rnd, "asia")
        eu_phones = eu.products.copy()
        asia_phones = asia.products.copy()
        
        eu5, asia5 = self._round_5_training_data(rnd)
        eu4, asia4 = self._round_4_training_data(rnd)

        if 5 in iclude and rnd != 5:
            eu_phones += eu5
            asia_phones += asia5
        if 4 in iclude and rnd != 4:
            eu_phones += eu4
            asia_phones += asia4

        return eu_phones, asia_phones

    def _round_5_training_data(self, rnd:int) -> tuple[list[Product], list[Product]]:
        data = self.model_europe.data()

        # EUROPE #
        eu = data.loc(rnd, "europe")
        eu5 = data.loc(5, "europe")

        avg_price = eu.stats.average_price()
        avg_battery = eu.stats.average_battery()
        avg_perf = eu.stats.average_performance()

        avg_price_5 = eu5.stats.average_price()
        avg_battery_5 = eu5.stats.average_battery()
        avg_perf_5 = eu5.stats.average_performance()

        for phone in eu5.products:
            phone.price = round(phone.performance * (avg_price / avg_price_5))
            phone.battery = round(phone.performance * (avg_battery / avg_battery_5))
            phone.performance = round(phone.performance * (avg_perf / avg_perf_5))
            
            phone.households_sales = round(phone.households_sales * (eu.households().total / eu5.households().total))
            phone.he_households_sales = round(phone.he_households_sales * (eu.households().total / eu5.households().total))
            phone.companies_sales = round(phone.companies_sales * (eu.households().total / eu5.households().total))
            phone.he_companies_sales = round(phone.he_companies_sales * (eu.households().total / eu5.households().total))

        # ASIA #
        asia = data.loc(rnd, "asia")
        asia5 = data.loc(5, "asia")

        avg_price = asia.stats.average_price()
        avg_battery = asia.stats.average_battery()
        avg_perf = asia.stats.average_performance()

        avg_price_5 = asia5.stats.average_price()
        avg_battery_5 = asia5.stats.average_battery()
        avg_perf_5 = asia5.stats.average_performance()

        for phone in asia5.products:
            phone.price = round(phone.performance * (avg_price / avg_price_5))
            phone.battery = round(phone.performance * (avg_battery / avg_battery_5))
            phone.performance = round(phone.performance * (avg_perf / avg_perf_5))
            
            phone.households_sales = round(phone.households_sales * (asia.households().total / asia5.households().total))
            phone.he_households_sales = round(phone.he_households_sales * (asia.households().total / asia5.households().total))
            phone.companies_sales = round(phone.companies_sales * (asia.households().total / asia5.households().total))
            phone.he_companies_sales = round(phone.he_companies_sales * (asia.households().total / asia5.households().total))

        return eu5.products, asia5.products

    def _round_4_training_data(self, rnd:int) -> tuple[list[Product], list[Product]]:
        data = self.model_asia.data()

        # EUROPE #
        eu = data.loc(rnd, "europe")
        eu4 = data.loc(4, "europe")
        eu_phones = [
            Phone(
                round(345 * (eu.stats.average_price() / eu4.stats.average_price())),
                225.64,
                round(120 * (eu.stats.average_performance() / eu4.stats.average_performance())),
                round(115 * (eu.stats.average_battery() / eu4.stats.average_battery())),
                0,
                0,
                True,
                True,
                False,
                False,
                True,
                "Sport",
                households_sales=3.6 * (eu.households().total / eu4.households().total),
                he_households_sales=2.5 * (eu.he_households().total / eu4.he_households().total),
                companies_sales=4.5 * (eu.companies().total / eu4.companies().total),
                he_companies_sales=5.1 * (eu.he_companies().total / eu4.he_companies().total),
                total_sales=15.6 * (eu.total / eu4.total),
                brand="Pink",
                warranty=24
            )# type: ignore
        ]

        # ASIA #
        asia = data.loc(rnd, "asia")
        asia4 = data.loc(4, "asia")
        asia_phones = [
            Phone(
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
                households_sales=0.4 * (asia.households().total / asia4.households().total),
                he_households_sales=2.8 * (asia.households().total / asia4.households().total),
                companies_sales=1.1 * (asia.households().total / asia4.households().total),
                he_companies_sales=6.3 * (asia.households().total / asia4.households().total),
                total_sales=10.8 * (asia.households().total / asia4.households().total),
                brand="Pink",
                warranty=24
            ) # type:ignore
        ]

        return eu_phones, asia_phones # type:ignore




