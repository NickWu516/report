import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.title('匯率')

st.sidebar.header('輸入選項')

currency_list=['AUD','USD','EUR']
base_price_unit=st.sidebar.selectbox('幣值',currency_list)
symbols_price_unit=st.sidebar.selectbox('轉換後',currency_list)

@st.cache
def load_data():
    url=''.join(['https://rate.bot.com.tw/xrt?Lang=zh-TW',base_price_unit,'&symbols=',symbols_price_unit]
    response = requests.get(url)
    data=response.json()
    base_currency=pd.DataFrame.from_dict(data['rates'].items())
    rates_df.columns=['converted_currency','price']
    conversion_date=pd.Series(data['date'],name='date')
    df=pd.concat([base_currency,rates_df,conversion_date],axis=1)
    return df
    
 df=load_data()
 
 st.header('匯率換算')
 st.write(df)
