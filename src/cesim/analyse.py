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

        focus_groups = ("Households", "High-End Households", "Companies", "High-End Companies")
        style_sales = {
            'Classic': (
                self.market.classic().households().total, 
                self.market.classic().high_end_households().total, 
                self.market.classic().companies().total, 
                self.market.classic().high_end_companies().total
            ),
            'Avant Garde': (
                self.market.avant_garde().households().total, 
                self.market.avant_garde().high_end_households().total, 
                self.market.avant_garde().companies().total, 
                self.market.avant_garde().high_end_companies().total
            ),
            'Sport': (
                self.market.sport().households().total, 
                self.market.sport().high_end_households().total, 
                self.market.sport().companies().total, 
                self.market.sport().high_end_companies().total
            ),
        }

        fig, ax = plt.subplots(layout='constrained')
        fig.suptitle(TITLE)

        res = ax.grouped_bar(style_sales, tick_labels=focus_groups, group_spacing=1) # pyright: ignore
        for container in res.bar_containers: # pyright: ignore
            ax.bar_label(container, padding=3)

        ax.set_ylabel('sales k')
        ax.set_title('Sales')
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0, self.market.y_lim().group)

        plt.show()

    # -- FEATURES -- #

    def feature(self):

        focus_groups = ("Households", "High-End Households", "Companies", "High-End Companies")
        feature_sales = {
            'Camera': (
                round(self.market.households().camera().total / self.market.households().total * 100, 2), 
                round(self.market.high_end_households().camera().total / self.market.high_end_households().total * 100, 2), 
                round(self.market.companies().camera().total / self.market.companies().total * 100, 2), 
                round(self.market.high_end_companies().camera().total / self.market.high_end_companies().total * 100, 2)
            ),
            'Memory': (
                round(self.market.households().memory().total / self.market.households().total * 100, 2),
                round(self.market.high_end_households().memory().total / self.market.high_end_households().total * 100, 2),
                round(self.market.companies().memory().total / self.market.companies().total * 100, 2),
                round(self.market.high_end_companies().memory().total / self.market.high_end_companies().total * 100, 2),
            ),
            'Display': (
                round(self.market.households().display().total / self.market.households().total * 100, 2), 
                round(self.market.high_end_households().display().total / self.market.high_end_households().total * 100, 2), 
                round(self.market.companies().display().total / self.market.companies().total * 100, 2), 
                round(self.market.high_end_companies().display().total / self.market.high_end_companies().total * 100, 2)
            ),
            'Resistance': (
                round(self.market.households().resistance().total / self.market.households().total * 100, 2),
                round(self.market.high_end_households().resistance().total / self.market.high_end_households().total * 100, 2),
                round(self.market.companies().resistance().total / self.market.companies().total * 100, 2),
                round(self.market.high_end_companies().resistance().total / self.market.high_end_companies().total * 100, 2)
            ),
            'Security': (
                round(self.market.households().security().total / self.market.households().total * 100, 2), 
                round(self.market.high_end_households().security().total / self.market.high_end_households().total * 100, 2), 
                round(self.market.companies().security().total / self.market.companies().total * 100, 2), 
                round(self.market.high_end_companies().security().total / self.market.high_end_companies().total * 100, 2)
            ),
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
        self._plot_features_by_design_for_focus_group("H")
        self._plot_features_by_design_for_focus_group("HH")
        self._plot_features_by_design_for_focus_group("C")
        self._plot_features_by_design_for_focus_group("HC")

        plt.show()

    def _plot_features_by_design_for_focus_group(self, group:Literal["H", "HH", "C", "HC"]):
        if group == "H":
            phones = self.market.households()
        elif group == "HH":
            phones = self.market.high_end_households()
        elif group == "C":
            phones = self.market.companies()
        elif group == "HC":
            phones = self.market.high_end_companies()
        else: raise ValueError()

        design_groups = ("Classic", "Avant garde", "Sport")
        feature_sales = {
            'Camera': (phones.classic().camera().total, phones.avant_garde().camera().total, phones.sport().camera().total),
            'Memory': (phones.classic().memory().total, phones.avant_garde().memory().total, phones.sport().memory().total),
            'Display': (phones.classic().display().total, phones.avant_garde().display().total, phones.sport().display().total),
            'Resistance': (phones.classic().resistance().total, phones.avant_garde().resistance().total, phones.sport().resistance().total),
            'Security': (phones.classic().security().total, phones.avant_garde().security().total, phones.sport().security().total),
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

    # -- PERFORMANCE & BATTERY -- #

    def performance(self):
        self.group_performance("H")
        self.group_performance("HH")
        self.group_performance("C")
        self.group_performance("HC")
        plt.show()

    def group_performance(self, group:Literal["H", "HH", "C", "HC"]):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.performance for p in classics]
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

        x = [p.performance for p in avants]
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

        x = [p.performance for p in sports]
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
        ax.set_title(f"{group} Performance")
        ax.set_xlabel("performance")
        ax.set_ylabel("sales k")
        ax.grid(True)

    def battery(self):
        self.group_battery("H")
        self.group_battery("HH")
        self.group_battery("C")
        self.group_battery("HC")
        plt.show()

    def group_battery(self, group:Literal["H", "HH", "C", "HC"]):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.battery for p in classics]
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

        x = [p.battery for p in avants]
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

        x = [p.battery for p in sports]
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
        ax.set_title(f"{group} Battery")
        ax.set_xlabel("battery")
        ax.set_ylabel("sales k")
        ax.grid(True)

    def performance_per_euro(self):
        self.group_ppe("H")
        self.group_ppe("HH")
        self.group_ppe("C")
        self.group_ppe("HC")
        plt.show()

    def all_ppe(self):
        """Performance per euro"""
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

    def group_ppe(self, group:Literal["H", "HH", "C", "HC"]):
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.performance_per_euro() for p in classics]
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

        x = [p.performance_per_euro() for p in avants]
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

        x = [p.performance_per_euro() for p in sports]
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
        ax.set_title(f"{group} Performance / €")
        ax.set_xlabel("performance")
        ax.set_ylabel("sales k")
        ax.grid(True)

    def battery_per_euro(self):
        self.group_bpe("H")
        self.group_bpe("HH")
        self.group_bpe("C")
        self.group_bpe("HC")
        plt.show()

    def all_bpe(self):
        """Battery per euro"""
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
        ax.set_title("Battery / €")
        ax.set_xlabel("battery / price")
        ax.set_ylabel("sales k")
        ax.grid(True)

        plt.show()

    def group_bpe(self, group:Literal["H", "HH", "C", "HC"]):
        """Battery per euro"""
        classics = self.market.products_by_design("Classic")
        avants = self.market.products_by_design("Avant garde")
        sports = self.market.products_by_design("Sport")

        fig, ax = plt.subplots()
        fig.suptitle(TITLE)

        x = [p.battery_per_euro() for p in classics]
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

        x = [p.battery_per_euro() for p in avants]
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

        x = [p.battery_per_euro() for p in sports]
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
        ax.set_title(f"{group} Battery / €")
        ax.set_xlabel("battery")
        ax.set_ylabel("sales k")
        ax.grid(True)



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

        source.sort(key=lambda p: abs(p.price - self.market.stats.median_price()))
        x_deviance = [abs(p.price - self.market.stats.median_price()) for p in source]


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