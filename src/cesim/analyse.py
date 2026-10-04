import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Literal
import pandas as pd
import textwrap
import itertools
from contextlib import suppress
from pprint import pprint

from .market import Market, MarketHistory
from .product import Product



class Analyse:

    def __init__(self, market_history:MarketHistory, round:int, area:Literal["europe", "asia"]) -> None:
        self.market_history: MarketHistory = market_history
        self.market: Market = market_history.loc(round, area)
        self.title: str = f"Round {round}"
        self.compare = Comparisons(self.market, round)

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
            y_limit = self.market.households().sport().y_lim().feature
        elif group == "HH":
            phones = self.market.high_end_households()
            y_limit = self.market.high_end_households().sport().y_lim().feature
        elif group == "C":
            phones = self.market.companies()
            y_limit = self.market.companies().sport().y_lim().feature
        elif group == "HC":
            phones = self.market.high_end_companies()
            y_limit = self.market.high_end_companies().sport().y_lim().feature
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
        ax.set_ylim(0, y_limit*1.2)

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

        x_classics = [p.performance for p in classics]
        x_avants = [p.performance for p in avants]
        x_sports = [p.performance for p in sports]
        x_trendline = [p.performance for p in self.market.products]
        x_dispersion = [p.performance for p in self.market.products]
        x_dispersion.sort()
        all_by_perf = [p for p in self.market.products]
        all_by_perf.sort(key=lambda p: p.performance)
        if group == "H":
            y_limit = self.market.households().y_lim().total

            y_classics = [p.households_sales for p in classics]
            y_avants = [p.households_sales for p in avants]
            y_sports = [p.households_sales for p in sports]

            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_perf]
        elif group == "HH":
            y_limit = self.market.high_end_households().y_lim().total

            y_classics = [p.high_end_households_sales for p in classics]
            y_avants = [p.high_end_households_sales for p in avants]
            y_sports = [p.high_end_households_sales for p in sports]

            y_trendline = [p.high_end_households_sales for p in self.market.products]
            y_dispersion = [p.high_end_households_sales for p in all_by_perf]
        elif group == "C":
            y_limit = self.market.companies().y_lim().total

            y_classics = [p.companies_sales for p in classics]
            y_avants = [p.companies_sales for p in avants]
            y_sports = [p.companies_sales for p in sports]

            y_trendline = [p.companies_sales for p in self.market.products]
            y_dispersion = [p.companies_sales for p in all_by_perf]
        elif group == "HC":
            y_limit = self.market.high_end_companies().y_lim().total

            y_classics = [p.high_end_companies_sales for p in classics]
            y_avants = [p.high_end_companies_sales for p in avants]
            y_sports = [p.high_end_companies_sales for p in sports]

            y_trendline = [p.high_end_companies_sales for p in self.market.products]
            y_dispersion = [p.high_end_companies_sales for p in all_by_perf]
        else: raise ValueError()
        scale = 200

        ax.scatter(x_classics, y_classics, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_avants, y_avants, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_sports, y_sports, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Average
        plt.plot([self.market.stats.average_performance(), self.market.stats.average_performance()], [0, y_limit], color="red", linewidth=2, linestyle="--")

        # Trendline
        z = np.polyfit(x_trendline, y_trendline, 1)
        p = np.poly1d(z)
        plt.plot(x_trendline, p(x_trendline), color="purple", linewidth=2, linestyle="--")

        # Statistical Dispersion
        bins = len(y_dispersion) // 4
        quantile_chunks = np.array_split(y_dispersion, bins)
        quantile_sales = [sum(lst) for lst in quantile_chunks]
        quantile_dispersion = [(sales / sum(y_dispersion)*100) for sales in quantile_sales]

        ax2 = ax.twinx()
        one_step = self.market.stats.max_performance() / bins
        ax2.plot([one_step*i for i in range(1, bins+1)], quantile_dispersion, color="yellow", linewidth=2, linestyle="--")
        ax2.set_ylabel("sales %")
        ax2.set_ylim(0)
        

        ax.legend()
        ax.set_title(f"{group} Performance")
        ax.set_xlabel("performance per €")
        ax.set_ylabel("sales k")
        ax.set_ylim(0, y_limit*1.04)
        ax.set_xlim(self.market.stats.min_performance(), self.market.stats.max_performance())
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

        x_classics = [p.battery for p in classics]
        x_avants = [p.battery for p in avants]
        x_sports = [p.battery for p in sports]
        x_trendline = [p.battery for p in self.market.products]
        x_dispersion = [p.battery for p in self.market.products]
        x_dispersion.sort()
        all_by_perf = [p for p in self.market.products]
        all_by_perf.sort(key=lambda p: p.battery)        
        if group == "H":
            y_limit = self.market.households().y_lim().total

            y_classics = [p.households_sales for p in classics]
            y_avants = [p.households_sales for p in avants]
            y_sports = [p.households_sales for p in sports]

            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_perf]
        elif group == "HH":
            y_limit = self.market.high_end_households().y_lim().total

            y_classics = [p.high_end_households_sales for p in classics]
            y_avants = [p.high_end_households_sales for p in avants]
            y_sports = [p.high_end_households_sales for p in sports]
            
            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_perf]
        elif group == "C":
            y_limit = self.market.companies().y_lim().total

            y_classics = [p.companies_sales for p in classics]
            y_avants = [p.companies_sales for p in avants]
            y_sports = [p.companies_sales for p in sports]
            
            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_perf]
        elif group == "HC":
            y_limit = self.market.high_end_companies().y_lim().total

            y_classics = [p.high_end_companies_sales for p in classics]
            y_avants = [p.high_end_companies_sales for p in avants]
            y_sports = [p.high_end_companies_sales for p in sports]
            
            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_perf]
        else: raise ValueError()
        scale = 200

        ax.scatter(x_classics, y_classics, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_avants, y_avants, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_sports, y_sports, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')
        
        # Average
        plt.plot([self.market.stats.average_battery(), self.market.stats.average_battery()], [0, y_limit], color="red", linewidth=2, linestyle="--")
        
        # Trendline
        z = np.polyfit(x_trendline, y_trendline, 1)
        p = np.poly1d(z)
        plt.plot(x_trendline, p(x_trendline), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title(f"{group} Battery")
        ax.set_xlabel("battery per €")
        ax.set_ylabel("sales k")
        ax.set_ylim(0, y_limit*1.04)
        ax.set_xlim(self.market.stats.min_battery(), self.market.stats.max_battery())
        ax.grid(True)

        # Statistical Dispersion
        bins = len(y_dispersion) // 4
        quantile_chunks = np.array_split(y_dispersion, bins)
        quantile_sales = [sum(lst) for lst in quantile_chunks]
        quantile_dispersion = [(sales / sum(y_dispersion)*100) for sales in quantile_sales]

        ax2 = ax.twinx()
        one_step = self.market.stats.max_performance() / bins
        ax2.plot([one_step*i for i in range(1, bins+1)], quantile_dispersion, color="yellow", linewidth=2, linestyle="--")
        ax2.set_ylabel("sales %")
        ax2.set_ylim(0)

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

        x = [p.performance_per_euro for p in classics]
        y = [p.total_sales for p in classics]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.performance_per_euro for p in avants]
        y = [p.total_sales for p in avants]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.performance_per_euro for p in sports]
        y = [p.total_sales for p in sports]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Trendline
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

        x_classics = [p.performance_per_euro for p in classics]
        x_avants = [p.performance_per_euro for p in avants]
        x_sports = [p.performance_per_euro for p in sports]
        x_trendline = [p.performance_per_euro for p in self.market.products]
        x_dispersion = [p.performance_per_euro for p in self.market.products]
        x_dispersion.sort()
        all_by_ppe = [p for p in self.market.products]
        all_by_ppe.sort(key=lambda p: p.performance_per_euro)         
        if group == "H":
            y_limit = self.market.households().y_lim().total

            y_classics = [p.households_sales for p in classics]
            y_avants = [p.households_sales for p in avants]
            y_sports = [p.households_sales for p in sports]

            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_ppe]
        elif group == "HH":
            y_limit = self.market.high_end_households().y_lim().total

            y_classics = [p.high_end_households_sales for p in classics]
            y_avants = [p.high_end_households_sales for p in avants]
            y_sports = [p.high_end_households_sales for p in sports]
          
            y_trendline = [p.high_end_households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_ppe]
        elif group == "C":
            y_limit = self.market.companies().y_lim().total

            y_classics = [p.companies_sales for p in classics]
            y_avants = [p.companies_sales for p in avants]
            y_sports = [p.companies_sales for p in sports]
         
            y_trendline = [p.companies_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_ppe]
        elif group == "HC":
            y_limit = self.market.high_end_companies().y_lim().total

            y_classics = [p.high_end_companies_sales for p in classics]
            y_avants = [p.high_end_companies_sales for p in avants]
            y_sports = [p.high_end_companies_sales for p in sports]

            y_trendline = [p.high_end_companies_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_ppe]
        else: raise ValueError()
        scale = 200

        ax.scatter(x_classics, y_classics, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_avants, y_avants, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_sports, y_sports, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Average
        plt.plot([self.market.stats.average_ppe(), self.market.stats.average_ppe()], [0, y_limit], color="red", linewidth=2, linestyle="--")

        # Trendline
        z = np.polyfit(x_trendline, y_trendline, 1)
        p = np.poly1d(z)
        plt.plot(x_trendline, p(x_trendline), color="purple", linewidth=2, linestyle="--")


        ax.legend()
        ax.set_title(f"{group} Performance / €")
        ax.set_xlabel("performance per €")
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

        x = [p.battery_per_euro for p in classics]
        y = [p.total_sales for p in classics]
        scale = 200
        ax.scatter(x, y, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro for p in avants]
        y = [p.total_sales for p in avants]
        scale = 200
        ax.scatter(x, y, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        x = [p.battery_per_euro for p in sports]
        y = [p.total_sales for p in sports]
        scale = 200
        ax.scatter(x, y, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Trendline
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

        x_classics = [p.battery_per_euro for p in classics]
        x_avants = [p.battery_per_euro for p in avants]
        x_sports = [p.battery_per_euro for p in sports]
        x_trendline = [p.battery_per_euro for p in self.market.products]
        x_dispersion = [p.battery_per_euro for p in self.market.products]
        x_dispersion.sort()
        all_by_bpe = [p for p in self.market.products]
        all_by_bpe.sort(key=lambda p: p.battery_per_euro) 
        if group == "H":
            y_limit = self.market.households().y_lim().total

            y_classics = [p.households_sales for p in classics]
            y_avants = [p.households_sales for p in avants]
            y_sports = [p.households_sales for p in sports]

            y_trendline = [p.households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_bpe]
        elif group == "HH":
            y_limit = self.market.high_end_households().y_lim().total

            y_classics = [p.high_end_households_sales for p in classics]
            y_avants = [p.high_end_households_sales for p in avants]
            y_sports = [p.high_end_households_sales for p in sports]

            y_trendline = [p.high_end_households_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_bpe]
        elif group == "C":
            y_limit = self.market.companies().y_lim().total

            y_classics = [p.companies_sales for p in classics]
            y_avants = [p.companies_sales for p in avants]
            y_sports = [p.companies_sales for p in sports]

            y_trendline = [p.companies_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_bpe]
        elif group == "HC":
            y_limit = self.market.high_end_companies().y_lim().total

            y_classics = [p.high_end_companies_sales for p in classics]
            y_avants = [p.high_end_companies_sales for p in avants]
            y_sports = [p.high_end_companies_sales for p in sports]

            y_trendline = [p.high_end_companies_sales for p in self.market.products]
            y_dispersion = [p.households_sales for p in all_by_bpe]
        else: raise ValueError()
        scale = 200

        ax.scatter(x_classics, y_classics, c=f"tab:blue", s=scale, label="Classic",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_avants, y_avants, c=f"tab:orange", s=scale, label="Avant garde",
                alpha=0.3, edgecolors='none')

        ax.scatter(x_sports, y_sports, c=f"tab:green", s=scale, label="Sport",
                alpha=0.3, edgecolors='none')

        # Average
        plt.plot([self.market.stats.average_bpe(), self.market.stats.average_bpe()], [0, y_limit], color="red", linewidth=2, linestyle="--")

        # Trendline
        z = np.polyfit(x_trendline, y_trendline, 1)
        p = np.poly1d(z)
        plt.plot(x_trendline, p(x_trendline), color="purple", linewidth=2, linestyle="--")

        ax.legend()
        ax.set_title(f"{group} Battery / €")
        ax.set_xlabel("battery per €")
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

        # Trendline
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

        # Trendline
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
        source.sort(key=lambda p: p.margin)
        x = [p.margin for p in source]
        y = [p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        ax.set_ylabel("sales k")
        ax.set_xlabel("margin €")
        ax.plot(x, y)

        # Trendline
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

    # -- ADVERTIZING -- #
    def advertizing(self):
        #self.ad_effect_teams()
        #self.all_advertizing()
        self.awareness_to_intentions_history_by_teams_and_groups()
        #self.money_to_awareness_history_by_teams_and_groups()
        #self.team_ad_effect_history()
        #self.advertizing_x_sales()
        #self.all_awareness()
        #self.awareness_x_sales()
        plt.show()
        
    def all_advertizing(self):
        x_pink = [p.advertizing for p in self.market.brand().pink.products]
        x_green = [p.advertizing for p in self.market.brand().green.products]
        x_grey = [p.advertizing for p in self.market.brand().grey.products]
        x_orange = [p.advertizing for p in self.market.brand().orange.products]
        x_blue = [p.advertizing for p in self.market.brand().blue.products]
        x_red = [p.advertizing for p in self.market.brand().red.products]

        y_pink = [p.total_sales for p in self.market.brand().pink.products]
        y_green = [p.total_sales for p in self.market.brand().green.products]
        y_grey = [p.total_sales for p in self.market.brand().grey.products]
        y_orange = [p.total_sales for p in self.market.brand().orange.products]
        y_blue = [p.total_sales for p in self.market.brand().blue.products]
        y_red = [p.total_sales for p in self.market.brand().red.products]

        fig, ax = plt.subplots()
        fig.suptitle(self.title)

        ax.scatter(x_pink, y_pink, c="tab:pink")
        ax.scatter(x_green, y_green, c="tab:green")
        ax.scatter(x_grey, y_grey, c="tab:grey")
        ax.scatter(x_orange, y_orange, c="tab:orange")
        ax.scatter(x_blue, y_blue, c="tab:blue")
        ax.scatter(x_red, y_red, c="tab:red")

        z = np.polyfit(x_pink, y_pink, 1)
        p = np.poly1d(z)
        ax.plot(x_pink, p(x_pink), color="pink", linewidth=2, linestyle="--")

        z = np.polyfit(x_green, y_green, 1)
        p = np.poly1d(z)
        ax.plot(x_green, p(x_green), color="green", linewidth=2, linestyle="--")

        z = np.polyfit(x_grey, y_grey, 1)
        p = np.poly1d(z)
        ax.plot(x_grey, p(x_grey), color="grey", linewidth=2, linestyle="--")

        z = np.polyfit(x_orange, y_orange, 1)
        p = np.poly1d(z)
        ax.plot(x_orange, p(x_orange), color="orange", linewidth=2, linestyle="--")

        z = np.polyfit(x_blue, y_blue, 1)
        p = np.poly1d(z)
        ax.plot(x_blue, p(x_blue), color="blue", linewidth=2, linestyle="--")

        z = np.polyfit(x_red, y_red, 1)
        p = np.poly1d(z)
        ax.plot(x_red, p(x_red), color="red", linewidth=2, linestyle="--")
                       # 1200, 140     3100, 340 k=0.105
        ax.set_title("Teams Advertizing")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("sales k")
        ax.set_ylim(0)
        
    def all_awareness(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]

        trendline = [p.total_awareness for p in source]
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

        # Trendline
        z = np.polyfit(x, trendline, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="grey", linewidth=2, linestyle="--")

        z = np.polyfit(x, awareness_h, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        z = np.polyfit(x, awareness_hh, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="orange", linewidth=2, linestyle="--")

        z = np.polyfit(x, awareness_c, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="green", linewidth=2, linestyle="--")

        z = np.polyfit(x, awareness_hc, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="blue", linewidth=2, linestyle="--")

        ax.set_title("All Awareness")
        ax.set_xlabel("advertizing €")
        ax.set_ylabel("awareness k")
        ax.legend(loc="upper right")

    def awareness_x_sales(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.total_awareness)
        x = [p.total_awareness for p in source]

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

        # Trendline
        z = np.polyfit(x, trendline, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        ax.set_title("All Awareness x Sales")
        ax.set_xlabel("awareness")
        ax.set_ylabel("sales k")
        ax.legend(loc="upper right")
        
    def advertizing_x_sales(self):
        source = self.market.products.copy()
        source.sort(key=lambda p: p.advertizing)
        x = [p.advertizing for p in source]

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

        for key, sales_count in sales_counts.items():
            color = "grey"
            if key == "H":
                color = "purple"
            if key == "HH":
                color = "orange"
            if key == "C":
                color = "green"
            if key == "HC":
                color = "blue"
            p = ax.bar(x, sales_count, width, label=key, bottom=bottom, color=[color])
            bottom += sales_count

        # Trendline
        z = np.polyfit(x, trendline, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="grey", linewidth=2, linestyle="--")

        z = np.polyfit(x, sales_h, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        z = np.polyfit(x, sales_hh, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="orange", linewidth=2, linestyle="--")

        z = np.polyfit(x, sales_c, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="green", linewidth=2, linestyle="--")

        z = np.polyfit(x, sales_hc, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="blue", linewidth=2, linestyle="--")

        ax.set_title("All Advertizing x Sales")
        ax.set_xlabel("advertizing €")
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
        x = [p for p in source if p.battery_per_euro >= self.market.stats.average_bpe()]
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
        x = [p for p in source if p.battery_per_euro <= self.market.stats.average_bpe()]
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
        x = [p for p in source if p.performance_per_euro >= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro <= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro >= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro <= self.market.stats.average_ppe()]
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

    def team_ad_effect_history(self):
        fig, ax = plt.subplots(2, 2)

        # € to Awareness, EUROPE
        blue = [1.527, 0.011]
        green = [-0.080, 0.023, 0.014]
        grey = [0.049, 0.038, 0.072]
        orange = [0.066, 0.052, 0.027]
        pink = [0.105, -0.004]
        red = [0.063, -0.021, 0.016]

        ax[0,0].plot([2,3], blue, color="blue", label="blue")
        ax[0,0].plot([1,2,3], green, color="green", label="green")
        ax[0,0].plot([1,2,3], grey, color="grey", label="grey")
        ax[0,0].plot([1,2,3], orange, color="orange", label="orange")
        ax[0,0].plot([1,2], pink, color="pink", label="pink")
        ax[0,0].plot([1,2,3], red, color="red", label="red")

        ax[0,0].set_title("Awareness per euro, Europe")
        ax[0,0].set_xlabel("Rounds")
        ax[0,0].set_ylabel("Awareness per euro")
        ax[0,0].legend(loc="upper left")
        ax[0,0].set_xticks([1,2,3])

        # € to Awareness, ASIA
        blue = [2.283, 0.013]
        green = [0.069, 0.020]
        grey = [0.164]
        orange = [0.046, 0.011, 0.003]
        pink = []
        red = [0.108, 0.066]

        ax[0,1].plot([2,3], blue, color="blue", label="blue")
        ax[0,1].plot([1,2], green, color="green", label="green")
        ax[0,1].plot([1], grey, color="grey", label="grey")
        ax[0,1].plot([1,2,3], orange, color="orange", label="orange")
        ax[0,1].plot([], pink, color="pink", label="pink")
        ax[0,1].plot([1,2], red, color="red", label="red")

        ax[0,1].set_title("Awareness per euro, Asia")
        ax[0,1].set_xlabel("Rounds")
        ax[0,1].set_ylabel("Awareness per euro")
        ax[0,1].legend(loc="upper left")
        ax[0,1].set_xticks([1,2,3])

        # Awareness to Sales, EUROPE
        blue = [0.197, 0.155]
        green = [0.231, 0.155, 0.146]
        grey = [0.123, 0.223, 0.194]
        orange = [0.162, 0.182, 0.179]
        pink = [0.170, 0.182, -0.288]
        red = [0.183, 0.282, 0.153]

        ax[1,0].plot([2,3], blue, color="blue", label="blue")
        ax[1,0].plot([1,2,3], green, color="green", label="green")
        ax[1,0].plot([1,2,3], grey, color="grey", label="grey")
        ax[1,0].plot([1,2,3], orange, color="orange", label="orange")
        ax[1,0].plot([1,2,3], pink, color="pink", label="pink")
        ax[1,0].plot([1,2,3], red, color="red", label="red")

        ax[1,0].set_title("Sales per Awareness, Europe")
        ax[1,0].set_xlabel("Rounds")
        ax[1,0].set_ylabel("Sales per Awareness")
        ax[1,0].legend(loc="upper left")
        ax[1,0].set_xticks([1,2,3])

        # Awareness to Sales, ASIA
        blue = [0.197, 0.173]
        green = [0.162, 0.169]
        grey = [0.197]
        orange = [0.135, 0.129, 0.154]
        pink = []
        red = [0.219, 0.183]

        ax[1,1].plot([2,3], blue, color="blue", label="blue")
        ax[1,1].plot([1,2], green, color="green", label="green")
        ax[1,1].plot([1], grey, color="grey", label="grey")
        ax[1,1].plot([1,2,3], orange, color="orange", label="orange")
        ax[1,1].plot([], pink, color="pink", label="pink")
        ax[1,1].plot([1,2], red, color="red", label="red")

        ax[1,1].set_title("Sales per Awareness, Asia")
        ax[1,1].set_xlabel("Rounds")
        ax[1,1].set_ylabel("Sales per Awareness")
        ax[1,1].legend(loc="upper left")
        ax[1,1].set_xticks([1,2,3])

        fig.tight_layout()
        plt.show()

    def ad_effect_teams(self):
        brands = [b.lower() for b in self.market.brands]
        brands.sort()
        slopes = dict()
        for brand in brands:
            x = [p.total_awareness for p in self.market.brand()[brand].products]
            y = [p.total_sales for p in self.market.brand()[brand].products]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
            slopes[brand] = slope
        
        print(brands)
        pprint(slopes, sort_dicts=False)
        return slopes

    def money_to_awareness_history_by_teams_and_groups(self):
        groups = ["households", "high_end_households", "companies", "high_end_companies"]
        for group in groups:
            fig, ax = plt.subplots(2,2)
            fig.suptitle(f"{group.capitalize().replace("_", " ")}")

            for j, area in enumerate(self.market_history.columns):
                y_results_ma = dict()
                y_results_as = dict()
                x_results_ma = dict()
                x_results_as = dict()

                for index, europe, asia in self.market_history.rounds():
                    market = europe if area == "europe" else asia
                    for brand in market.brands:
                        if brand not in y_results_ma.keys(): y_results_ma[brand] = []
                        if brand not in y_results_as.keys(): y_results_as[brand] = []
                        if brand not in x_results_ma.keys(): x_results_ma[brand] = []
                        if brand not in x_results_as.keys(): x_results_as[brand] = []

                        products = market.brand()[brand].group()[group].products
                        ma_result = self._money_to_awareness(products)
                        as_result = self._awareness_to_sales(products)

                        if not bool(np.isnan(ma_result)):
                            y_results_ma[brand].append(ma_result)
                            x_results_ma[brand].append(index)
                            
                        if not bool(np.isnan(ma_result)):
                            y_results_as[brand].append(as_result)
                            x_results_as[brand].append(index)


                for brand, value in y_results_ma.items():
                    ax[0,j].plot(x_results_ma[brand], value, label=brand)
                for brand, value in y_results_as.items():
                    ax[1,j].plot(x_results_as[brand], value, label=brand)

                ax[0,j].set_title(f"Awareness per euro, {area}")
                ax[0,j].set_xlabel("Rounds")
                ax[0,j].set_xticks([i for i in range(1, self.market_history._nrounds+1)])

                ax[1,j].set_title(f"Sales per Awareness, {area}")
                ax[1,j].set_xlabel("Rounds")
                ax[1,j].set_xticks([i for i in range(1, self.market_history._nrounds+1)])
                fig.tight_layout()


        plt.show()

    def awareness_to_intentions_history_by_teams_and_groups(self):
        groups = ["households", "high_end_households", "companies", "high_end_companies"]
        for group in groups:
            fig, ax = plt.subplots(2,2)
            fig.suptitle(f"{group.capitalize().replace("_", " ")}")

            for j, area in enumerate(self.market_history.columns):
                y_results_ma = dict()
                y_results_as = dict()
                x_results_ma = dict()
                x_results_as = dict()

                for index, europe, asia in self.market_history.rounds():
                    market = europe if area == "europe" else asia
                    for brand in market.brands:
                        if brand not in y_results_ma.keys(): y_results_ma[brand] = []
                        if brand not in y_results_as.keys(): y_results_as[brand] = []
                        if brand not in x_results_ma.keys(): x_results_ma[brand] = []
                        if brand not in x_results_as.keys(): x_results_as[brand] = []

                        products = market.brand()[brand].group()[group].products
                        ma_result = self._awareness_to_intentions(products)
                        as_result = self._intentions_to_sales(products)

                        if not bool(np.isnan(ma_result)):
                            y_results_ma[brand].append(ma_result)
                            x_results_ma[brand].append(index)
                            
                        if not bool(np.isnan(ma_result)):
                            y_results_as[brand].append(as_result)
                            x_results_as[brand].append(index)


                for brand, value in y_results_ma.items():
                    ax[0,j].plot(x_results_ma[brand], value, label=brand)
                for brand, value in y_results_as.items():
                    ax[1,j].plot(x_results_as[brand], value, label=brand)

                ax[0,j].set_title(f"Intentions per Awareness, {area}")
                ax[0,j].set_xlabel("Rounds")
                ax[0,j].set_xticks([i for i in range(1, self.market_history._nrounds+1)])

                ax[1,j].set_title(f"Sales per Intention, {area}")
                ax[1,j].set_xlabel("Rounds")
                ax[1,j].set_xticks([i for i in range(1, self.market_history._nrounds+1)])
                fig.tight_layout()


        plt.show()


    def _money_to_awareness(self, products:list[Product]):
        x = [p.advertizing for p in products]
        y = [p.total_awareness for p in products]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope

    def _awareness_to_sales(self, products:list[Product]):
        x = [p.total_awareness for p in products]
        y = [p.total_sales for p in products]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope

    def _awareness_to_intentions(self, products:list[Product]):
        x = [p.advertizing for p in products]
        y = [p.total_awareness for p in products]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope

    def _intentions_to_sales(self, products:list[Product]):
        x = [p.total_intentions for p in products]
        y = [p.total_sales for p in products]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        slope = self._calc_k(x[0], x[-1], p(x)[0], p(x)[-1])
        return slope


    
    def _calc_k(self, x1, x2, y1, y2):
        """kulmakerroin"""
        if x1 == x2: return np.nan
        k = (y2-y1) / (x2-x1)
        return k
  
    # -- CHANNEL INVESTMENTS -- #
    def channel_investments(self):
        self.all_channel_investments()
        self.channel_investments_hc()
        self.channel_investments_hh()
        self.channel_investments_h()
        plt.show()

    def all_channel_investments(self):
        source = self.market.products

        x = [p.channel_investments for p in source]
        y = [p.total_sales for p in source]
        
        fig, ax = plt.subplots()
        fig.suptitle(self.title)
        ax.scatter(x,y)
        ax.set_title("Channel Investments")
        ax.set_xlabel("investment €")
        ax.set_ylabel("sales k")

        # Trendline
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), color="purple", linewidth=2, linestyle="--")

        plt.show()

        # x  600, y 216.5
        # x 1400, y 231.4
        #    800     14.9
        #    14.9 / 800 = 0.01862

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
        x = [p for p in source if p.battery_per_euro >= self.market.stats.average_bpe()]
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
        x = [p for p in source if p.battery_per_euro <= self.market.stats.average_bpe()]
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
        x = [p for p in source if p.performance_per_euro >= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro <= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro >= self.market.stats.average_ppe()]
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
        x = [p for p in source if p.performance_per_euro <= self.market.stats.average_ppe()]
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
        y = [p.margin * p.total_sales for p in source]
        x_price = [p.price for p in source]

        source.sort(key=lambda p: p.total_sales)
        y = [p.margin * p.total_sales for p in source]
        x_sales = [p.total_sales for p in source]

        source.sort(key=lambda p: p.margin)
        y = [p.margin * p.total_sales for p in source]
        x_margin = [p.margin for p in source]

        source.sort(key=lambda p: abs(p.price - self.market.stats.average_price()))
        y = [p.margin * p.total_sales for p in source]
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
        y = [p.margin * p.total_sales for p in source]
        
        fig, ax = plt.subplots(2)
        ax[0].set_ylabel("profit")
        ax[0].set_xlabel("performance")
        ax[0].plot(x, y)

        # Battery
        source.sort(key=lambda p: p.battery)
        x = [p.battery for p in source]
        y = [p.margin * p.total_sales for p in source]

        ax[1].set_ylabel("profit")
        ax[1].set_xlabel("battery")
        ax[1].plot(x, y)

        fig.tight_layout()
        plt.show()

    # -- COMPETITION -- #
    def competion(self, 
                  camera:bool=False, memory:bool=False, display:bool=False, resistance:bool=False, security:bool=False, 
                  classic:bool=False, avant_garde:bool=False, sport:bool=False):
        
        source = self.market
        if camera:
            source = source.camera()
        if memory:
            source = source.memory()
        if display:
            source = source.display()
        if resistance:
            source = source.resistance()
        if security:
            source = source.security()

        if sport:
            source = source.sport()
        if avant_garde:
            source = source.avant_garde()
        if classic:
            source = source.classic()

        # COMPETITION #
        x_classics = [p.price for p in source.classic().products]
        x_avants = [p.price for p in source.avant_garde().products]
        x_sports = [p.price for p in source.sport().products]
        y_classics = [p.performance + p.battery for p in source.classic().products]
        y_avants = [p.performance + p.battery for p in source.avant_garde().products]
        y_sports = [p.performance + p.battery for p in source.sport().products]

        # DEMAND #
        x_price = [p.price for p in source.products]
        y_h_sales = [p.households_sales for p in source.products]
        y_hh_sales = [p.high_end_households_sales for p in source.products]
        y_c_sales = [p.companies_sales for p in source.products]
        y_hc_sales = [p.high_end_companies_sales for p in source.products]
        y_total_sales = [p.total_sales for p in source.products]

        # PLOT COMPETITION #
        fig, ax = plt.subplots()
        ax.scatter(x_classics, y_classics, c="tab:blue")
        ax.scatter(x_avants, y_avants, c="tab:orange")
        ax.scatter(x_sports, y_sports, c="tab:green")
        ax.set_xlabel("price €")
        ax.set_ylabel("specs")

        # PLOT DEMAND #
        ax2 = ax.twinx()
        ax2.plot(x_price, y_h_sales, color="purple", label="Households")
        ax2.plot(x_price, y_hh_sales, color="orange", label="High-End Households")
        ax2.plot(x_price, y_c_sales, color="green", label="Companies")
        ax2.plot(x_price, y_hc_sales, color="blue", label="High-End Companies")
        ax2.plot(x_price, y_total_sales, color="grey", label="Total sales", linestyle="--")
        ax2.set_ylabel("sales k")
        ax2.legend(loc="upper left")

        plt.show()

    def competion_stack(self, 
                  camera:bool=False, memory:bool=False, display:bool=False, resistance:bool=False, security:bool=False, 
                  classic:bool=False, avant_garde:bool=False, sport:bool=False, new_products:list=[]):
        
        source = self.market
        if camera:
            source = source.camera()
        if memory:
            source = source.memory()
        if display:
            source = source.display()
        if resistance:
            source = source.resistance()
        if security:
            source = source.security()

        if sport:
            source = source.sport()
        if avant_garde:
            source = source.avant_garde()
        if classic:
            source = source.classic()

        # COMPETITION #
        if new_products:
            x_classics = [p.price for p in source.classic().products if p.brand != "Pink"]
            x_avants = [p.price for p in source.avant_garde().products if p.brand != "Pink"]
            x_sports = [p.price for p in source.sport().products  if p.brand != "Pink"]
            y_classics = [p.performance + p.battery for p in source.classic().products if p.brand != "Pink"]
            y_avants = [p.performance + p.battery for p in source.avant_garde().products if p.brand != "Pink"]
            y_sports = [p.performance + p.battery for p in source.sport().products if p.brand != "Pink"]
        else:
            x_classics = [p.price for p in source.classic().products]
            x_avants = [p.price for p in source.avant_garde().products]
            x_sports = [p.price for p in source.sport().products ]
            y_classics = [p.performance + p.battery for p in source.classic().products]
            y_avants = [p.performance + p.battery for p in source.avant_garde().products]
            y_sports = [p.performance + p.battery for p in source.sport().products]

        # HYPOTETICAL
        x_hypotetical = [n[0] for n in new_products]
        y_hypotetical = [n[1] for n in new_products]

        # DEMAND #
        x_price = [p.price for p in source.products]
        y_h_sales = [p.households_sales for p in source.products]
        y_hh_sales = [p.high_end_households_sales for p in source.products]
        y_c_sales = [p.companies_sales for p in source.products]
        y_hc_sales = [p.high_end_companies_sales for p in source.products]
        y_total_sales = [p.total_sales for p in source.products]

        # PLOT COMPETITION #
        fig, ax = plt.subplots()
        ax.scatter(x_classics, y_classics, c="tab:blue")
        ax.scatter(x_avants, y_avants, c="tab:orange")
        ax.scatter(x_sports, y_sports, c="tab:green")
        ax.set_xlabel("price €")
        ax.set_ylabel("specs")

        # PLOT HYPOTETICAL
        ax.scatter(x_hypotetical, y_hypotetical, c="tab:pink")

        # PLOT DEMAND #
        ax2 = ax.twinx()
        y = np.vstack([y_h_sales, y_hh_sales, y_c_sales, y_hc_sales])
        ax2.stackplot(x_price, y, alpha=0.2, colors=["purple", "orange", "green", "blue"])

        ax2.set_ylabel("sales k")
        ax2.legend(loc="upper left")

        plt.show()

    # -- DEMAND -- #

    def price_demand(self, 
                  camera:bool=False, memory:bool=False, display:bool=False, resistance:bool=False, security:bool=False, 
                  classic:bool=False, avant_garde:bool=False, sport:bool=False):
        
        source = self.market
        if camera:
            source = source.camera()
        if memory:
            source = source.memory()
        if display:
            source = source.display()
        if resistance:
            source = source.resistance()
        if security:
            source = source.security()

        if sport:
            source = source.sport()
        if avant_garde:
            source = source.avant_garde()
        if classic:
            source = source.classic()

        # COMPETITION #
        x_classics = [p.price for p in source.classic().products]
        x_avants = [p.price for p in source.avant_garde().products]
        x_sports = [p.price for p in source.sport().products]
        y_classics = [p.performance + p.battery for p in source.classic().products]
        y_avants = [p.performance + p.battery for p in source.avant_garde().products]
        y_sports = [p.performance + p.battery for p in source.sport().products]

        # DEMAND #
        x_price = [p.price for p in source.products]
        y_h_sales = [p.households_sales for p in source.products]
        y_hh_sales = [p.high_end_households_sales for p in source.products]
        y_c_sales = [p.companies_sales for p in source.products]
        y_hc_sales = [p.high_end_companies_sales for p in source.products]
        y_total_sales = [p.total_sales for p in source.products]

        # PLOT COMPETITION #
        fig, ax = plt.subplots(2,2)
        ax[0,0].scatter(x_classics, y_classics, c="tab:blue")
        ax[0,0].scatter(x_avants, y_avants, c="tab:orange")
        ax[0,0].scatter(x_sports, y_sports, c="tab:green")
        ax[0,0].set_xlabel("price €")
        ax[0,0].set_ylabel("specs")

        ax[0,1].scatter(x_classics, y_classics, c="tab:blue")
        ax[0,1].scatter(x_avants, y_avants, c="tab:orange")
        ax[0,1].scatter(x_sports, y_sports, c="tab:green")
        ax[0,1].set_xlabel("price €")
        ax[0,1].set_ylabel("specs")

        ax[1,0].scatter(x_classics, y_classics, c="tab:blue")
        ax[1,0].scatter(x_avants, y_avants, c="tab:orange")
        ax[1,0].scatter(x_sports, y_sports, c="tab:green")
        ax[1,0].set_xlabel("price €")
        ax[1,0].set_ylabel("specs")

        ax[1,1].scatter(x_classics, y_classics, c="tab:blue")
        ax[1,1].scatter(x_avants, y_avants, c="tab:orange")
        ax[1,1].scatter(x_sports, y_sports, c="tab:green")
        ax[1,1].set_xlabel("price €")
        ax[1,1].set_ylabel("specs")

        # PLOT DEMAND #
        divitions = 11
        y_h_ = np.array_split(y_h_sales, divitions)
        y_hh_ = np.array_split(y_hh_sales, divitions)
        y_c_ = np.array_split(y_c_sales, divitions)
        y_hc_ = np.array_split(y_hc_sales, divitions)

        y_h = [sum(p) / source.households().total * 100 for p in y_h_]
        y_hh = [sum(p) / source.high_end_households().total * 100 for p in y_hh_]
        y_c = [sum(p) / source.companies().total * 100 for p in y_c_]
        y_hc = [sum(p) / source.high_end_companies().total * 100 for p in y_hc_]

        x_range = self.market.stats.max_price() - self.market.stats.min_price()
        x_step = x_range / divitions
        x_start = self.market.stats.min_price()
        x = [x_start]
        
        for i in range(1, divitions):
            x.insert(i, x[i-1] + x_step)
        axh = ax[0,0].twinx()
        axh.bar(x, y_h, alpha=0.2, color=["purple"], width=x_step)
        axh.set_ylabel("sales k")
        axh.legend(loc="upper left")
        print("")
        print([round(_) for _ in x])
        print("")
        print([round(float(_)) for _ in y_hc])
        print("")
        
        axhh = ax[0,1].twinx()
        axhh.bar(x, y_hh, alpha=0.2, color=["orange"], width=x_step)
        axhh.set_ylabel("sales k")
        axhh.legend(loc="upper left")
        
        axc = ax[1,0].twinx()
        axc.bar(x, y_c, alpha=0.2, color=["green"], width=x_step)
        axc.set_ylabel("sales k")
        axc.legend(loc="upper left")
        
        axhc = ax[1,1].twinx()
        axhc.bar(x, y_hc, alpha=0.2, color=["blue"], width=x_step)
        axhc.set_ylabel("sales k")
        axhc.legend(loc="upper left")

        plt.show()

    def demand(self, market:Market):

        situation = pd.DataFrame(columns=[
            "price",
            "performance",
            "battery",
            
            "h_sales",
            "hh_sales",
            "c_sales",
            "hc_sales",
            "total_sales",

            "ads",
            "h_awareness",
            "hh_awareness",
            "c_awareness",
            "hc_awareness",
            "total_awareness",
            "base_awareness",
            
            "channel_investments",
            "specialist",
            "generalist",
            "online",

        ])
        for i, product in enumerate(market.products, 1):
            situation.loc[i] = [
                # specs
                product.price,
                product.performance,
                product.battery,

                # sales
                product.households_sales,
                product.high_end_households_sales,
                product.companies_sales,
                product.high_end_companies_sales,
                product.total_sales,

                # ads
                product.advertizing,
                product.households_awareness,
                product.high_end_households_awareness,
                product.companies_awareness,
                product.high_end_companies_awareness,
                product.total_awareness,
                product.total_awareness - (product.advertizing * 0.2),

                # 
                product.channel_investments,
                product.specialist,
                product.generalist,
                product.online,
            ]
        return situation



class DisplayPhone:

    def __init__(self) -> None:
        self.name = True
        self.company = False
        self.price = False
        self.variable_unit_cost = False

        # Sales
        self.households_sales = False
        self.high_end_households_sales = False
        self.companies_sales = False
        self.high_end_companies_sales = False
        self.total_sales = False

        # Sales by distribution channel
        self.specialist = False
        self.generalist = False
        self.online = False
        
        # Market share %
        self.households_market_share = False
        self.high_end_households_market_share = False
        self.companies_market_share = False
        self.high_end_companies_market_share = False
        
        # Marketing
        self.advertizing = False
        self.channel_investments = False

        # Product characteristics
        self.performance = False
        self.battery = False
        self.camera = False
        self.memory = False
        self.display = False
        self.resistance = False
        self.security = False
        self.design = False

        # Awareness & Intention
        self.households_awareness = False
        self.high_end_households_awareness = False
        self.companies_awareness = False
        self.high_end_companies_awareness = False

        self.households_intention = False
        self.high_end_households_intention = False
        self.companies_intention = False
        self.high_end_companies_intention = False

        self.margin = False
        self.margin_percent = False
        self.performance_per_euro = False
        self.battery_per_euro = False
        self.total_awareness = False
        self.profit = False
        self.audience = False

    def empty(self):
        keys = list(self.__dict__.keys())
        for key in keys:
            self.__delattr__(key)
        #self.__setattr__("", None)
        return self

    def __call__(self, product:Product) -> DisplayPhone:
        keys = list(self.__dict__.keys())
        new_instance = super().__new__(self.__class__)
        new_instance.__init__()
        for key in keys:
            if key.startswith("_"): continue
            if self.__getattribute__(key) is not True:
                new_instance.__delattr__(key)
                continue
            new_instance.__setattr__(key, product.__getattribute__(key))
        
        return new_instance
    
    def __str__(self) -> str:
        features = vars(self)

        display_string = f""""""
        for key, value in features.items():
            display_string += f"""{key:<28}{value}\n"""

        return display_string

    def __getitem__(self, index:int):
        features = vars(self)
        try:
            key, value = list(features.items())[index]
        except IndexError:
            return None, None
        return key, value


class ComparisonTable:

    def __init__(self, table:list[list[DisplayPhone]]) -> None:
        self.table = table.copy()
        self._index = 0
        self.nrow = max([len(n) for n in table])
        self.ncol = len(self.table)

    def display(self, *header):
        print(f"{"":23}", end="")
        for text in header:
            print(f"{text:20}", end="")
        else:
            print(f"\n{"":23}", end="")
        for text in header:
            print(f"{"----------":<20}", end="")
        print("")

        for row in self:
            # List all features
            features_set:set[str] = set()
            for phone in row:
                for key in vars(phone).keys(): features_set.add(key)
            features = list(features_set)
            features.sort()

            # Set 'name' as first
            with suppress(ValueError):
                features.insert(0, features.pop(features.index("name")))
            
            # Print rows
            for feature in features:
                heading = " ".join(feature.split("_"))
                heading_lines = textwrap.wrap(heading, width=19)
                row_text = f"""{heading_lines[0]:<23}"""

                for phone in row:
                    feature_value = ""
                    with suppress(AttributeError):
                        feature_value = phone.__getattribute__(feature)
                        if isinstance(feature_value, float):
                            feature_value = round(feature_value, 2)

                    if feature == "name":
                        row_text += f"\033[1m{feature_value:<20}\033[0m"
                    else:
                        row_text += f"{feature_value:<20}"
                print(row_text)
                if len(heading_lines) > 1: print(" ".join(heading_lines[0:]))
            print("")

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self.nrow:
            item:list[DisplayPhone] = []
            for column in self.table:
                if self._index < len(column):
                    item.append(column[self._index])
                else:
                    item.append(DisplayPhone().empty())
            self._index += 1
            return item
        else:
            raise StopIteration

    def __getitem__(self, index:int):
        if index > self.ncol -1: raise IndexError("list index out of range")
        return self.table[index]


class Comparisons:

    def __init__(self, market: Market, round:int) -> None:
        self.market = market
        self.round = round

    def winners_across_segments(self):
        display = self._display_phone()

        comparison_table = self._compare(
            display, 
            self.market.price().high.profitable().high.products,
            self.market.price().mid.profitable().high.products,
            self.market.price().low.profitable().high.products,
        )
        print(f"\nWinners Across Segments (Round {self.round})")
        comparison_table.display("High Price", "Mid Price", "Low Price")

    def high_price_segment(self):
        display = self._display_phone()

        comparison_table = self._compare(
            display, 
            self.market.price().high.profitable().high.products,
            self.market.price().high.profitable().mid.products,
            self.market.price().high.profitable().low.products,
        )

        print(f"\nHigh Price Segment (Round {self.round})")
        comparison_table.display("High Profit", "Mid Profit", "Low Profit")

    def mid_price_segment(self):
        display = self._display_phone()

        comparison_table = self._compare(
            display, 
            self.market.price().mid.profitable().high.products,
            self.market.price().mid.profitable().mid.products,
            self.market.price().mid.profitable().low.products,
        )

        print(f"\nMid Price Segment (Round {self.round})")
        comparison_table.display("High Profit", "Mid Profit", "Low Profit")

    def low_price_segment(self):
        display = self._display_phone()

        comparison_table = self._compare(
            display, 
            self.market.price().low.profitable().high.products,
            self.market.price().low.profitable().mid.products,
            self.market.price().low.profitable().low.products,
        )

        print(f"\nLow Price Segment (Round {self.round})")
        comparison_table.display("High Profit", "Mid Profit", "Low Profit")

    def _display_phone(self) -> DisplayPhone:
            display = DisplayPhone()
            display.price = True
            display.profit = True
            display.total_sales = True
            display.margin = True
            display.margin_percent = True
            display.performance = True
            display.battery = True
            display.audience = True
            display.camera = True
            display.security = True
            display.memory = True
            display.total_awareness = True
            return display

    def _compare(self, phone:DisplayPhone, *args:list[Product]):
        comparison_table: list[list[DisplayPhone]] = []
        for products in args:
            comparison_table.append([])
            for product in products:
                comparison_table[-1].append(
                    phone(product)
                )
        if phone.profit:
            for column in comparison_table:
                column.sort(key=lambda p: p.profit)
                column.reverse()
                
        return ComparisonTable(comparison_table)