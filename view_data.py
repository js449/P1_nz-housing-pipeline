import streamlit as st
import pandas as pd

st.title("NZ Housing Data Viewer")
df = pd.read_csv('tmp/housing_data_silver.csv')
st.dataframe(df) # Renders an interactive table in browser