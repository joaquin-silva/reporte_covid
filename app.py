import streamlit as st
import pandas as pd
from reporte_diario import *

st.title('Reporte COVID-19 Chile')

data = obtener_datos()
df = obtener_resumen(data)

fecha_actual = data['Fecha'][data.shape[0]-1]
fecha_actual = fecha_actual.strftime('%d-%m-%Y')

st.header(f'Reporte {fecha_actual}')
st.table(df)

st.header('Visualizaciones')

option = st.selectbox(
     'Seleccione un dato',
     ('Casos nuevos totales', 'Fallecidos', 'Pacientes UCI'))

st.subheader(f'{option} por Semana')
pivot = datos_por_semana(data, option)
cmap = sns.color_palette("YlOrRd", as_cmap=True)
st.dataframe(pivot.style.background_gradient(cmap=cmap))

st.subheader(f'{option} por Fecha')
fig = grafico_casos(data, option)
st.pyplot(fig)
