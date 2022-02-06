import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def help(series):
    return np.append(series[0], [series[i]-series[i-1] for i in range(1, len(series))])

def obtener_casos_nuevos_totales():
    df = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_T.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df[["Fecha", "Casos nuevos totales","Fallecidos"]]
    df["Año"] = df["Fecha"].apply(lambda x: x.isocalendar()[0])
    df["Semana"] = df["Fecha"].apply(lambda x: x.isocalendar()[1])
    df["Número día"] = df["Fecha"].apply(lambda x: x.weekday())
    series = df["Fallecidos"]
    df["Fallecidos"] = help(df['Fallecidos']).astype(int)
    df['Casos nuevos totales media móvil'] = df['Casos nuevos totales'].rolling(7).mean()
    return df

def grafico_casos(df_totales, column):
    # Datoss
    data = df_totales[-28:]
    # Figura
    sns.set_style('darkgrid')
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(data['Fecha'], data[f'{column} media móvil'], color='red', label='Media móvil 7 días')
    ax.bar(data['Fecha'], data[column], label=column)
    # Formato
    format = mdates.DateFormatter("%d-%m-%Y")
    ax.xaxis.set_major_formatter(format)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x).replace(",",".") for x in current_values])
    # Títulos
    plt.title(f'{column} COVID-19')
    plt.xlabel('Fecha')
    plt.ylabel(column)
    plt.legend()
    return fig

def datos_por_semana(data, column):
    pivot = pd.pivot(data, index=["Año","Semana"], columns="Número día", values=column)
    pivot = pivot.loc[pivot.index[-5:],]
    pivot.columns = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    pivot = pivot.fillna(0)
    pivot = pivot.astype(int)
    return pivot
