import matplotlib
from flask import Blueprint, render_template

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates

from controllers.UserManager import UserManager
from app import Dao

dashboard_view = Blueprint('dashboard_route', __name__, template_folder='/templates')

user_manager = UserManager(Dao)

job_offer_data = pd.read_csv("dane.csv")

@dashboard_view.route('/dashboard', methods=['POST', 'GET'])
@user_manager.user.login_required
def dashboard():
    get_plot()
    get_statistic_for_wroclaw()
    get_work_types()
    get_workplace_popularity()
    get_statistic_for_mid()
    get_statistic_for_php_js()

    return render_template('dashboard.html')


def get_plot():
    data = {
        'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)
    }
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('X label')
    plt.ylabel('Y label')
    plt.title('Wykres testowy')
    plt.savefig(os.path.join('static', 'plots', 'plot1.png'))


def get_statistic_for_wroclaw():
    wykres1 = job_offer_data
    filtered_data = wykres1.loc[wykres1['City'].str.contains('Wrocław', case=False)]
    selected_columns = ['City', 'Marker_icon']
    filtered_data = filtered_data[selected_columns]
    countsPositionType = wykres1['Marker_icon'].value_counts().reset_index().rename(columns={'count': 'Liczba'})

    plt.figure(figsize=(22, 6))
    bars = plt.bar(countsPositionType['Marker_icon'], countsPositionType['Liczba'])
    plt.xlabel('Typ stanowiska')
    plt.ylabel('Liczba')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    plt.title('Liczba poszczególnych typów stanowisk we Wrocławiu')
    plt.savefig(os.path.join('static', 'plots', 'plot2.png'))


def get_work_types():
    wykres2 = job_offer_data
    filteredDataWorkplaceType = wykres2.drop_duplicates(subset='Workplace_type')

    countsWorkplaceType = wykres2['Workplace_type'].value_counts()
    countsWorkplaceTypeForTable = countsWorkplaceType.reset_index().rename(columns={'count': 'Liczba'})

    plt.figure(figsize=(8, 8))
    plt.pie(countsWorkplaceType, labels=countsWorkplaceType.index, autopct='%1.1f%%')
    plt.title('Przedstawienie pracy na wszystkich stanowiskach z podziałem ze względu na model pracy')
    plt.savefig(os.path.join('static', 'plots', 'plot3.png'))


