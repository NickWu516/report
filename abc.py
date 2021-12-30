import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import  Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


START='2015-01-01'
TODAY=date.today().strftime('%Y-%m-%d')

st.title('股票預測')

stocks=('0056.tw','2412.tw')
selected_stocks=st.selectbox('選擇股票',stocks)

n_years=st.slider('年預測',1,4)
period=n_years*365

@st.cache
def load_data(ticker):
  data=yf.download(ticker,START,TODAY)
  data.reset_index(inplace=True)
  return data

data_load_state=st.text('數據載入中...')
data=load_data(selected_stock)
data_load_state.text('數據載入完畢')

st.subheader('原始數據')
st.write(data.tail())

def plot_raw_data():
  fig=go.Figure()
  fig.add_trace(go.Scatter(x=data['日期'],y=data['開盤價'],name='stock_open'))
  fig.add_trace(go.Scatter(x=data['日期'],y=data['收盤價'],name='stock_close'))
  fig.layout.update(title_text='時間序列資料',xaxis_rangeslider_visible=True)
  st.plotly_chart(fig)
  
plot_raw_data()

df_train=data[['日期','收盤']]
df_train=df_train.rename(columns={'日期':'ds','收盤':'y'})
m=Prophet()
m.fit(df_train)
future=m.male_future_dataframe(periods=period)
forecast=m.predict(future)

st.subheader('預測數據')
st.write(forecast.tail())

st.write('預測數據')
fig1=plot_plotly(m,forecast)
st.plotly_cart(fig1)

st.write('預測圖')
fig2=m.plot_components(forecast)
st.write(fig2)
