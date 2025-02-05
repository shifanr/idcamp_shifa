import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import utils.helpers as helpers
import os
print("Current working directory:", os.getcwd())

sns.set(style='dark')

# st.title("Dasbor Interaktif")
# st.write("Selamat datang di dashboard interaktif!")

# memuat data csv
all_df = pd.read_csv("dashboard/all_data.csv")

# preprocessing data
datetime_columns = ["order_date", "order_delivered_customer_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)

# konversi kolom datetime
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# mendapatkan rentang tanggal
min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

# menambahkan widget sidebar
with st.sidebar:
    # menambahkan logo perusahaan
    st.image("dashboard/Ss.png")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# filter data berdasarkan rentang tanggal
main_df = all_df[(all_df["order_date"] >= str(start_date)) &

                 (all_df["order_date"] <= str(end_date))]

# memanggil helpers
daily_orders_df = helpers.create_daily_orders_df(main_df)
sum_order_items_df = helpers.create_sum_order_items_df(main_df)
bystatus_df = helpers.create_bystatus_df(main_df)
bystate_df = helpers.create_bystate_df(main_df)
rfm_df = helpers.create_rfm_df(main_df)

st.header('E-commerce Public Dataset Dashboard :sparkles:')

# informasi daily orders
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(
        daily_orders_df.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# informasi performa penjualan dari setiap produk
st.subheader("Best & Worts Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="quantity", y="product_category_name",
            data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="quantity", y="product_category_name", data=sum_order_items_df.sort_values(
    by="quantity", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)


# # info transaksi pelanggan
# st.subheader("Customer Transtions")

# fig, ax = plt.subplots(figsize=(20, 10))

# sns.barplot(
#     x="customer_count",
#     y="order_status",
#     data=bystatus_df.sort_values(by="customer_count", ascending=False),
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by Status", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
# st.pyplot(fig)


# info wilayah
st.subheader("Customer Demographics")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3",
          "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by State", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# info parameter RFM (Recency, Frequency, & Monetary)
st.subheader("Best CUstomer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(
        rfm_df.monetary.mean(), "AUD", locale='es_CO')
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(
    by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', rotation=45, labelsize=15)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(
    by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', rotation=45, labelsize=15)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(
    by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_ylabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', rotation=45, labelsize=15)


st.pyplot(fig)

st.caption('Copyright (c) Shifa 2024')
