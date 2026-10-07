from typing import Any, Literal
from dataclasses import dataclass
from pprint import pprint
import statsmodels.api as sm
import pandas as pd
import numpy as np
from pprint import pprint

from .product import Product, Phone
from .market import Market, MarketHistory



class SalesForecast:

    def __init__(self, households:float, high_end_households:float, companies:float, high_end_companies:float) -> None:
        self.households = households
        self.high_end_households = high_end_households
        self.companies = companies
        self.high_end_companies = high_end_companies


class Effects:
    """A simple multiplier on demand"""

    def __init__(self, households:float, he_households:float, companies:float, he_companies:float) -> None:
        self.households:float = households
        self.he_households:float = he_households
        self.companies:float = companies
        self.he_companies:float = he_companies

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


class DemandModel:

    def __init__(self, market:Market) -> None:
        self.market = market
        self.h_model = self._make_model(market.households())
        self.hh_model = self._make_model(market.he_households())
        self.c_model = self._make_model(market.companies())
        self.hc_model = self._make_model(market.he_companies())
        self.model = self._make_model(market)
        
        #price_elasticity = self.model.params["log_price"]

    def predict_demand(self, phone:Phone|Product):

        def make_hypothetical(average_price:float, average_performance:float, average_battery:float):
            hypothetical = pd.DataFrame({
                "log_price": [np.log(phone.price)],
                "log_battery": [np.log(phone.battery)],
                "log_performance": [np.log(phone.performance)],
                "log_advertizing": [phone.advertizing],
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

        h_X = make_hypothetical(
            self.market.households().stats.average_price(),
            self.market.households().stats.average_performance(),
            self.market.households().stats.average_battery())
        hh_X = make_hypothetical(
            self.market.he_households().stats.average_price(),
            self.market.he_households().stats.average_performance(),
            self.market.he_households().stats.average_battery())
        c_X = make_hypothetical(
            self.market.companies().stats.average_price(),
            self.market.companies().stats.average_performance(),
            self.market.companies().stats.average_battery())
        hc_X = make_hypothetical(
            self.market.he_companies().stats.average_price(),
            self.market.he_companies().stats.average_performance(),
            self.market.he_companies().stats.average_battery())
        

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

    def _make_model(self, market:Market):
        
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
            "log_battery": np.log(df["battery"]),
            "log_performance": np.log(df["performance"]),
            "log_advertizing": df["advertizing"],
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


class SpecsModel:


    def performances_effects_on_demand(self, performance:int, average_performance:int) -> tuple[Effects, Effects]:
        """Returns multipliers on demand. Europe and Asia."""
        ratio = performance / average_performance
        x = ratio - 1

        if ratio < 0.75: # -50 - -25
            # Asia
            y_households    = x * 0.5864 + 2.52
            y_he_households = x * 1.1276 - 3.01
            y_companies     = x * 0.6356 + 2.49
            y_hc_companies  = x * 1.0728 - 1.45

            asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

            # Europe
            y_households    = x * 0.4200 + 2.23
            y_he_households = x * 1.0252 - 0.44
            y_companies     = x * 0.5336 + 2.47
            y_hc_companies  = x * 1.0512 - 0.95

            europe = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio < 0 and ratio >=0.75:
            # Asia
            y_households    = x * 0.4856 + 0
            y_he_households = x * 1.2480 + 0
            y_companies     = x * 0.5360 + 0
            y_hc_companies  = x * 1.1308 + 0

            asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

            # Europe
            y_households    = x * 0.3308 + 0
            y_he_households = x * 1.0428 + 0
            y_companies     = x * 0.4348 + 0
            y_hc_companies  = x * 1.0892 + 0

            europe = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio > 0 and ratio <=1.25:
            # Asia
            y_households    = x * 0.4224 + 0
            y_he_households = x * 1.3460 + 0
            y_companies     = x * 0.4720 + 0
            y_hc_companies  = x * 1.1760 + 0

            asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

            # Europe
            y_households    = x * 0.2768 + 0
            y_he_households = x * 1.0560 + 0
            y_companies     = x * 0.3736 + 0
            y_hc_companies  = x * 1.1184 + 0

            europe = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio > 1.25: # +25 - +50
            # Asia
            y_households    = x * 0.3784 + 1.1
            y_he_households = x * 1.4300 - 2.1
            y_companies     = x * 0.4268 + 1.13
            y_hc_companies  = x * 1.2132 - 0.93

            asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

            # Europe
            y_households    = x * 0.2404 + 0.91
            y_he_households = x * 1.0668 - 0.27
            y_companies     = x * 0.3308 + 1.07
            y_hc_companies  = x * 1.1184 - 0.6

            europe = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        else: raise Exception("Jotain on pielessä kaavassa")
        return europe, asia

    def batterys_effects_on_demand(self, battery:int, average_battery:int) -> Effects:
        """Returns multipliers on demand. Europe and Asia."""
        ratio = battery / average_battery
        x = ratio - 1

        if ratio < 0.75: # -50 - -25
            # Europe & Asia
            y_households    = x * 0.4200 + 2.23
            y_he_households = x * 1.0252 - 0.44
            y_companies     = x * 0.5336 + 2.47
            y_hc_companies  = x * 1.0512 - 0.95

            europe_and_asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio < 0 and ratio >=0.75:
            # Europe & Asia
            y_households    = x * 0.3780 + 0
            y_he_households = x * 0.5288 + 0
            y_companies     = x * 1.1536 + 0
            y_hc_companies  = x * 1.2724 + 0

            europe_and_asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio > 0 and ratio <=1.25:
            # Europe & Asia
            y_households    = x * 0.3212 + 0
            y_he_households = x * 0.4668 + 0
            y_companies     = x * 1.2128 + 0
            y_hc_companies  = x * 1.3880 + 0

            europe_and_asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )

        elif ratio > 1.25: # +25 - +50
            # Europe & Asia
            y_households    = x * 0.2820 + 0.98
            y_he_households = x * 0.4220 + 1.12
            y_companies     = x * 1.2620 - 1.23
            y_hc_companies  = x * 1.4884 - 2.51

            europe_and_asia = Effects(
                y_households,
                y_he_households,
                y_companies,
                y_hc_companies
            )


        else: raise Exception("Jotain on pielessä kaavassa")
        return europe_and_asia

    def _function(self, x:float):
        return x * 0.5864 + 2.52


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
        h_sport = 0.85,
        h_avant_garde = 0.11,
        h_classic = 0.0377,

        hh_sport = 0.604,
        hh_avant_garde = 0.354,
        hh_classic = 0.0429,

        c_sport = 0.73,
        c_avant_garde = 0.19,
        c_classic = 0.0827,

        hc_sport = 0.63,
        hc_avant_garde = 0.29,
        hc_classic = 0.077,

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

    preferences_asia = PreferenceDistribution(
        # -- DESIGN -- #
        h_sport = 0.1379,
        h_avant_garde = 0.2153,
        h_classic = 0.6468,

        hh_sport = 0.1157,
        hh_avant_garde = 0.5491,
        hh_classic = 0.37,

        c_sport = 0.1041,
        c_avant_garde = 0.3578,
        c_classic = 0.5381,

        hc_sport = 0.1072,
        hc_avant_garde = 0.5634,
        hc_classic = 0.3295,

        # -- FEATURES -- #
        h_camera = 65.55,
        h_memory = 94.15,
        h_display = 78.47,
        h_resistance = 3.34,
        h_security = 60.21,

        hh_camera = 94.22,
        hh_memory = 90.5,
        hh_display = 45.09,
        hh_resistance = 7.28,
        hh_security = 65.33,

        c_camera = 78.24,
        c_memory = 89.48,
        c_display = 64.22,
        c_resistance = 5.51,
        c_security = 64.68,

        hc_camera = 92.07,
        hc_memory = 83.2,
        hc_display = 43.66,
        hc_resistance = 9.66,
        hc_security = 76.24,
    )

    specs_model = SpecsModel()

    def play(self, data:MarketHistory):
        self.data = data

        round_5_europe = data.loc(5, "europe")
        round_5_asia = data.loc(5, "asia")

        actual_sales = []
        predicted_sales = []
        total_error = []
        h_error = []
        hh_error = []
        c_error = []
        hc_error = []
        test_set:list[Product] = round_5_asia.products
        training_set:list[Product] = round_5_asia.products
        training_set += self.add_no_ads_phone_europe()
        training_set += self.add_no_ads_phone_asia()
        for index in range(len(test_set)):
            products = test_set.copy()
            test_product = products.pop(index)
            
            model = DemandModel(Market(training_set))
            h, hh, c, hc, total = model.predict_demand(test_product)
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
        """
            EXTRA           ORIGINAL        EXTRA EXTRA     XTR XTR +       
                                                            NO LOG ADS
            CORRELATION
            0.8132          0.66201         0.8311          0.8625

            AVERAGE
            31.18           36.30           30.41           28.69

            48.86           53.48           51.76           47.34
            46.57           51.15           45.72           50.48
            27.64           33.19           32.62           31.45
            57.54           61.70           57.48           59.59

            MEDIAN
            32.0            35              29              26

            39.0            48              41              33
            41.5            35              36              36
            20.0            32              17              18
            48.5            56              47              52

            MAX 
            102             103             98              92

            169             170             237             246
            175             270             177             181
            137             138             174             177
            174             190             177             215
            
            MIN 
            2               0               0

            0               1               3
            1               2               1
            1               0               0
            2               4               3
        """

        print("AVERAGE")
        print(f"All: {sum(total_error) / len(total_error):>4}")
        print(f"H: {sum(h_error) / len(h_error):>4}")
        print(f"HH:{sum(hh_error) / len(hh_error):>4}")
        print(f"C: {sum(c_error) / len(c_error):>4}")
        print(f"HC: {sum(hc_error) / ( len(hc_error)):>4}")
    
        print("MEDIAN")
        print(np.median(total_error))
        print(np.median(h_error))
        print(np.median(hh_error))
        print(np.median(c_error))
        print(np.median(hc_error))
    
        print("MAX")
        print(max(total_error))
        print(max(h_error))
        print(max(hh_error))
        print(max(c_error))
        print(max(hc_error))
    
        print("MIN")
        print(min(total_error))
        print(min(h_error))
        print(min(hh_error))
        print(min(c_error))
        print(min(hc_error))
    




    def add_no_ads_phone_europe(self) -> list[Product]:
        # Aito
        phone = Phone(
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
        )

        return [phone] # type:ignore

    def add_no_ads_phone_asia(self) -> list[Product]:
        phone = Phone(
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
        )
        return [phone] # type:ignore
