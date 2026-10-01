import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
from random import randint

import itertools

from .market import Market



class Analyse:

    def __init__(self, market:Market, round:int) -> None:
        self.market: Market = market
        self.title: str = f"Round {round}"

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
        fig.suptitle(self.title)

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
        fig.suptitle(self.title)

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
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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

    # -- SPECS PER EURO -- #
    
    def performance_per_euro(self):
        self.group_ppe("H")
        self.group_ppe("HH")
        self.group_ppe("C")
        self.group_ppe("HC")
        plt.show()

    def all_ppe(self):
        """Performance per euro"""
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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

    def group_price(self, group:Literal["H", "HH", "C", "HC"]):
        classics = self.market.classic().products
        avants = self.market.avant_garde().products
        sports = self.market.sport().products

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

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
        ax.set_ylim(0)
        ax.grid(True)

    def margin_x_sales(self):
        source = self.market.products
        source.sort(key=lambda p: p.margin())
        x = [p.margin() for p in source]
        y = [p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("sales k")
        ax.set_xlabel("margin €")
        ax.plot(x, y)

        # Calculate the best-fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        plt.show()

    # -- RELATIVE PRICE -- #

    def cumulative(self):
        self.group_cumulative("H")
        self.group_cumulative("HH")
        self.group_cumulative("C")
        self.group_cumulative("HC")
        plt.show()

    def group_cumulative(self, group:Literal["H", "HH", "C", "HC"]):
        if group == "H":
            low_perf = [p for p in self.market.households().products if p.performance <= self.market.stats.low_performance()]
            high_perf = [p for p in self.market.households().products if p.performance >= self.market.stats.high_performance()]
            mid_perf = [p for p in self.market.households().products if p not in low_perf and p not in high_perf]

            average = self.market.households().stats.average_price()
            x_average = [average, average]
            y_average = [0, self.market.households().y_lim().total]
            x_trend = [p.price for p in self.market.households().products]
            y_cum_sales = list(itertools.accumulate([p.total_sales / self.market.households().total for p in self.market.households().products]))
            y_cum_sales = [1 - p for p in y_cum_sales]
        elif group == "HH":
            low_perf = [p for p in self.market.high_end_households().products if p.performance <= self.market.stats.low_performance()]
            high_perf = [p for p in self.market.high_end_households().products if p.performance >= self.market.stats.high_performance()]
            mid_perf = [p for p in self.market.high_end_households().products if p not in low_perf and p not in high_perf]

            average = self.market.high_end_households().stats.average_price()
            x_average = [average, average]
            y_average = [0, self.market.high_end_households().y_lim().total]
            x_trend = [p.price for p in self.market.high_end_households().products]
            y_cum_sales = list(itertools.accumulate([p.total_sales / self.market.high_end_households().total for p in self.market.high_end_households().products]))
            y_cum_sales = [1 - p for p in y_cum_sales]
        elif group == "C":
            low_perf = [p for p in self.market.companies().products if p.performance <= self.market.stats.low_performance()]
            high_perf = [p for p in self.market.companies().products if p.performance >= self.market.stats.high_performance()]
            mid_perf = [p for p in self.market.companies().products if p not in low_perf and p not in high_perf]
            
            average = self.market.companies().stats.average_price()
            x_average = [average, average]
            y_average = [0, self.market.companies().y_lim().total]
            x_trend = [p.price for p in self.market.companies().products]
            y_cum_sales = list(itertools.accumulate([p.total_sales / self.market.companies().total for p in self.market.companies().products]))
            y_cum_sales = [1 - p for p in y_cum_sales]
        elif group == "HC":
            low_perf = [p for p in self.market.high_end_companies().products if p.performance <= self.market.stats.low_performance()]
            high_perf = [p for p in self.market.high_end_companies().products if p.performance >= self.market.stats.high_performance()]
            mid_perf = [p for p in self.market.high_end_companies().products if p not in low_perf and p not in high_perf]
            
            average = self.market.high_end_companies().stats.average_price()
            x_average = [average, average]
            y_average = [0, self.market.high_end_companies().y_lim().total]
            x_trend = [p.price for p in self.market.high_end_companies().products]
            y_cum_sales = list(itertools.accumulate([p.total_sales / self.market.high_end_companies().total for p in self.market.high_end_companies().products]))
            y_cum_sales = [1 - p for p in y_cum_sales]
        else: raise ValueError()

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        # Plot performance
        x = [p.price for p in low_perf]
        y = [p.total_sales for p in low_perf]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Low",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in mid_perf]
        y = [p.total_sales for p in mid_perf]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Mid",
                alpha=0.3, edgecolors='none')

        x = [p.price for p in high_perf]
        y = [p.total_sales for p in high_perf]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="High",
                alpha=0.3, edgecolors='none')

        # Plot averageline
        plt.plot(x_average, y_average, color="red", linewidth=2, linestyle="--")

        # Plot cumulative sales
        ax2 = ax.twinx()
        ax2.plot(x_trend, y_cum_sales, color="green", linewidth=2, linestyle="--")
        ax2.set_ylim(0, 1)

        y_limit = max([
            self.market.bestseller("H").households_sales,
            self.market.bestseller("HH").high_end_households_sales,
            self.market.bestseller("C").companies_sales,
            self.market.bestseller("HC").high_end_households_sales,
        ])
        ax.legend()
        ax.set_title(f"{group} Average")
        ax.set_xlabel("price €")
        ax.set_ylabel("sales k")
        ax.set_ylim(0, 150)
        ax.grid(True)

    # ADVERTIZING -- #
    def advertizing(self):
        self.all_advertizing()
        self.all_awareness()
        self.hh_awareness()
        self.h_awareness()
        self.hc_awareness()
        self.c_awareness()
        self.awareness_x_sales()
        plt.show()
        
    def all_advertizing(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        y = [p.total_sales for p in source]

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        ax.plot(x, y)
        ax.set_title("All Advertizing")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("sales k")
        
    def all_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        
        awareness_h = [p.households_awareness for p in source]
        awareness_hh = [p.high_end_households_awareness for p in source]
        awareness_c = [p.companies_awareness for p in source]
        awareness_hc = [p.high_end_companies_awareness for p in source]

        awareness_counts = {
            "H": awareness_h,
            "HH": awareness_hh,
            "C": awareness_c,
            "HC": awareness_hc,
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, awareness_count in awareness_counts.items():
            p = ax.bar(x, awareness_count, width, label=boolean, bottom=bottom)
            bottom += awareness_count

        ax.set_title("All Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")
        
    def h_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        
        awareness_h = [p.households_awareness for p in source]
        awareness_hh = [p.high_end_households_awareness for p in source]
        awareness_c = [p.companies_awareness for p in source]
        awareness_hc = [p.high_end_companies_awareness for p in source]

        awareness_counts = {
            "H": awareness_h,          
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, awareness_count in awareness_counts.items():
            p = ax.bar(x, awareness_count, width, label=boolean, bottom=bottom)
            bottom += awareness_count

        # Calculate the best-fit line
        z = np.polyfit(x, awareness_h, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("H Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")
        
    def hh_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        
        awareness_h = [p.households_awareness for p in source]
        awareness_hh = [p.high_end_households_awareness for p in source]
        awareness_c = [p.companies_awareness for p in source]
        awareness_hc = [p.high_end_companies_awareness for p in source]

        awareness_counts = {
            "HH": awareness_hh,          
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, awareness_count in awareness_counts.items():
            p = ax.bar(x, awareness_count, width, label=boolean, bottom=bottom)
            bottom += awareness_count

        # Calculate the best-fit line
        z = np.polyfit(x, awareness_hh, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("HH Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")
        
    def c_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        
        awareness_h = [p.households_awareness for p in source]
        awareness_hh = [p.high_end_households_awareness for p in source]
        awareness_c = [p.companies_awareness for p in source]
        awareness_hc = [p.high_end_companies_awareness for p in source]

        awareness_counts = {
            "C": awareness_c,          
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, awareness_count in awareness_counts.items():
            p = ax.bar(x, awareness_count, width, label=boolean, bottom=bottom)
            bottom += awareness_count

        # Calculate the best-fit line
        z = np.polyfit(x, awareness_c, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("C Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")
        
    def hc_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]
        
        awareness_h = [p.households_awareness for p in source]
        awareness_hh = [p.high_end_households_awareness for p in source]
        awareness_c = [p.companies_awareness for p in source]
        awareness_hc = [p.high_end_companies_awareness for p in source]

        awareness_counts = {
            "HC": awareness_hc,          
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, awareness_count in awareness_counts.items():
            p = ax.bar(x, awareness_count, width, label=boolean, bottom=bottom)
            bottom += awareness_count

        # Calculate the best-fit line
        z = np.polyfit(x, awareness_hc, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("HC Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")
        
    def awareness_x_sales(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.total_awareness() for p in source]

        trendline = [p.total_sales for p in source]
        sales_h = [p.households_sales for p in source]
        sales_hh = [p.high_end_households_sales for p in source]
        sales_c = [p.companies_sales for p in source]
        sales_hc = [p.high_end_companies_sales for p in source]

        sales_counts = {
            "H": sales_h,
            "HH": sales_hh,
            "C": sales_c,
            "HC": sales_hc,  
        }
        width = 60

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        bottom = np.zeros(len(x))

        for boolean, sales_count in sales_counts.items():
            p = ax.bar(x, sales_count, width, label=boolean, bottom=bottom)
            bottom += sales_count

        # Calculate the best-fit line
        z = np.polyfit(x, trendline, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("All Awareness x Sales")
        ax.set_xlabel("awareness")
        ax.set_ylabel("sales k")
        ax.legend(loc="upper right")

  
    def advertizing_relook(self):
        self.ad_relook_hc()
        self.ad_relook_hh()
        self.ad_relook_h()
        plt.show()

    def ad_relook_hc(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.battery >= self.market.stats.average_battery()]
        x = [p for p in x if p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Security + Good Battery")
        ax[0,0].set_xlabel("advertizing €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.battery <= self.market.stats.average_battery()]
        x = [p for p in x if not p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No Security + Bad Battery")
        ax[1,0].set_xlabel("advertizing €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.battery_per_euro() >= self.market.stats.average_bpe()]
        x = [p for p in x if p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Security + Good BPE")
        ax[0,1].set_xlabel("advertizing €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.battery_per_euro() <= self.market.stats.average_bpe()]
        x = [p for p in x if not p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No Security + Bad BPE")
        ax[1,1].set_xlabel("advertizing €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)

        fig.tight_layout()
  
    def ad_relook_hh(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.performance >= self.market.stats.average_performance()]
        x = [p for p in x if p.camera]
        y = [p.high_end_households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Camera + Good Performance")
        ax[0,0].set_xlabel("advertizing €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.performance <= self.market.stats.average_performance()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.high_end_households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No C/M + Bad Performance")
        ax[1,0].set_xlabel("advertizing €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.performance_per_euro() >= self.market.stats.average_ppe()]
        x = [p for p in x if p.camera]
        y = [p.high_end_households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Camera + Good PPE")
        ax[0,1].set_xlabel("advertizing €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.performance_per_euro() <= self.market.stats.average_ppe()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.high_end_households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No C/M + Bad PPE")
        ax[1,1].set_xlabel("advertizing €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)

        fig.tight_layout()

    def ad_relook_h(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.price <= self.market.households().stats.average_price()]
        x = [p for p in x if p.camera]
        y = [p.households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Camera + Cheap")
        ax[0,0].set_xlabel("advertizing €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.price >= self.market.households().stats.average_price()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No C/M + Expensive")
        ax[1,0].set_xlabel("advertizing €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.performance_per_euro() >= self.market.stats.average_ppe()]
        x = [p for p in x if p.camera]
        y = [p.households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Camera + Good PPE")
        ax[0,1].set_xlabel("advertizing €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.performance_per_euro() <= self.market.stats.average_ppe()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.households_sales for p in x]
        x = [p.advertizing for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No C/M + Bad PPE")
        ax[1,1].set_xlabel("advertizing €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)

        fig.tight_layout()
  

    # -- CHANNEL INVESTMENTS -- #
    def channel_investments(self):
        self.channel_investments_hc()
        self.channel_investments_hh()
        self.channel_investments_h()
        plt.show()

    def channel_investments_hc(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.channel_investments)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.battery >= self.market.stats.average_battery()]
        x = [p for p in x if p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Security + Good Battery")
        ax[0,0].set_xlabel("channel investments €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.battery <= self.market.stats.average_battery()]
        x = [p for p in x if not p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No Security + Bad Battery")
        ax[1,0].set_xlabel("channel investments €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.battery_per_euro() >= self.market.stats.average_bpe()]
        x = [p for p in x if p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Security + Good BPE")
        ax[0,1].set_xlabel("channel investments €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.battery_per_euro() <= self.market.stats.average_bpe()]
        x = [p for p in x if not p.security]
        y = [p.high_end_companies_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No Security + Bad BPE")
        ax[1,1].set_xlabel("channel investments €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)


        fig.tight_layout()
  
    def channel_investments_hh(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.channel_investments)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.performance >= self.market.stats.average_performance()]
        x = [p for p in x if p.camera]
        y = [p.high_end_households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Camera + Good Performance")
        ax[0,0].set_xlabel("channel investments €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.performance <= self.market.stats.average_performance()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.high_end_households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No C/M + Bad Performance")
        ax[1,0].set_xlabel("channel investments €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.performance_per_euro() >= self.market.stats.average_ppe()]
        x = [p for p in x if p.camera]
        y = [p.high_end_households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Camera + Good PPE")
        ax[0,1].set_xlabel("channel investments €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.performance_per_euro() <= self.market.stats.average_ppe()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.high_end_households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No C/M + Bad PPE")
        ax[1,1].set_xlabel("channel investments €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)

        fig.tight_layout()

    def channel_investments_h(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.channel_investments)

        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        # 1
        x = [p for p in source if p.price <= self.market.households().stats.average_price()]
        x = [p for p in x if p.camera]
        y = [p.households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,0].set_title("Camera + Cheap")
        ax[0,0].set_xlabel("channel investments €")
        ax[0,0].set_ylabel("sales k")
        ax[0,0].set_ylim(0)

        # 2
        x = [p for p in source if p.price >= self.market.households().stats.average_price()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,0].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,0].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,0].set_title("No C/M + Expensive")
        ax[1,0].set_xlabel("channel investments €")
        ax[1,0].set_ylabel("sales k")
        ax[1,0].set_ylim(0)

        # 3
        x = [p for p in source if p.performance_per_euro() >= self.market.stats.average_ppe()]
        x = [p for p in x if p.camera]
        y = [p.households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[0,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[0,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[0,1].set_title("Camera + Good PPE")
        ax[0,1].set_xlabel("channel investments €")
        ax[0,1].set_ylabel("sales k")
        ax[0,1].set_ylim(0)

        # 4
        x = [p for p in source if p.performance_per_euro() <= self.market.stats.average_ppe()]
        x = [p for p in x if not p.camera or not p.memory]
        y = [p.households_sales for p in x]
        x = [p.channel_investments for p in x]
        ax[1,1].scatter(x, y)

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[1,1].plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax[1,1].set_title("No C/M + Bad PPE")
        ax[1,1].set_xlabel("channel investments €")
        ax[1,1].set_ylabel("sales k")
        ax[1,1].set_ylim(0)

        fig.tight_layout()
  

    # -- PROFIT -- #

    def profit(self):
    
        source = self.market.products.copy()

        source.sort(key=lambda p: p.price)
        y = [p.margin() * p.total_sales for p in source]
        x_price = [p.price for p in source]

        source.sort(key=lambda p: p.total_sales)
        y = [p.margin() * p.total_sales for p in source]
        x_sales = [p.total_sales for p in source]

        source.sort(key=lambda p: p.margin())
        y = [p.margin() * p.total_sales for p in source]
        x_margin = [p.margin() for p in source]

        source.sort(key=lambda p: abs(p.price - self.market.stats.average_price()))
        y = [p.margin() * p.total_sales for p in source]
        x_deviance = [abs(p.price - self.market.stats.average_price()) for p in source]


        fig, ax = plt.subplots(2,2)
        fig.suptitle(self.title)

        ax[0,0].plot(x_price, y); ax[0,0].set_title("Price"); ax[0,0].set_ylabel("profit"); ax[0,0].set_xlabel("price €")
        ax[0,1].plot(x_sales, y); ax[0,1].set_title("Sales"); ax[0,1].set_ylabel("profit"); ax[0,1].set_xlabel("sales k")
        ax[1,0].plot(x_margin, y); ax[1,0].set_title("Margin"); ax[1,0].set_ylabel("profit"); ax[1,0].set_xlabel("margin €")
        ax[1,1].plot(x_deviance, y); ax[1,1].set_title("Deviance"); ax[1,1].set_ylabel("profit"); ax[1,1].set_xlabel("deviance from median price €")

        fig.tight_layout()
        plt.show()

    def profit_x_specs(self):
        source = self.market.products

        # Performance
        source.sort(key=lambda p: p.performance)
        x = [p.performance for p in source]
        y = [p.margin() * p.total_sales for p in source]
        
        fig, ax = plt.subplots(2)
        ax[0].set_ylabel("profit")
        ax[0].set_xlabel("performance")
        ax[0].plot(x, y)

        # Battery
        source.sort(key=lambda p: p.battery)
        x = [p.battery for p in source]
        y = [p.margin() * p.total_sales for p in source]

        ax[1].set_ylabel("profit")
        ax[1].set_xlabel("battery")
        ax[1].plot(x, y)

        fig.tight_layout()
        plt.show()