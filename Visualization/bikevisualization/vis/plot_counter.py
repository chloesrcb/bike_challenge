
import calendar
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import Image
from IPython import display

def plot_date(df):
    sns.set_theme(style="darkgrid")
    sns.relplot(x="date", y="intensity", kind="line", ci="sd", data=df)
    plt.xlabel('Date')
    plt.ylabel('Intensity of bike')
    plt.xticks(rotation=45)
    plt.title("Daily intensity of bike")
    plt.show()

def plot_week(df):
    counter_week = df.groupby("weekday")["intensity"]
    days = ['Lundi', 'Mardi', 'Mercredi',
        'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    counter_week.plot()
    plt.legend(labels=days, loc='lower left', bbox_to_anchor=(1, 0.1))
    plt.title("Intensity of bike by day of week")
    plt.xlabel('Date')
    plt.ylabel('Intensity of bike')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_month(df):
    months = ['Janvier', 'Fevrier', 'Mars', 'Avril',
              'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre',
              'Octobre', 'Novembre', 'Decembre']
    df['month'] = df.index.month
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    counter_month = df.groupby("month")["intensity"]
    counter_month.plot()
    plt.title("Monthly and daily intensity of bike")
    plt.xlabel('Date')
    plt.ylabel('Intensity of bike')
    plt.legend(labels=months, loc='lower left', bbox_to_anchor=(1, 0.1))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def histplot_counter(df):
    sns.histplot(data=df, y="intensity", hue="month", multiple="stack")
    plt.title("Histogram of intensity of bike by month")
    plt.xlabel('Count')
    plt.ylabel('Intensity of bike')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_counter(dict_counters, counter, option, animation):
    if animation :
        animatedGif = "./bikevisualization/images/bike_gif.gif" #path relative to your notebook
        file = open(animatedGif , "rb")
        image = file.read()
        progress= Image(
            value=image,
            format='gif')
        display.display(progress)
    elif option=="date" :
        plot_date(dict_counters[counter])
    elif option=="week" :
        plot_week(dict_counters[counter])
    elif option=="month" :
        plot_month(dict_counters[counter])
    elif option=="histogram" :
        histplot_counter(dict_counters[counter])
    



