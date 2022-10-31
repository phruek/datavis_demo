import streamlit as st 
import numpy as np
import pandas as pd
import datetime as dt
import altair as alt
import toolz
import geopandas as gpd
import re

st.header("Overview Performance")
st.write("Growth Year on Year comparison")

dfYOY = pd.read_csv('./Growth-Rate.csv')

dfYOYSeries = pd.DataFrame()
dfYOYMPP = dfYOY[['year-month','growth_rate_purchased_price']].copy()
dfYOYMPP.rename(columns={"growth_rate_purchased_price": "y"}, inplace=True)
dfYOYMPP['category'] = "A"
dfYOYMPP['x'] = [x for x in range(len(dfYOYMPP))]

dfYOYUB = dfYOY[['year-month','growth_rate_unique_basket']].copy()
dfYOYUB.rename(columns={"growth_rate_unique_basket": "y"}, inplace=True)
dfYOYUB['category'] = "B"
dfYOYUB['x'] = [x for x in range(len(dfYOYUB))]
dfYOYSeries = pd.concat([dfYOYMPP, dfYOYUB])

def growthRate():
    bar = alt.Chart(dfYOY).mark_bar(size=35).encode(
        x="year-month:T",
        y="growth_rate_purchased_price:Q",
        color=alt.condition(
            alt.datum.growth_rate_purchased_price > 0,
            alt.value("#2E9599"),  # The positive color
            alt.value("#2E9599")  # The negative color
        )
    ).properties(width=alt.Step(40))

    # ส้ม จำนวน Order
    line1 = alt.Chart(dfYOY).mark_line().encode(
        x='year-month:T',
        y='growth_rate_unique_basket:Q',
        color=alt.value('#F46C3F')
    )

    # ชมพู ยอดรวม
    line2 = alt.Chart(dfYOY).mark_line().encode(
        x='year-month:T',
        y='growth_rate_total:Q',
        color=alt.value("#A7226F")
    )

    chart = alt.layer(
        bar,line1,line2
    ).properties(
        width=1000, height=400
    )
    return chart
def map():
    dfpop = pd.read_csv('./proportion.csv',low_memory=False)
    dfpop['name'] = dfpop['Central_Province']
    dfpop.loc[dfpop['central_order_status']=='Completed']
    dfComplated = dfpop[dfpop['central_order_status']=='Completed'].groupby(['name'])['proportion'].mean()
    dfProcessing = dfpop[dfpop['central_order_status']=='Processing'].groupby(['name'])['proportion'].mean()
    dfFailed = dfpop[dfpop['central_order_status']=='Failed'].groupby(['name'])['proportion'].mean()
    dfReturned = dfpop[dfpop['central_order_status']=='Returned'].groupby(['name'])['proportion'].mean()
    alt.pipe = toolz.curried.pipe
    # dfmap = gpd.read_file('https://bit.ly/thaigeojson')
    dfmap = pd.read_csv('thaigeo.csv')
    dfmap['name'] = dfmap['name'].apply(lambda x: 'Nong Bua Lamphu' if x == 'Nong Bua Lam Phu' else x)
    dfplot = dfmap.merge(dfComplated, on='name', how='left', indicator=True)
    complatedChart = alt.Chart(dfplot).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['name','proportion']
    )
    dfplot = dfmap.merge(dfProcessing, on='name', how='left', indicator=True)
    processingChart = alt.Chart(dfplot).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['name','proportion']
    )
    dfplot = dfmap.merge(dfFailed, on='name', how='left', indicator=True)
    failedChart = alt.Chart(dfplot).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['name','proportion']
    )
    dfplot = dfmap.merge(dfReturned, on='name', how='left', indicator=True)
    returnChart = alt.Chart(dfplot).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['name','proportion']
    )
    return alt.hconcat(complatedChart, processingChart)

tab1, tab2, tab3, tab4 = st.tabs(['Growth Rate comparison', 'Coloplate Status Map','Coloplate total mean per order','Category Shares'])
with tab1:
    st.markdown("#### เปรียบเทียบค่าการเติบโตระหว่าง ยอดขายรวม, ยอดต่อบิล และ จำนวนคำสั่งซื้อ(order)")
    st.markdown("----- กราฟแท่ง การเติบโตของยอดรวมทั้งหมด")
    st.markdown("----- เส้นสีส้ม การเติบโตจำนวน Order")
    st.markdown("----- เส้นสีชมพู การเติบโตของยอดแต่ละ Order")
    st.altair_chart(growthRate())

