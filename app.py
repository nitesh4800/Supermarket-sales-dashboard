import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Supermarket Sales Analysis",
                   page_icon=":bar_chart:",
                   layout="wide"
)

@st.cache_data
def get_data_from_excel():
    df=pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000
    )
    df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df

df=get_data_from_excel()

#st.dataframe(df)

# ------sidebar--------------
st.sidebar.header("Please Filter Here:")
city=st.sidebar.multiselect(
    "Select the city:",
    options=df['City'].unique(),
    default=df['City'].unique()
)
customer_type=st.sidebar.multiselect(
    "Select the customer type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)
gender=st.sidebar.multiselect(
    "Select the gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection=df.query(
    "City==@city & Customer_type==@customer_type & Gender==@gender"
)
#st.dataframe(df_selection)
#-----title of main page--------
st.title(":bar_chart: Supermarket Sales Analysis")
st.markdown("##")

#-----KPIs-------------------
total_sales=int(df_selection['Total'].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:"*int(round(average_rating,0))
average_sales=round(df_selection["Total"].mean(),2)

left_column, middle_column ,right_column=st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales per transaction:")
    st.subheader(f"US $ {average_sales}")

st.markdown("---")


#----charts-----
#---------sales per category------------
df_selection["Total"]=df_selection["Total"].astype("int64")
sales_by_prod_category=(
    df_selection.groupby('Product line')['Total'].sum().sort_values(ascending=False)
)
fig_prod_sales=px.bar(
    sales_by_prod_category,
    x='Total',
    y=sales_by_prod_category.index,
    orientation="h",
    title="<b>Sales by product category</b>",
    color_discrete_sequence=["#1D5D9B"]*len(sales_by_prod_category),
    template="plotly_white"
)
fig_prod_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#-------sales by hour----------------
sales_by_hour=df_selection.groupby('hour')['Total'].sum()
fig_hourly_sales=px.line(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#1D5D9B"]*len(sales_by_hour),

)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column.plotly_chart(fig_prod_sales,use_container_width=True)

st.markdown("---")

#--------payment method pie chart-------------------

payment_method=df_selection.groupby('Payment')['Payment'].count()

fig_payment_method=px.pie(
    payment_method,
    names=payment_method.index,
    values='Payment',
    hole=0.5,
    title="<b>Payment method distribution</b>"
)

#--------------Rating of various product categories-------------
#--------dataframe------------

rating_by_category=df_selection.groupby('Product line')['Rating'].mean()

#-------------chart------------

fig_rating_by_category=px.bar(
    rating_by_category,
    x=rating_by_category.index,
    y='Rating',
    title="<b>Rating by product category</b>",
    color_discrete_sequence=["#1D5D9B"]*len(sales_by_prod_category),
    template="plotly_white"
)
fig_rating_by_category.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)

left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_rating_by_category,use_container_width=True)
right_column.plotly_chart(fig_payment_method,use_container_width=True)

st.markdown("---")

st.dataframe(df_selection)