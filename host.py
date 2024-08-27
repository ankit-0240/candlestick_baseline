import streamlit as st
import pandas as pd
import plotly.graph_objs as go



nifty50_df = pd.read_csv('nifty50_1y.csv')
niftybank_df = pd.read_csv('niftybank_1y.csv')


nifty50_df.columns = nifty50_df.columns.str.strip()
niftybank_df.columns = niftybank_df.columns.str.strip()


nifty50_df['Date'] = pd.to_datetime(nifty50_df['Date'])
niftybank_df['Date'] = pd.to_datetime(niftybank_df['Date'])

nifty50_df['Weekday'] = nifty50_df['Date'].dt.day_name()
niftybank_df['Weekday'] = niftybank_df['Date'].dt.day_name()


st.sidebar.title('Stock Analysis')
option = st.sidebar.selectbox(
    'Select the index',
    ('Nifty 50', 'Nifty Bank')
)


st.sidebar.title('Select Date')
start_date = st.sidebar.date_input('Start date', min(nifty50_df['Date'].min(), niftybank_df['Date'].min()))
end_date = st.sidebar.date_input('End date', max(nifty50_df['Date'].max(), niftybank_df['Date'].max()))


if option == 'Nifty 50':
    df = nifty50_df[(nifty50_df['Date'] >= pd.Timestamp(start_date)) & (nifty50_df['Date'] <= pd.Timestamp(end_date))]
else:
    df = niftybank_df[(niftybank_df['Date'] >= pd.Timestamp(start_date)) & (niftybank_df['Date'] <= pd.Timestamp(end_date))]


days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
selected_days = st.sidebar.multiselect('Select Days', days_order, default=days_order)


for day in selected_days:
    day_data = df[df['Weekday'] == day]

    baseline = [0] * len(day_data)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=day_data['Date'],
        open=day_data['Open'] - day_data['Open'],
        high=day_data['High'] - day_data['Open'],
        low=day_data['Low'] - day_data['Open'],
        close=day_data['Close'] - day_data['Open'],
        name=f'Candlestick ({day})',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    fig.add_trace(go.Scatter(
        x=day_data['Date'],
        y=baseline,
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Baseline'
    ))

    fig.update_layout(
        title=f'Candlestick Chart for {day} - {option}',
        xaxis_title='Date',
        yaxis_title=f'{day}',
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        yaxis=dict(showgrid=True, zeroline=True)
    )

    st.plotly_chart(fig)

st.sidebar.markdown("Created by [Ankit kumar]")