with tab2:
    st.markdown("#### แสดงแผนที่ประเทศไทยในมุมมอง Failed Status")
    dfpop = pd.read_csv('./proportion.csv',low_memory=False)
    dfpop['name'] = dfpop['Central_Province']
    dfComplated = dfpop[dfpop['central_order_status']=='Completed'].groupby(['name'])['proportion'].mean()
    # dfProcessing = dfpop[dfpop['central_order_status']=='Processing'].groupby(['name'])['proportion'].mean()
    # dfFailed = dfpop[dfpop['central_order_status']=='Failed'].groupby(['name'])['proportion'].mean()
    # dfReturned = dfpop[dfpop['central_order_status']=='Returned'].groupby(['name'])['proportion'].mean()
    alt.pipe = toolz.curried.pipe
    dfmap = gpd.read_file('https://bit.ly/thaigeojson')
    
    # dfmap = pd.read_csv('thaigeo.csv')
    # dfmap['geometry'] = gpd.GeoSeries.from_wkt(dfmap['geometry'])
    # dfmap = gpd.GeoDataFrame(dfmap, geometry='geometry')
    dfmap['geometry'] = dfmap.geometry.apply(lambda x: x.wkt).apply(lambda x: re.sub('"(.*)"', '\\1', x))

    dfmap['name'] = dfmap['name'].apply(lambda x: 'Nong Bua Lamphu' if x == 'Nong Bua Lam Phu' else x)
    dfplot = dfmap.merge(dfComplated, on='name', how='left', indicator=True)
    # dfplot = dfplot[['geometry']].copy()
    
    complatedChart = alt.Chart(dfplot).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['name','proportion']
    ).properties(
        width=500,
        height=300
    )
    
    # dfplot = dfmap.merge(dfProcessing, on='name', how='left', indicator=True)
    # processingChart = alt.Chart(dfplot).mark_geoshape().encode(
    #     color='proportion:Q',
    #     tooltip=['name','proportion']
    # )
    # dfplot = dfmap.merge(dfFailed, on='name', how='left', indicator=True)
    # failedChart = alt.Chart(dfplot).mark_geoshape().encode(
    #     color='proportion:Q',
    #     tooltip=['name','proportion']
    # )
    # dfplot = dfmap.merge(dfReturned, on='name', how='left', indicator=True)
    # returnChart = alt.Chart(dfplot).mark_geoshape().encode(
    #     color='proportion:Q',
    #     tooltip=['name','proportion']
    # )
    # chartLine1 = alt.hconcat(complatedChart, processingChart)
    
    st.markdown("###### Order failed status 2020")
    st.image('./images/failed-proportion1.svg')
    st.markdown("###### Order failed status 2021")
    st.image('./images/failed-proportion2.svg')
    st.markdown("###### Order failed status 2022")
    st.image('./images/failed-proportion3.svg')
    st.altair_chart(complatedChart)
with tab3:
    # USA
    # from vega_datasets import data
    # counties = alt.topo_feature(data.us_10m.url, 'counties')
    # source = data.unemployment.url
    # chart = alt.Chart(counties).mark_geoshape().encode(
    #     color='rate:Q'
    # ).transform_lookup(
    #     lookup='id',
    #     from_=alt.LookupData(source, 'id', ['rate'])
    # ).project(
    #     type='albersUsa'
    # ).properties(
    #     width=500,
    #     height=300
    # )
    # st.altair_chart(chart)

    st.markdown("#### แสดงแผนที่ประเทศไทยในมุมมอง ค่าเฉลี่ยยอดขายต่อ Order")
    st.markdown("######  ค่าเฉลี่ยยอดขายต่อ Order 2020")
    st.image('./images/mean-total-order1.svg')
    st.markdown("###### ค่าเฉลี่ยยอดขายต่อ Order 2021")
    st.image('./images/mean-total-order2.svg')

    
    st.markdown("###### ค่าเฉลี่ยยอดขายต่อ Order 2022")
    st.image('./images/mean-total-order3.svg')
with tab4:
    st.header("Graph แสดงกลุ่มของ Category ที่มีผลต่อยอดรวมสินค้าต่อ Order และ ปริมาณ Order")
    dfCategoryShares = pd.read_csv('./CategoryShares.csv',low_memory=False)
    dfCategoryShares['StdSca_total_price_in_basket'] = (dfCategoryShares['total_price_in_basket']-dfCategoryShares['total_price_in_basket'].mean())/dfCategoryShares['total_price_in_basket'].std()
    dfCategoryShares['StdSca_number_of_unique_basket'] = (dfCategoryShares['number_of_unique_basket']-dfCategoryShares['number_of_unique_basket'].mean())/dfCategoryShares['number_of_unique_basket'].std()
    lineY = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y',color=alt.value('#FF0000'))
    lineX = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule().encode(x='x',color=alt.value('#FF0000'))
    chart = alt.Chart(dfCategoryShares).mark_circle(size=60).encode(
        x='StdSca_total_price_in_basket',
        y='StdSca_number_of_unique_basket',
        color='category_level_1',
        tooltip=['category_level_1', 'total_price_in_basket', 'number_of_unique_basket']
    ).properties(
        width=1000,
        height=800
    ).interactive()
    st.altair_chart(chart+lineY+lineX)

