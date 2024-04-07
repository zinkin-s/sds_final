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

def calc_nominal_wage_index(df):
    nominal_wage = list(df['Всего по  экономике'])
    arr = []
    arr.append(2223 / 1523 * 100)

    for i in range(1, len(nominal_wage)):
        arr.append(nominal_wage[i]/nominal_wage[i-1]*100)
    
    return np.array(arr)

def calculate_cip_rate(df):
    cip = list(df['ИПЦ'])
    cip_rate = []
    t = 1
    for i in range(len(cip)):
        t = t*cip[i]/100
        cip_rate.append(t)
    
    return np.array(cip_rate) * 100


st.set_page_config(page_title="Всего по экономике", page_icon="📈")
st.sidebar.header('Всего по экономике')
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
data['ИНЗП % к пред.году'] = calc_nominal_wage_index(data)
data['ИРЗП % к пред. году'] = data['ИНЗП % к пред.году'] / data['ИПЦ'] * 100
data['ИПЦ % к базовому году'] = calculate_cip_rate(data)
data['ИРЗП % к базовому году'] = data['Всего по  экономике'] / data['ИПЦ % к базовому году']

st.markdown('### ИНЗП и ИРЗП в % к пред.году')
st.line_chart(data, y=['ИРЗП % к пред. году', 'ИНЗП % к пред.году'])
st.line_chart(data, y=['ИПЦ % к базовому году','ИРЗП % к базовому году'])