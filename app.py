import pandas as pd
import streamlit as st
import plotly.express as pt
import numpy as np

def load_dataset(path):
    df = pd.read_csv(path)
    return df

def merge_datasets(df1, df2):
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def calculate_cpi():
    return inflation['Всего'] + 100


st.title('Анализ заработных плат в Российской Федерации')

path_1 = 'data//sheet_1.csv'
sheet_1 = load_dataset(path_1)

path_2 = 'data//sheet_2.csv'
sheet_2 = load_dataset(path_2)
sheet_2 = sheet_2.rename(columns={'Всего': 'Всего по  экономике'})

data = merge_datasets(sheet_1[['Год', 'Всего по  экономике']], sheet_2[['Год', 'Всего по  экономике']])

infl_path = 'data//inflation.csv'
inflation = pd.read_csv(infl_path)
data = data.set_index('Год').sort_index()
inflation = inflation.set_index('Год').sort_index()
data['ИПЦ'] = calculate_cpi()

st.dataframe(data)