def get_workplace_popularity():
    wykres3 = job_offer_data
    selected_countries = ['DE', 'GB', 'PL', 'FR', 'GB', 'CZ']
    results = pd.DataFrame()
    for country in selected_countries:
        result = findMinMaxMarkers(wykres3, country)
        results = pd.concat([results, result], ignore_index=True)

    countries = results['Country_code']
    minValues = results['Minimum']
    maxValues = results['Maksimum']
    minMarkers = results['Marker_icon_min']
    maxMarkers = results['Marker_icon_max']

    x = np.arange(len(countries))
    width = 0.4
    fig, ax = plt.subplots(figsize=(16, 9.5))
    rects1 = ax.bar(x - width / 2, minValues, width, label='Minimum', color='blue')
    rects2 = ax.bar(x + width / 2, maxValues, width, label='Maksimum', color='red')
    ax.set_xticks(x)
    ax.set_xticklabels(countries)
    ax.tick_params(axis='x', which='both', labeltop=False, labelbottom=True, pad=20)
    for i, (rect1, rect2, height1, height2) in enumerate(zip(rects1, rects2, minValues, maxValues)):
        ax.annotate(f'{minMarkers[i]}', xy=(rect1.get_x() + rect1.get_width() / 2, rect1.get_y()),
                    xytext=(0, -15), textcoords="offset points",
                    ha='center', va='bottom')
        ax.annotate(f'{maxMarkers[i]}', xy=(rect2.get_x() + rect2.get_width() / 2, rect2.get_y()),
                    xytext=(0, -15), textcoords="offset points",
                    ha='center', va='bottom')
    for rect1, rect2, height1, height2 in zip(rects1, rects2, minValues, maxValues):
        ax.annotate(height1, xy=(rect1.get_x() + rect1.get_width() / 2, height1),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')
        ax.annotate(height2, xy=(rect2.get_x() + rect2.get_width() / 2, height2),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')
    ax.legend()
    plt.xlabel('Najczęstrze i najrzadsze typy stanowisk w danym kraju')
    plt.ylabel('Liczba')
    plt.title('Najbardziej i najmniej popularne typy stanowisk w wybranych krajach europejskich')
    plt.savefig(os.path.join('static', 'plots', 'plot4.png'))


def findMinMaxMarkers(data, countryCode):
    filteredDataJobType = data[data['Country_code'] == countryCode]
    counts = filteredDataJobType['Marker_icon'].value_counts()
    minValue = counts.min()
    maxValue = counts.max()
    minIcon = counts[counts == minValue].index[0]
    maxIcon = counts[counts == maxValue].index[0]
    result = pd.DataFrame(
        {'Country_code': countryCode, 'Minimum': minValue, 'Marker_icon_min': minIcon, 'Maksimum': maxValue,
         'Marker_icon_max': maxIcon}, index=[0])
    return result


def get_statistic_for_mid():
    wykres4 = job_offer_data
    filteredDataDate = wykres4[
        (wykres4['Open_to_hire_Ukrainians'] == True) & (wykres4['Published_at'] > '2022-10-26T14:00:00.000Z') & (
                wykres4['Experience_level'] == 'mid')]
    counts = filteredDataDate['City'].value_counts()
    countsForTable = counts.reset_index().rename(columns={'count': 'Liczba'})

    suma = countsForTable.loc[countsForTable['Liczba'] == 1, 'Liczba'].sum()
    countsForTable = countsForTable[countsForTable['Liczba'] != 1]
    countsForTable.loc[len(countsForTable)] = ['Other', suma]

    liczba = countsForTable['Liczba']
    plt.figure(figsize=(18, 6))
    plt.grid()
    plt.scatter(range(len(countsForTable)), liczba)
    plt.xticks(range(len(countsForTable)), countsForTable['City'])
    plt.xlabel('Nazwa miasta')
    plt.ylabel('Liczba')
    plt.title(
        'Miejsca, które wystawiły swoją ofertę po 26 października 2022, gdzie zatrunia się ludzi ze średnim poziomem doświadczenia, w tym Ukraińców')
    plt.savefig(os.path.join('static', 'plots', 'plot5.png'))


def get_statistic_for_php_js():
    wykres5 = job_offer_data
    filteredDataPHPJavaScript = wykres5[
        (wykres5['skills_name_0'] == 'PHP') & (wykres5['skills_name_1'] == 'JavaScript') |
        (wykres5['skills_name_1'] == 'PHP') & (wykres5['skills_name_2'] == 'JavaScript') |
        (wykres5['skills_name_0'] == 'PHP') & (wykres5['skills_name_2'] == 'JavaScript')]

    fig, ax = plt.subplots(figsize=(13, 6))
    filteredDataPHPJavaScript.loc[:, 'Published_at'] = pd.to_datetime(filteredDataPHPJavaScript['Published_at'])
    filteredDataPHPJavaScript = filteredDataPHPJavaScript.sort_values('Published_at')
    for city in filteredDataPHPJavaScript['City'].unique():
        cityData = filteredDataPHPJavaScript[filteredDataPHPJavaScript['City'] == city]
        ax.scatter(cityData['Marker_icon'], cityData['Published_at'], label=city)
    ax.grid()
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1))
    ax.set_title(
        'Stanowiska, które w wymienionych umiejętnościach mają PHP i JavaScript, z podziałem na typ stanowiska i datę publikacji')
    ax.set_xlabel('Typ stanowiska')
    ax.set_ylabel('Data publikacji')
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.savefig(os.path.join('static', 'plots', 'plot6.png'))
