from typing import Any, Literal
from dataclasses import dataclass
from pprint import pprint
import statsmodels.api as sm
import pandas as pd
import numpy as np
from pprint import pprint

from .product import Product, Phone
from .market import Market, MarketHistory
from .demand_model import DemandModel



class SalesForecast:

    def __init__(self, households:float, high_end_households:float, companies:float, high_end_companies:float) -> None:
        self.households = households
        self.high_end_households = high_end_households
        self.companies = companies
        self.high_end_companies = high_end_companies


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
        self.model_europe = DemandModel()
        self.model_asia = DemandModel()
        eu_data, asia_data = self.training_data()
        self.model_europe.train(Market(eu_data))
        self.model_asia.train(Market(asia_data))

        self.manufacturing = ManufacturingCosts(
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

    def find_best_phone(self):
        pass


    def test_model_europe(self, r:int=5):

        actual_sales = []
        predicted_sales = []
        total_error = []
        h_error = []
        hh_error = []
        c_error = []
        hc_error = []

        test_set:list[Product] = self.model_europe.data().loc(r, "europe").products
        for index in range(len(test_set)):
            products = test_set.copy()
            test_product = products.pop(index)
            #self.model_europe.train(Market(products))
            
            h, hh, c, hc, total = self.model_europe.predict(test_product)
            
            actual_sales.append(test_product.total_sales)
            predicted_sales.append(total)

            total_error.append(abs(round((total - test_product.total_sales) / test_product.total_sales * 100)))
            h_error.append(abs(round((h - test_product.households_sales) / test_product.households_sales * 100)))
            hh_error.append(abs(round((hh - test_product.he_households_sales) / test_product.he_households_sales * 100)))
            c_error.append(abs(round((c - test_product.companies_sales) / test_product.companies_sales * 100)))
            hc_error.append(abs(round((hc - test_product.he_companies_sales) / test_product.he_companies_sales * 100)))

        pprint(sorted(total_error))
        correlation = np.corrcoef(
            actual_sales,
            predicted_sales
        )[0, 1]
        print(f"{correlation=}")

        print("AVERAGE")
        print(f"All: {sum(total_error) / len(total_error):>4}")
        print(f"H: {sum(h_error) / len(h_error):>4}")
        print(f"HH:{sum(hh_error) / len(hh_error):>4}")
        print(f"C: {sum(c_error) / len(c_error):>4}")
        print(f"HC: {sum(hc_error) / ( len(hc_error)):>4}")
        print("")
    
        print("MEDIAN")
        print(np.median(total_error))
        print(np.median(h_error))
        print(np.median(hh_error))
        print(np.median(c_error))
        print(np.median(hc_error))
        print("")
    
        print("MAX")
        print(max(total_error))
        print(max(h_error))
        print(max(hh_error))
        print(max(c_error))
        print(max(hc_error))
        print("")
    
        print("MIN")
        print(min(total_error))
        print(min(h_error))
        print(min(hh_error))
        print(min(c_error))
        print(min(hc_error))
        print("")
    

    def training_data(self):
        data = self.model_europe.data()
        eu_phones = data.loc(5, "europe").products.copy()
        eu_phones.append(
            Phone(
                345,
                225.64,
                120,
                115,
                0,
                0,
                True,
                True,
                False,
                False,
                True,
                "Sport",
                households_sales=3.6,
                he_households_sales=2.5,
                companies_sales=4.5,
                he_companies_sales=5.1,
                total_sales=15.6,
                brand="Pink",
                warranty=24
            )# type: ignore
        )

        data = self.model_asia.data()
        asia_phones = data.loc(5, "asia").products.copy()

        asia_phones.append(
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
                households_sales=0.4,
                he_households_sales=2.8,
                companies_sales=1.1,
                he_companies_sales=6.3,
                total_sales=10.8,
                brand="Pink",
                warranty=24
            ) # type:ignore
        )
        return eu_phones, asia_phones

