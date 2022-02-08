import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def help(series):
    return np.append(series[0], [series[i]-series[i-1] for i in range(1, len(series))])

def obtener_tipo_pacientes():
    df = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario_T.csv")
    df = df.rename(columns={"Tipo de cama":"Fecha", "UCI":"Pacientes UCI"})
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df

def obtener_casos_nuevos_totales():
    df = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_T.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df[["Fecha", "Casos nuevos totales","Fallecidos"]]
    df["Año"] = df["Fecha"].apply(lambda x: x.isocalendar()[0])
    df["Semana"] = df["Fecha"].apply(lambda x: x.isocalendar()[1])
    df["Número día"] = df["Fecha"].apply(lambda x: x.weekday())
    df["Fallecidos"] = help(df['Fallecidos']).astype(int)
    return df

def obtener_datos():
    df_casos = obtener_casos_nuevos_totales()
    df_pacientes = obtener_tipo_pacientes()
    df = df_casos.join(df_pacientes.set_index("Fecha"), on="Fecha")

    for column in ["Casos nuevos totales", "Fallecidos", "Pacientes UCI"]:
        df[column + " media móvil"] = df[column].rolling(7).mean()

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

def obtener_dato(data, column, pos):
    return int(data[column][pos])
    # return "{:,d}".format(int(data[column][pos])).replace(",",".")

def obtener_variacion(nuevo, original):
    variacion = float(nuevo)/float(original) - 1
    return variacion
    # return "{:.1%}".format(variacion)

def obtener_fila(column, data):
    valor = obtener_dato(data, column, data.shape[0]-1)
    media_movil = obtener_dato(data, column + " media móvil", data.shape[0]-1)
    variacion_7dias = obtener_variacion(valor, obtener_dato(data, column, data.shape[0]-8))
    variacion_7dias_mm = obtener_variacion(media_movil, obtener_dato(data, column + " media móvil", data.shape[0]-8))
    return [column, valor, media_movil, variacion_7dias, variacion_7dias_mm]

def obtener_resumen(data):
    df = pd.DataFrame(columns=["Dato","Valor Reportado","Media Móvil","Variación 7 días","Variación Media Móvil"])
    df.loc[0] = obtener_fila('Casos nuevos totales', data)
    df.loc[1] = obtener_fila('Fallecidos', data)
    df.loc[2] = obtener_fila('Pacientes UCI', data)
    return df
