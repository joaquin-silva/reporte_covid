import streamlit as st
import pandas as pd
from reporte_diario import *

st.title('Reporte COVID-19 Chile')


data = obtener_casos_nuevos_totales()

casos_nuevos = "{:,d}".format(int(data['Casos nuevos totales'][data.shape[0]-1])).replace(",",".")
fallecidos_nuevos = "{:,d}".format(int(data['Fallecidos'][data.shape[0]-1])).replace(",",".")
fecha_actual = data['Fecha'][data.shape[0]-1]
fecha_actual = fecha_actual.strftime('%d-%m-%Y')

st.header('Datos Reporte')

st.markdown(f"""
    A la fecha {fecha_actual} se reportan:
    * Nuevos casos: {casos_nuevos}
    * Fallecidos: {fallecidos_nuevos}
""")

st.header('Casos Nuevos por Semana')
pivot = datos_por_semana(data, "Casos nuevos totales")
cmap = sns.color_palette("YlOrRd", as_cmap=True)
st.dataframe(pivot.style.background_gradient(cmap=cmap))

st.header('Fallecidos Nuevos por Semana')
pivot = datos_por_semana(data, "Fallecidos")
cmap = sns.color_palette("YlOrRd", as_cmap=True)
st.dataframe(pivot.style.background_gradient(cmap=cmap))

st.header('Gráfico Casos Nuevos')

fig = grafico_casos(data)
st.pyplot(fig)
