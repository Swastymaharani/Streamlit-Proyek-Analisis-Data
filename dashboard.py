import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
day_csv = Path(__file__).resolve().parent / 'day.csv'
day_df = pd.read_csv(day_csv)
day_df.head()


# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'hum': 'humidity',
    'cnt': 'count'
}, inplace=True)

# Mengubah value kolom season
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

# Mengubah value kolom year
day_df['year'] = day_df['year'].map({
    0: '2011', 1: '2012'
})

# Mengubah value komlom month
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

# Mengubah value komlom holiday
day_df['holiday'] = day_df['holiday'].map({
    0: 'Non-Holiday', 1: 'National Holiday'
})

# Mengubah value kolom weekday
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})

# Mengubah value komlom workingday
day_df['workingday'] = day_df['workingday'].map({
    0: 'weekend', 1: 'Workingday'
})

# Mengubah value kolom weather_cond
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    })
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
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

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df


# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
 
with st.sidebar:
    st.image('https://s-light.tiket.photos/t/01E25EBZS3W0FY9GTG6C42E1SE/rsfit1600900gsm/eventThirdParty/2023/10/20/0cd35786-2c9a-4d36-870b-a5cf0828a39a-1697755366056-657fc6aadea5d624f479313157653bec.jpg')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Sharing Rental')

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

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index.to_numpy(),
    monthly_rent_df['count'].to_numpy(),
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)


# Membuat jumlah penyewaan berdasarkan cuaca
weather_df = day_df.groupby(by='weather_cond').agg({
    'count': ['max', 'min', 'mean', 'sum']
})

sum_count_per_condition = day_df.groupby('weather_cond')['count'].sum()
weather_dict = weather_df[('count', 'sum')].to_dict()

colors = ['#72BCD4' if weather_dict[cond] == sum_count_per_condition.max() else '#D3D3D3' for cond in weather_dict]

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=weather_df.index,
    y=weather_df[('count', 'sum')],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_df[('count', 'sum')]):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Weather Condition', fontsize=20)
ax.set_ylabel('Total Rentals', fontsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)

st.subheader('Weather based Rentals')
st.pyplot(fig)


# Membuat jumlah penyewaan berdasarkan kondisi musim
season_df = season_rent_df.groupby('season').agg({
    'count': ['max', 'min', 'mean', 'sum']
})

sum_count_per_season = season_rent_df.groupby('season')['count'].sum()
season_dict = sum_count_per_season.to_dict()

colors = ['#72BCD4' if season_dict[cond] == sum_count_per_season.max() else '#D3D3D3' for cond in season_dict]

st.subheader('Season based Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x=season_rent_df.index,
    y=season_rent_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(season_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Workingday, Holiday Rentals, and Weekday')

workingday_df = day_df.groupby(by='workingday').agg({
    'count': ['max', 'min', 'mean', 'sum']
})

sum_count_per_workingday = day_df.groupby('workingday')['count'].sum()
workingday_dict = workingday_df[('count', 'sum')].to_dict()

colors1 = ['#72BCD4' if workingday_dict[cond] == sum_count_per_workingday.max() else '#D3D3D3' for cond in workingday_dict]

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))
#Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
holiday_df = day_df.groupby(by='holiday').agg({
    'count': ['max', 'min', 'mean', 'sum']
})

sum_count_per_holiday = day_df.groupby('holiday')['count'].sum()
holiday_dict = holiday_df[('count', 'sum')].to_dict()

colors2 = ['#72BCD4' if holiday_dict[cond] == sum_count_per_holiday.max() else '#D3D3D3' for cond in holiday_dict]

sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=colors2,
    ax=axes[1])

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
weekday_df = day_df.groupby(by='weekday').agg({
    'count': ['max', 'min', 'mean', 'sum']
})

sum_count_per_weekday = day_df.groupby('weekday')['count'].sum()
weekday_dict = weekday_df[('count', 'sum')].to_dict()

colors3 = ['#72BCD4' if weekday_dict[cond] == sum_count_per_weekday.max() else '#D3D3D3' for cond in weekday_dict]

sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors3,
    ax=axes[2])

for index, row in enumerate(weekday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

# Tight layout to ensure the plots do not overlap
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Membuat plot scatter untuk 'temp', 'atemp', 'humidity', 'windspeed' vs 'count'
st.subheader('Correlation between count bike with tempt, atempt, humidity, and windspeed')
fig, axes = plt.subplots(1, 4, figsize=(14, 6))

# Scatter plot untuk 'temp' vs 'count'
sns.scatterplot(
    x='temp',
    y='count',
    data=main_df,
    alpha=0.5,
    ax=axes[0]
)
axes[0].set_title('Temperature vs Count')

# Scatter plot untuk 'atemp' vs 'count'
sns.scatterplot(
    x='atemp',
    y='count',
    data=main_df,
    alpha=0.5,
    ax=axes[1]
)
axes[1].set_title('Feels Like Temperature vs Count')

# Scatter plot untuk 'humidity' vs 'count'
sns.scatterplot(
    x='humidity',
    y='count',
    data=main_df,
    alpha=0.5,
    ax=axes[2]
)
axes[2].set_title('Humidity vs Count')

# Scatter plot untuk 'windspeed' vs 'count'
sns.scatterplot(
    x='windspeed',
    y='count',
    data=main_df,
    alpha=0.5,
    ax=axes[3]
)
axes[3].set_title('Windspeed vs Count')

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

st.caption('Copyright © Swasty Maha Rani 2024')