import streamlit as st  
from transform import *

st.title('Mapão Sala do Futuro')
st.caption('Centralizador de notas')


file_path1 = 'Map_2C_1bi.xlsx'
sheet_name = 'Mapão'

file_path2 = 'Map_2C_2bi.xlsx'


df1 = data_frame(file_path1, sheet_name)
df2 = data_frame(file_path2, sheet_name)


st.dataframe(df1)
st.dataframe(df2)

