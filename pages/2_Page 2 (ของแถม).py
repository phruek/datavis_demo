# import dependencies packages
import streamlit as st 
import numpy as np
import pandas as pd
import datetime as dt
import altair as alt

####################################################
# dataset
# df_order = pd.read_csv('order_level.csv')
# df_order.loc[df_order['giveaway_item']=='[nan]',['has_giveaway']] = 'No'
# df_order.loc[df_order['giveaway_item']=='[nan]',['giveaway_item']] = np.nan
# df_order = df_order[df_order['status'].isin(['COMPLETED','delivered'])]
# df_order['year'] = df_order['year'].astype(str).apply(lambda x: x.replace('.0',''))
# df_order['month'] = df_order['month'].astype(str).apply(lambda x: x.replace('.0','') if len(x)==4 else '0'+x.replace('.0',''))
# df_order['ym'] = df_order['year']+'-'+df_order['month']

df_order = pd.read_csv('df_order.csv')

####################################################
# define df chart function
df_sel = df_order.groupby(['channel_id','ym', 'year','month','has_giveaway'], as_index=False).agg(
    total = ('purchased_price', sum), 
    avg = ('purchased_price', np.mean),
    n = ('purchased_price', len))

####################################################
# define chart function
lazada = (df_sel['channel_id']=='Lazada')
shopee = (df_sel['channel_id']=='Shopee')
rm2020 = ~(df_sel['year']=='2020')

def chart():
    fig1 = alt.Chart(df_sel[lazada&rm2020]).mark_line(point=True).encode(
        x='ym:O',
        y='avg:Q',
        color='has_giveaway'
    ).properties(title='LAZADA', width=600, height=200)

    fig2 = alt.Chart(df_sel[shopee&rm2020]).mark_line(point=True).encode(
        x='ym:O',
        y='avg:Q',
        color='has_giveaway'
    ).properties(title='SHOPEE', width=600, height=200)

    return (fig1 & fig2)

####################################################
# display

st.header("Hello Kiang 👏")
st.write("This is the first project demo of data visualization. (Page 2)")

tab1, tab2 = st.tabs(['tab1', 'source code'])

with tab1:
    st.markdown("##### เปรียบเทียบค่าเฉลี่ยของ order price ระหว่าง มีของแถม กับ ไม่มีของแถม")
    st.altair_chart(chart())
    
with tab2:
    code = open('pages/2_Page 2 (ของแถม).py', encoding="utf-8").readlines()
    lines = ''
    for line in code:
        lines += line
    st.code(lines, language='python')