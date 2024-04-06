import pandas as pd
import streamlit as st
import plotly.express as pt

def load_dataset(path):
    df = pd.read_csv(path)
    return df

st.title('Анализ заработных плат в Российской Федерации')

path = 'data//sheet_1.csv'
data = load_dataset(path)
st.dataframe(data)