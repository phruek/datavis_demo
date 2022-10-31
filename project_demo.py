# import dependencies packages
import streamlit as st 
import numpy as np
import pandas as pd
import datetime as dt
import altair as alt

####################################################
# dataset
# @st.cache()
# def import_df():
#     df = pd.read_csv('item_level.csv')
#     # add/edit the dataset
#     df = df[df['status'].isin(['COMPLETED','delivered'])]
#     df['year'] = df['year'].astype(str).apply(lambda x: x.replace('.0',''))
#     df['month'] = df['month'].astype(str).apply(lambda x: x.replace('.0','') if len(x)==4 else '0'+x.replace('.0',''))
#     df['ym'] = df['year']+'-'+df['month']
#     df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#     df['day_name'] = df['date'].dt.day_name()
#     df['%discount'] = 1-df['price_per_unit']/df['max_price_per_unit']
#     df['%discount_bin'] = ((((np.ceil(df['%discount']*10)-1)*10+1)).astype(str)+'-'+(np.ceil(df['%discount']*10)*10).astype(str)+'%')\
#         .apply(lambda x: x.replace('.0',''))
#     df['%discount_bin'] = df['%discount_bin'].apply(lambda x: x.replace('-9-0%','0% (Base)'))
#     df = df.drop(columns=['Unnamed: 0', 'trans_date', 'seller_name', 'status', 'province', 'brand_category_1', 'brand_category_2', 'brand_category_3'])
#     return df
# df = import_df()

@st.cache()
# def import_df():
#     df = pd.read_csv('df_item.csv')
#     df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#     return df
# df = import_df()
    
####################################################
# define df_chart function

# def df_cht(nsq_barcode, start_date = min(df['date']), end_date = max(df['date'])):
#     submask1 = df['nsq_barcode']==nsq_barcode if type(nsq_barcode)==str else df['nsq_barcode'].isin(nsq_barcode)
#     mask = submask1&(df['date']>=start_date)&(df['date']<=end_date)
#     df_chart = df[mask][['date', 'quantity', 'discounted_price', 'price_per_unit', 'max_price_per_unit', '%discount']].groupby(
#         ['date'], as_index=False).agg(
#             avg_discount = ('%discount', np.mean),
#             total_quantity = ('quantity', len),
#             avg_quantity = ('quantity', np.mean),
#             avg_price = ('price_per_unit', np.mean),
#             base_price = ('max_price_per_unit', np.mean),
#             total_sales = ('discounted_price', np.sum)
#             )
#     df_chart['%discount_bin'] = ((((np.ceil(df_chart['avg_discount']*10)-1)*10+1)).astype(str)\
#                                  +'-'+(np.ceil(df_chart['avg_discount']*10)*10).astype(str)+'%'
#                                 ).apply(lambda x: x.replace('.0',''))
#     df_chart['%discount_bin'] = df_chart['%discount_bin'].apply(lambda x: x.replace('-9-0%','0% (Base)'))
#     table = pd.DataFrame({'%discount_bin':['0% (Base)','1-10%','11-20%','21-30%','31-40%','41-50%','51-60%','61-70%','71-80%','81-90%','91-100%']})
#     df_chart = df_chart.merge(table, on='%discount_bin', how='right')
#     return df_chart

# def df_cht2(start_date = min(df['date']), end_date = max(df['date'])):
#     mask = (df['date']>=start_date)&(df['date']<=end_date)&(df['%discount_bin']!='nan-nan%')
#     df_chart = df[mask][['channel_id', 'quantity', '%discount_bin']]
#     df_chart = df_chart.groupby(['channel_id', '%discount_bin'], as_index=False).agg(
#                 avg_quantity = ('quantity', np.mean),
#                 total_quantity = ('quantity', len))
    
#     table1 = pd.DataFrame({'channel_id':'Shopee', 
#                            '%discount_bin':['0% (Base)','1-10%','11-20%','21-30%','31-40%','41-50%','51-60%','61-70%','71-80%','81-90%','91-100%']})
#     table2 = pd.DataFrame({'channel_id':'Lazada', 
#                            '%discount_bin':['0% (Base)','1-10%','11-20%','21-30%','31-40%','41-50%','51-60%','61-70%','71-80%','81-90%','91-100%']})
#     table = pd.concat([table1, table2])

#     df_chart = df_chart.merge(table, on=['channel_id','%discount_bin'], how='right')
#     return df_chart

