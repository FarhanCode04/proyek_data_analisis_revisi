import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour):
  hour_count_df =  hour.groupby(by="hour").agg({"total_count": ["sum"]})
  return hour_count_df

def count_by_day_df(day):
    day_df_count_2011 = day.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def sum_order (hour):
    sum_order_items_df = hour.groupby("hour").total_count.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day): 
    season_df = day.groupby(by="season").total_count.sum().reset_index() 
    return season_df

day = pd.read_csv("dashboard/day_cleaned.csv")
hour = pd.read_csv("dashboard/hour_cleaned.csv")

datetime_columns = ["dteday"]
day.sort_values(by="dteday", inplace=True)
day.reset_index(inplace=True)   

hour.sort_values(by="dteday", inplace=True)
hour.reset_index(inplace=True)

for column in datetime_columns:
    day[column] = pd.to_datetime(day[column])
    hour[column] = pd.to_datetime(hour[column])

min_date_days = day["dteday"].min()
max_date_days = day["dteday"].max()

min_date_hour = hour["dteday"].min()
max_date_hour = hour["dteday"].max()

with st.sidebar:

    
        
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = day[(day["dteday"] >= str(start_date)) & 
                       (day["dteday"] <= str(end_date))]

main_df_hour = hour[(hour["dteday"] >= str(start_date)) & 
                        (hour["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing Data Analysis')


st.subheader("Waktu penyewaan sepeda paling tinggi dan paling rendah dalam 1 hari")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 12))

sns.barplot(x="hour", y="total_count", data=sum_order_items_df.head(5), palette="coolwarm", hue ="hour", ax=ax[0])

ax[0].legend_.remove()  # Menghapus legend karena tidak diperlukan
ax[0].set_xlabel("Jam (PM)", fontsize=24)
ax[0].set_ylabel("Jumlah Penyewaan", fontsize=24)
ax[0].set_title("Jam dengan Penyewa Sepeda Terbanyak", loc="center", fontsize=26)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].set_ylim(0, sum_order_items_df["total_count"].max() * 1.1)  # Memberikan ruang di atas maksimum
 
sns.barplot(x="hour", y="total_count", data=sum_order_items_df.sort_values(by="hour", ascending=True).head(5), palette="YlGnBu", ax=ax[1])
ax[1].set_xlabel("Jam (AM)", fontsize=24)
ax[1].set_ylabel("Jumlah Penyewaan", fontsize=24)
ax[1].set_title("Jam dengan Penyewa Sepeda Terdikit", loc="center", fontsize=26)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)
ax[1].set_ylim(0, sum_order_items_df["total_count"].max() * 1.1)  # Memberikan ruang di atas maksimum
st.pyplot(fig)


st.subheader("Performa penjualan perusahaan dalam beberapa tahun terakhir")
# Pastikan kolom tanggal diformat dengan benar
day['dteday'] = pd.to_datetime(day['dteday'])

# Menghitung jumlah pelanggan maksimum per bulan
monthly_counts = day.groupby(day['dteday'].dt.to_period('M'))['total_count'].max()

# Membuat plot
fig, ax = plt.subplots(figsize=(24, 5))  # Menyesuaikan ukuran plot
ax.bar(monthly_counts.index.astype(str), monthly_counts.values, color="#90CAF9", width=0.6, label="Jumlah Maksimum")
ax.plot(monthly_counts.index.astype(str), monthly_counts.values, color="blue", marker="o", markersize=8, label="Trend")

# Menambahkan label
ax.set_xlabel('Bulan', fontsize=14)
ax.set_ylabel('Jumlah Pelanggan', fontsize=14)
ax.set_title('Jumlah Pelanggan Maksimum per Bulan pada Tahun 2012', fontsize=16)

# Menyesuaikan tampilan sumbu
ax.tick_params(axis='x', labelsize=12, rotation=45)
ax.tick_params(axis='y', labelsize=12)

# Menampilkan legenda
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)


st.subheader("Frekuensi peminjaman sepeda pada setiap musim")
season_counts = day.groupby("season", observed=False)["total_count"].sum()

# Warna untuk setiap musim
colors = ["#FFA07A", "#90CAF9", "#8FBC8F", "#D3D3D3"]

# Membuat pie chart
fig, ax = plt.subplots(figsize=(10, 10))
ax.pie(
    season_counts,  # Data jumlah
    labels=season_counts.index,  # Label untuk setiap musim
    autopct='%1.1f%%',  # Format persentase
    colors=colors,  # Warna berdasarkan musim
    startangle=90,  # Sudut awal
    textprops={'fontsize': 20}  # Ukuran font
)

# Menambahkan judul
ax.set_title("Distribusi Antar Musim", fontsize=25)

# Menampilkan plot di Streamlit
st.pyplot(fig)

