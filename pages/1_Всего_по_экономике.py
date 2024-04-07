import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

def load_dataset(path):
    df = pd.read_csv(path)
    return df

def merge_datasets(df1, df2):
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def calculate_cpi(df):
    x = df['Темпы инфляции']
    return x + 100

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

def calculate_real_wage_rate(df):
    arr = []
    ys = list(df['ИРЗП % к пред. году'])
    t = 1
    for j in range(len(ys)):
        t = t * (ys[j]/100)
        arr.append(t)
    return np.array(arr) * 100




st.set_page_config(page_title="Всего по экономике", page_icon="📈")
st.sidebar.header('Всего по экономике')
st.title('Анализ заработных плат в Российской Федерации')

path_1 = 'data//sheet_1.csv'
sheet_1 = load_dataset(path_1)

path_2 = 'data//sheet_2.csv'
sheet_2 = load_dataset(path_2)
sheet_2 = sheet_2.rename(columns={'Всего': 'Всего по  экономике'})

data = merge_datasets(sheet_1[['Год', 'Всего по  экономике']], sheet_2[['Год', 'Всего по  экономике']])
idx = data['Год']

infl_path = 'data//inflation.csv'
inflation = pd.read_csv(infl_path)

data = data.rename(columns={'Год':'год'})
data = data.set_index(idx).sort_index()
inflation = inflation.set_index('Год').sort_index()

data['Темпы инфляции'] = inflation['Всего']
data['ИПЦ'] = calculate_cpi(data)
data['ИНЗП % к пред.году'] = calc_nominal_wage_index(data)
data['ИРЗП % к пред. году'] = data['ИНЗП % к пред.году'] / data['ИПЦ'] * 100
data['ИПЦ % к базовому году'] = calculate_cip_rate(data)
data['РЗП % к базовому году'] = data['Всего по  экономике'] / (data['ИПЦ % к базовому году'] / 100)
data['ИРЗП % к базовому году'] = calculate_real_wage_rate(data)

#data = data['год'].astype('datetime64[Y]')

st.markdown('### ИНЗП и ИРЗП в % к пред.году')
#st.line_chart(data,x='год', y=['ИРЗП % к пред. году', 'ИНЗП % к пред.году'])

#st.line_chart(data, y=['ИПЦ % к базовому году','ИРЗП % к базовому году'])


base = alt.Chart(data).encode(
    alt.X('год', 
    axis = alt.Axis(title=None))
)
real_wage = base.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white"),
    color='##57A44C'
).encode(
    alt.Y('РЗП % к базовому году',
    axis=alt.Axis(title='РЗП, руб', titleColor='#57A44C'))
)

nominal_wage = base.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white", color='red'),
    color='red'
).encode(
    alt.Y('Всего по  экономике',
    axis=alt.Axis(title='НЗП по экономике, руб.', titleColor='red'))
)



rwi = base.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white"),
).encode(
    alt.Y('ИРЗП % к базовому году',
    axis=alt.Axis(title='% к базовому (1999) году', titleColor='#57A44C'))
)

cpi = base.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white", color='red'),
    color='red'
).encode(
    alt.Y('ИПЦ % к базовому году',
    axis=alt.Axis(title='% к базовому (1999) году', titleColor='##5276A7'))
)


tab1, tab2 = st.tabs(['Реальная и номинальная заработная плата за период 2000-2023 гг.', 'ИРЗП и ИПЦ за период 2000-2023 гг. % к 1999 году'])

with tab1:
    chart = alt.layer(real_wage, nominal_wage).resolve_scale(
        y='independent',
    )
    st.altair_chart(chart, theme='streamlit', use_container_width=True)
with tab2:
    chart_2 = alt.layer(rwi, cpi)
    st.altair_chart(chart_2, theme='streamlit', use_container_width=True)

st.dataframe(data)
