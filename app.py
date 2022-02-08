import streamlit as st
import pandas as pd
from reporte_diario import *

cmap = sns.color_palette("YlOrRd", as_cmap=True)

st.title('COVID-19 Chile')

data = obtener_datos()
df = obtener_resumen(data)

fecha_actual = data['Fecha'][data.shape[0]-1]
fecha_actual = fecha_actual.strftime('%d-%m-%Y')

st.header(f'Reporte {fecha_actual}')
st.table(
     df.style.background_gradient(cmap=cmap, subset=["Variación 7 días","Variación Media Móvil"]).format(
          {"Valor Reportado":"{:,d}",
          "Media Móvil":"{:,d}",
          "Variación 7 días":"{:.1%}",
          "Variación Media Móvil":"{:.1%}"})
     )

st.header('Visualizaciones')

option = st.selectbox(
     'Seleccione un dato',
     ('Casos nuevos totales', 'Fallecidos', 'Pacientes UCI'))

st.subheader(f'{option} por Semana')
pivot = datos_por_semana(data, option)
st.table(pivot.style.background_gradient(cmap=cmap).format("{:,d}"))
st.subheader(f'{option} por Fecha')
fig = grafico_casos(data, option)
st.pyplot(fig)