# ####################################################
# # define chart function
# def chart1(chart_type, sel_item, start_date, end_date):
#     source = df_cht(nsq_barcode=sel_item, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
#     n_day = (source['date'].max()-source['date'].min()).days
#     view = 'total_quantity:Q' if chart_type=='Daily Quantity' else 'total_sales:Q'
#     view_title = 'total daily sale quantity (unit)' if view=='total_quantity:Q' else 'total daily sales (THB)'

#     base = alt.Chart(source).encode(
#                 x = alt.X('date:T', scale=alt.Scale(padding=20), 
#                           axis=alt.Axis(format='%Y-%m-%d %a', labelAngle=-90, grid=False)) #tickCount='week'
#             ).properties(width=700, height=400)

#     bar = base.mark_bar(size=500/n_day).encode(
#                 y = alt.Y(view, title=view_title),
#                 color = alt.Color('avg_discount:Q', 
#                                   scale=alt.Scale(scheme='spectral', domain=[1,0]),
#                                   legend=alt.Legend(title=['Average', '%Discount'], format='%')),
#                 tooltip = ['total_sales:Q',
#                            'total_quantity:Q',
#                            alt.Tooltip('date:T', format='%Y-%m-%d %a'), 
#                            alt.Tooltip('avg_discount:Q', format='.1%'),
#                            alt.Tooltip('avg_price:Q', format='.1f'),
#                            alt.Tooltip('base_price:Q', format='.1f')
#                           ])

#     text = base.mark_text(dy = -10).encode(
#                 y = view,
#                 text=view)
    
#     return (bar+text if n_day<=31 else bar)

# def chart2(chart_type, sel_item, start_date, end_date):
#     source = df_cht(nsq_barcode=sel_item, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
#     view = 'total_quantity:Q' if chart_type=='Daily Quantity' else 'total_sales:Q'
#     view_title = 'total daily sale quantity (unit)' if view=='total_quantity:Q' else 'total daily sales (THB)'
#     chart1 = alt.Chart(source).mark_circle().encode(
#             x = alt.X('avg_discount:Q', title='Average %discount', axis=alt.Axis(format='%')),
#             y = alt.Y(view, title=view_title),
#             tooltip = ['total_sales:Q',
#                        'total_quantity:Q',
#                        alt.Tooltip('avg_discount:Q', format='.1%'),
#                        alt.Tooltip('avg_price:Q', format='.1f'),
#                        alt.Tooltip('base_price:Q', format='.1f')])
    
#     view = 'mean(total_quantity):Q' if chart_type=='Daily Quantity' else 'mean(total_sales):Q'
#     view_title = 'Average daily sale quantity (unit)' if chart_type=='Daily Quantity' else 'Average daily sales (THB)'
#     source = source[['total_quantity', 'total_sales', '%discount_bin']].fillna(0)
#     chart2 = alt.Chart(source).mark_bar().encode(
#             x = alt.X(view, title=view_title),
#             y = alt.Y('%discount_bin:O', title='%discount range'),
#             tooltip = [alt.Tooltip('mean(total_quantity):Q', format='.1f'),
#                        alt.Tooltip('mean(total_sales):Q', format='.1f')])
    
#     return chart1.properties(width=350, height=300)|chart2.properties(width=150, height=300)

# def chart3(start_date, end_date):
#     source = df_cht2(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d')).fillna(0)
#     mask_shopee = (source['channel_id']=='Shopee')
#     mask_lazada = (source['channel_id']=='Lazada')
#     max_scale = source['avg_quantity'].max()+2
#     total_qty_shopee = str(sum(source[mask_shopee]['total_quantity']))
#     total_qty_lazada = str(sum(source[mask_lazada]['total_quantity']))

#     left = alt.Chart(source[mask_shopee]).mark_bar().encode(
#                 x = alt.X('avg_quantity:Q', 
#                           title='Average sale quantity',
#                           scale=alt.Scale(domain=[0,max_scale]),
#                           sort=alt.SortOrder('descending')),
#                 y = alt.Y('%discount_bin:O', axis=None),
#                 color = alt.Color('channel_id:N', legend=None),
#                 tooltip = ['total_quantity:Q', 
#                            alt.Tooltip('avg_quantity:Q', format='.1f'),
#                            '%discount_bin:O']
#             ).properties(title='SHOPEE (item count = '+total_qty_shopee+')', width=300, height=300)

