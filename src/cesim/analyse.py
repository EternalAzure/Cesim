import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from random import randint

from .market import Market

TITLE = "Round 3"

class Analyse:

    def __init__(self, market:Market) -> None:
        self.market = market


    # -- DESIGN -- #
    def design(self):
        h_classic = self.market.group_design_sales("Classic", "H")
        h_avant = self.market.group_design_sales("Avant garde", "H")
        h_sport = self.market.group_design_sales("Sport", "H")
        
        hh_classic = self.market.group_design_sales("Classic", "HH")
        hh_avant = self.market.group_design_sales("Avant garde", "HH")
        hh_sport = self.market.group_design_sales("Sport", "HH")
        
        c_classic = self.market.group_design_sales("Classic", "C")
        c_avant = self.market.group_design_sales("Avant garde", "C")
        c_sport = self.market.group_design_sales("Sport", "C")
        
        hc_classic = self.market.group_design_sales("Classic", "HC")
        hc_avant = self.market.group_design_sales("Avant garde", "HC")
        hc_sport = self.market.group_design_sales("Sport", "HC")

        focus_groups = ("Households", "High-End Households", "Companies", "High-End Companies")
        style_sales = {
            'Classic': (h_classic, hh_classic, c_classic, hc_classic),
            'Avant Garde': (h_avant, hh_avant, c_avant, hc_avant),
            'Sport': (h_sport, hh_sport, c_sport, hc_sport),
        }

        fig, ax = plt.subplots(layout='constrained')
        fig.suptitle(TITLE)

        res = ax.grouped_bar(style_sales, tick_labels=focus_groups, group_spacing=1) # pyright: ignore
        for container in res.bar_containers: # pyright: ignore
            ax.bar_label(container, padding=3)

        # Add some text for labels, title, etc.
        most_popular = hc_sport
        if hc_avant > hc_sport:
            most_popular = hc_avant
        ax.set_ylabel('sales k')
        ax.set_title('Sales')
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0, most_popular * 1.5)

        plt.show()

    # -- FEATURES -- #

    def feature(self):
        h_sales = self.market.h_sales()
        h_camera = round(self.market.group_feature_sales("camera", "H") / h_sales * 100)
        h_memory = round(self.market.group_feature_sales("memory", "H") / h_sales * 100)
        h_display = round(self.market.group_feature_sales("display", "H") / h_sales * 100)
        h_resistance = round(self.market.group_feature_sales("resistance", "H") / h_sales * 100)
        h_security = round(self.market.group_feature_sales("security", "H") / h_sales * 100)

        hh_sales = self.market.hh_sales()
        hh_camera = round(self.market.group_feature_sales("camera", "HH") / hh_sales * 100)
        hh_memory = round(self.market.group_feature_sales("memory", "HH") / hh_sales * 100)
        hh_display = round(self.market.group_feature_sales("display", "HH") / hh_sales * 100)
        hh_resistance = round(self.market.group_feature_sales("resistance", "HH") / hh_sales * 100)
        hh_security = round(self.market.group_feature_sales("security", "HH") / hh_sales * 100)

        c_sales = self.market.c_sales()
        c_camera = round(self.market.group_feature_sales("camera", "C") / c_sales * 100)
        c_memory = round(self.market.group_feature_sales("memory", "C") / c_sales * 100)
        c_display = round(self.market.group_feature_sales("display", "C") / c_sales * 100)
        c_resistance = round(self.market.group_feature_sales("resistance", "C") / c_sales * 100)
        c_security = round(self.market.group_feature_sales("security", "C") / c_sales * 100)

        hc_sales = self.market.hc_sales()
        hc_camera = round(self.market.group_feature_sales("camera", "HC") / hc_sales * 100)
        hc_memory = round(self.market.group_feature_sales("memory", "HC") / hc_sales * 100)
        hc_display = round(self.market.group_feature_sales("display", "HC") / hc_sales * 100)
        hc_resistance = round(self.market.group_feature_sales("resistance", "HC") / hc_sales * 100)
        hc_security = round(self.market.group_feature_sales("security", "HC") / hc_sales * 100)

        focus_groups = ("Households", "High-End Households", "Companies", "High-End Companies")
        feature_sales = {
            'Camera': (h_camera, hh_camera, c_camera, hc_camera),
            'Memory': (h_memory, hh_memory, c_memory, hc_memory),
            'Display': (h_display, hh_display, c_display, hc_display),
            'Resistance': (h_resistance, hh_resistance, c_resistance, hc_resistance),
            'Security': (h_security, hh_security, c_security, hc_security),
        }

        fig, ax = plt.subplots(layout='constrained')
        fig.suptitle(TITLE)

        res = ax.grouped_bar(feature_sales, tick_labels=focus_groups, group_spacing=1) # pyright: ignore
        for container in res.bar_containers: # pyright: ignore
            ax.bar_label(container, padding=3)

        # Add some text for labels, title, etc.
        ax.set_ylabel('sales %')
        ax.set_title('Sales')
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0, 120)

        plt.show()

    def design_feature(self):
        
        h_design_feature = self.market.group_design_feature("H")
        hh_design_feature = self.market.group_design_feature("HH")
        c_design_feature = self.market.group_design_feature("C")
        hc_design_feature = self.market.group_design_feature("HC")
        self._plot_features_by_design_for_focus_group(h_design_feature, "H")
        self._plot_features_by_design_for_focus_group(hh_design_feature, "HH")
        self._plot_features_by_design_for_focus_group(c_design_feature, "C")
        self._plot_features_by_design_for_focus_group(hc_design_feature, "HC")

        plt.show()

    def _plot_features_by_design_for_focus_group(self, features_by_design:dict, group:Literal["H", "HH", "C", "HC"]):
        classic = features_by_design["Classic"]
        avant = features_by_design["Avant garde"]
        sport = features_by_design["Sport"]

        design_groups = ("Classic", "Avant garde", "Sport")
        feature_sales = {
            'Camera': (classic["camera"], avant["camera"], sport["camera"]),
            'Memory': (classic["memory"], avant["memory"], sport["memory"]),
            'Display': (classic["display"], avant["display"], sport["display"]),
            'Resistance': (classic["resistance"], avant["resistance"], sport["resistance"]),
            'Security': (classic["security"], avant["security"], sport["security"]),
        }

        fig, ax = plt.subplots(layout='constrained')
        fig.suptitle(TITLE)

        res = ax.grouped_bar(feature_sales, tick_labels=design_groups, group_spacing=1) # pyright: ignore
        for container in res.bar_containers: # pyright: ignore
            ax.bar_label(container, padding=3)

        # Add some text for labels, title, etc.
        ax.set_ylabel('sales %')
        
        ax.set_title(f"{group} Design & Features")
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0, 130)

    # -- PRICE -- #
    def price(self):
        self.all_price()
        self.group_price("H")
        self.group_price("HH")
        self.group_price("C")
        self.group_price("HC")
        plt.show()

    def all_price(self):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.price for p in classics]
        y = [p.total_sales for p in classics]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in avants]
        y = [p.total_sales for p in avants]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in sports]
        y = [p.total_sales for p in sports]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Calculate the best-fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title("All Price")
        ax.set_xlabel("price €")
        ax.set_ylabel("sales k")
        ax.grid(True)

        #plt.show()

    def group_price(self, group:Literal["H", "HH", "C", "HC"]):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.price for p in classics]
        if group == "H":
            y = [p.households_sales for p in classics]
        elif group == "HH":
            y = [p.high_end_households_sales for p in classics]
        elif group == "C":
            y = [p.companies_sales for p in classics]
        elif group == "HC":
            y = [p.high_end_companies_sales for p in classics]
        else: raise ValueError()
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in avants]
        if group == "H":
            y = [p.households_sales for p in avants]
        elif group == "HH":
            y = [p.high_end_households_sales for p in avants]
        elif group == "C":
            y = [p.companies_sales for p in avants]
        elif group == "HC":
            y = [p.high_end_companies_sales for p in avants]
        else: raise ValueError()
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in sports]
        if group == "H":
            y = [p.households_sales for p in sports]
        elif group == "HH":
            y = [p.high_end_households_sales for p in sports]
        elif group == "C":
            y = [p.companies_sales for p in sports]
        elif group == "HC":
            y = [p.high_end_companies_sales for p in sports]
        else: raise ValueError()
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Calculate the best-fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title(f"{group} Price")
        ax.set_xlabel("price €")
        ax.set_ylabel("sales k")
        ax.grid(True)

        #plt.show()

    def all_performance_per_euro(self):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.performance_per_euro() for p in classics]
        y = [p.total_sales for p in classics]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.performance_per_euro() for p in avants]
        y = [p.total_sales for p in avants]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.performance_per_euro() for p in sports]
        y = [p.total_sales for p in sports]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Calculate the best-fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title("Performance per €")
        ax.set_xlabel("performance / price")
        ax.set_ylabel("sales k")
        ax.grid(True)

        plt.show()

    def all_battery_per_euro(self):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.battery_per_euro() for p in classics]
        y = [p.total_sales for p in classics]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro() for p in avants]
        y = [p.total_sales for p in avants]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro() for p in sports]
        y = [p.total_sales for p in sports]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Calculate the best-fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title("Battery per €")
        ax.set_xlabel("battery / price")
        ax.set_ylabel("sales k")
        ax.grid(True)

        plt.show()

    def all_ppe_bpe(self):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.battery_per_euro() for p in classics]
        y = [p.performance_per_euro() for p in classics]
        scale = [p.total_sales for p in classics]
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro() for p in avants]
        y = [p.performance_per_euro() for p in avants]
        scale = [p.total_sales for p in avants]
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro() for p in sports]
        y = [p.performance_per_euro() for p in sports]
        scale = [p.total_sales for p in sports]
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        ax.legend()
        ax.set_title("Sales")
        ax.set_xlabel("battery / price")
        ax.set_ylabel("performance / price")
        ax.grid(True)

        plt.show()

    # -- RELATIVE PRICE -- #
    def median(self):
        pass

    # -- ? -- #
    def margin_x_sales(self):
        source = self.market.products
        source.sort(key=lambda p: p.margin())
        x = [p.margin() for p in source]
        y = [p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("sales k")
        ax.set_xlabel("margin €")
        ax.plot(x, y)
        plt.show()

    def profit(self):
    
        source = self.market.products.copy()
        y = [p.margin() * p.total_sales for p in source]

        source.sort(key=lambda p: p.price)
        x_price = [p.price for p in source]

        source.sort(key=lambda p: p.total_sales)
        x_sales = [p.total_sales for p in source]

        source.sort(key=lambda p: p.margin())
        x_margin = [p.margin() for p in source]

        source.sort(key=lambda p: abs(p.price - self.market.median_price()))
        x_deviance = [abs(p.price - self.market.median_price()) for p in source]


        fig, ax = plt.subplots(2,2)
        fig.suptitle(TITLE)

        ax[0,0].plot(x_price, y); ax[0,0].set_title("Price"); ax[0,0].set_ylabel("profit"); ax[0,0].set_xlabel("price €")
        ax[0,1].plot(x_sales, y); ax[0,1].set_title("Sales"); ax[0,1].set_ylabel("profit"); ax[0,1].set_xlabel("sales k")
        ax[1,0].plot(x_margin, y); ax[1,0].set_title("Margin"); ax[1,0].set_ylabel("profit"); ax[1,0].set_xlabel("margin €")
        ax[1,1].plot(x_deviance, y); ax[1,1].set_title("Deviance"); ax[1,1].set_ylabel("profit"); ax[1,1].set_xlabel("deviance from median price €")
        #ax[1,1].plot(x, y4); ax[1,1].set_title("Tanh")
        fig.tight_layout()
        plt.show()

    def profit_x_price(self):
        source = self.market.products
        source.sort(key=lambda p: p.price)
        x = [p.price for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("profit")
        ax.set_xlabel("price")
        ax.plot(x, y)
        plt.show()

    def profit_x_sales(self):
        source = self.market.products
        source.sort(key=lambda p: p.total_sales)
        x = [p.total_sales for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("profit")
        ax.set_xlabel("sales k")
        ax.plot(x, y)
        plt.show()

    def profit_x_margin(self):
        source = self.market.products
        source.sort(key=lambda p: p.margin())
        x = [p.margin() for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("profit")
        ax.set_xlabel("margin")
        ax.plot(x, y)
        plt.show()

    def profit_x_performance(self):
        source = self.market.products
        source.sort(key=lambda p: p.performance)
        x = [p.performance for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("profit")
        ax.set_xlabel("performance")
        ax.plot(x, y)
        plt.show()

    def profit_x_battery(self):
        source = self.market.products
        source.sort(key=lambda p: p.battery)
        x = [p.battery for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("profit")
        ax.set_xlabel("battery")
        ax.plot(x, y)
        plt.show()