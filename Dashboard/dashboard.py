import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv('Dashboard/cleaned_day_data.csv')
hour = pd.read_csv('Dashboard/hour.csv')
day_df.head()

day_df.rename(columns={
    'cnt': 'count'
}, inplace=True)

# menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df= df.groupby(by='dateday').agg({
        'count':'sum'
    }).reset_index()
    return daily_rent_df

# menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual':'sum'
        }).reset_index()
    return daily_casual_rent_df

# menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df=df.groupby(by='dateday').agg({
        'registered':'sum'
    }).reset_index()
    return daily_registered_rent_df

# menyiapkan season_rent_df

def create_season_rent_df(df):
    season_rent_df=df.groupby(by='season')[['registered','casual']].sum().reset_index()
    return season_rent_df

# menyiapkan monthly_rent_df

def create_monthy_rent_df(df):
    monthly_rent_df= df.groupby(by='month').agg({
        'count' : 'sum'
    })
    ordered_months= [
        'jan','feb','mar','apr','may',
        'jun','jul','jul','aug','sep',
        'oct','nov','dec'
    ]
    monthly_rent_df=monthly_rent_df.reindex(ordered_months,fill_value=0)
    return monthly_rent_df

# menyiapkan working_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
        }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# menyipakan  holiday
def create_holiday_rent_df(df):
    holiday_rent_df=df.groupby(by='holiday').agg({
        'count':'sum'
    }).reset_index()
    return holiday_rent_df

# menyiapkan weater_rent_df

def create_weather_rent_df(df):
    holiday_rent_df=df.groupby(by='weathersit').agg({
        'count':'sum'
    })
    return holiday_rent_df

min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    st.image('Dashboard/images.png')
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

main_hr_df = hour[(hour['dteday'] >= str(start_date)) & 
                (hour['dteday'] <= str(end_date))]

# menyiapkan dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthy_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Membuat judul
st.header('Bike Rental Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)


# 1. Visualisasi Penyewaan Berdasarkan Jam
plt.figure(figsize=(12, 5))
sns.lineplot(x=hour['hr'], y=hour['cnt'], marker="o", linewidth=2)
plt.title("Jumlah Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
plt.xlabel("Jam dalam Sehari", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
plt.xticks(range(0, 24))
st.pyplot(plt)

# 2. Visualisasi Penyewaan Berdasarkan Hari
plt.figure(figsize=(8, 5))
sns.barplot(x=main_df['weekday'], y=main_df['count'], hue=main_df['weekday'], palette="viridis", legend=False)
plt.title("Jumlah Penyewaan Sepeda Berdasarkan Hari", fontsize=14)
plt.xlabel("Hari dalam Seminggu (0=Minggu, 6=Sabtu)", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
plt.xticks(ticks=range(7), labels=['Min','Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'])
st.pyplot(plt)

# 3. Visualisasi Penyewaan Berdasarkan Bulan
plt.figure(figsize=(10, 6))
sns.barplot(x=main_df['month'], y=main_df['count'], hue=main_df['month'], palette="magma", legend=False)
plt.title("Jumlah Penyewaan Sepeda Berdasarkan Bulan", fontsize=14)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(plt)

usage_by_season = main_df.groupby('season')['count'].mean()

plt.figure(figsize=(8, 6))
usage_by_season.plot(kind='bar', color='lightcoral')
plt.title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
plt.ylabel('Rata-rata Jumlah Sepeda yang Disewa')
plt.xlabel('Musim')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(plt)