#     middle = alt.Chart(source).mark_text().encode(
#                  y = alt.Y('%discount_bin:O', axis=None),
#                  text = alt.Text('%discount_bin:O')
#              ).properties(title=['%discount','range'], width=60, height=300)

#     right = alt.Chart(source[mask_lazada]).mark_bar().encode(
#                 x = alt.X('avg_quantity:Q', 
#                           title='Average sale quantity',
#                           scale=alt.Scale(domain=[0,max_scale])),
#                 y = alt.Y('%discount_bin:O', axis=None),
#                 color = alt.Color('channel_id:N', legend=None),
#                 tooltip = ['total_quantity:Q', 
#                            alt.Tooltip('avg_quantity:Q', format='.1f'),
#                            '%discount_bin:O']
#             ).properties(title='LAZADA (item count = '+total_qty_lazada+')', width=300, height=300)

#     return alt.hconcat(left, middle, right, spacing=0)

# ####################################################
# # display

# st.header("Hello Kiang 👏")
# st.write("This is the first project demo of data visualization. (Page 1)")

# tab1, tab2, tab3 = st.tabs(['tab1','tab2','source code'])
    
# with tab1:
#     with st.form("form1"):
#         sel_cht = st.radio("Select chart:", ['Daily Quantity', 'Daily Sales'], horizontal=True, label_visibility='hidden')

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             sel_item = st.text_input("Input nsq_barcode", "NEWST-00606")

#         with col2:
#             sel_startdate = st.date_input("Select start date 📅", dt.date(2021, 11, 1), 
#                                           min_value=dt.date(2020, 1, 1), max_value=dt.date(2022, 3, 31))
#         with col3:
#             sel_enddate = st.date_input("Select end date 📅", dt.date(2021, 12, 31), 
#                                           min_value=dt.date(2020, 1, 1), max_value=dt.date(2022, 3, 31))
#         st.write("* import only dataset for year 2021 due to some limitation.")
#         if st.form_submit_button('Show chart 📊'):
#             st.subheader("Show "+sel_cht+" and average %discount")
#             st.write("Item Name: "+df[df['nsq_barcode']==sel_item]['item_name'].unique()[0])
#             st.altair_chart(chart1(chart_type=sel_cht, sel_item=sel_item, start_date=sel_startdate, end_date=sel_enddate), 
#                             use_container_width=True)
#             st.markdown("##### Show scatterplot of "+sel_cht+" and average %discount")
#             st.write("Item Name: "+df[df['nsq_barcode']==sel_item]['item_name'].unique()[0])
#             st.altair_chart(chart2(chart_type=sel_cht, sel_item=sel_item, start_date=sel_startdate, end_date=sel_enddate))
#         else:
#             st.subheader("Show "+sel_cht+" and average %discount")
#             st.write("Item Name: "+df[df['nsq_barcode']==sel_item]['item_name'].unique()[0])
#             st.altair_chart(chart1(chart_type=sel_cht, sel_item=sel_item, start_date=sel_startdate, end_date=sel_enddate), 
#                             use_container_width=True)
#             st.markdown("##### Show scatterplot of "+sel_cht+" and average %discount")
#             st.write("Item Name: "+df[df['nsq_barcode']==sel_item]['item_name'].unique()[0])
#             st.altair_chart(chart2(chart_type=sel_cht, sel_item=sel_item, start_date=sel_startdate, end_date=sel_enddate))

# with tab2:
#     with st.form("form2"):
#         st.subheader("Show average sale quantity by %discount range")
#         col1, col2 = st.columns(2)
#         with col1:
#             sel_startdate2 = st.date_input("Select start date 📅", dt.date(2021, 11, 1), 
#                                           min_value=dt.date(2020, 1, 1), max_value=dt.date(2022, 3, 31))
#         with col2:
#             sel_enddate2 = st.date_input("Select end date 📅", dt.date(2021, 12, 31), 
#                                           min_value=dt.date(2020, 1, 1), max_value=dt.date(2022, 3, 31))
#         st.write("* import only dataset for year 2021 due to some limitation.")
#         if st.form_submit_button('Show chart 📊'):
#             st.altair_chart(chart3(start_date=sel_startdate2, end_date=sel_enddate2))
#         else:
#             st.altair_chart(chart3(start_date=sel_startdate2, end_date=sel_enddate2))
            
# with tab3:
#     code = open('project_demo.py', encoding="utf-8").readlines()
#     lines = ''
#     for line in code:
#         lines += line
#     st.code(lines, language='python')
