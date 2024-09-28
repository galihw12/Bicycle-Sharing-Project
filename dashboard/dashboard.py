import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Importing Data
hour_df = pd.read_csv("cleaned_hour.csv")

#by year
def create_by_year(hour_df):
    hour_by_year_df = hour_df.groupby(by='yr').agg({
          'casual': ['sum'],
          'registered': ['sum'],
          'total_count': ['sum']
          })
    return hour_by_year_df

#by season
def create_by_season(hour_df):
    hour_by_season_df = hour_df.groupby(by='season').agg({
          'casual': ['sum'],
          'registered': ['sum'],
          'total_count': ['sum']
          })
    return hour_by_season_df

#by hr
def create_by_hr(hour_df):
    hour_by_hr_df = hour_df.groupby(by='hr').agg({
          'casual': ['sum'],
          'registered': ['sum'],
          'total_count': ['sum']
          })
    return hour_by_hr_df

#Making FIlter Component
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    st.image("https://images.adsttc.com/media/images/5189/8106/b3fc/4b6e/2900/0020/large_jpg/taestall_st_paul_mn.jpg?1367965955")
    
    start_date, end_date = st.date_input(
        label='Time Interval',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

hour_by_year_df = create_by_year(main_df)
hour_by_season_df = create_by_season(main_df)
hour_by_hr_df = create_by_hr(main_df)

#header
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader ('by Muhamad Teguh Galih Pamenang')

#yearly Users
st.title('Yearly Users of Bike Sharing')

fig, ax = plt.subplots(figsize=(18, 10))

hour_by_year_df.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Yearly Casual Users, Registered Users, and Total Users of Bike Sharing', fontsize=30)
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Number of Users (in Millions)', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.legend(fontsize=20)

for bars in ax.containers:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, int(height),
                ha='center', va='bottom', fontsize=20)

ax.grid(axis='y')

st.pyplot(fig)

#seasonal Users
st.title('Seasonal Users of Bike Sharing')

fig, ax = plt.subplots(figsize=(18, 10))

hour_by_season_df.plot(kind='line', marker='o', ax=ax, markersize=16, linewidth=8)

ax.set_title('Seasonal Casual Users, Registered Users, and Total Users of Bike Sharing', fontsize=30)
ax.set_xlabel('Season', fontsize=20)
ax.set_ylabel('Number of Users (in Millions)', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.legend(fontsize=20)

for line in ax.lines:
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        ax.text(x, y, int(y), ha='center', va='bottom', fontsize=20)

ax.grid(axis='y')

st.pyplot(fig)

#hourly Users
st.title('Hourly Users of Bike Sharing')

fig, ax = plt.subplots(figsize=(18, 10))

hour_by_hr_df.plot(kind='line', marker='o', ax=ax, markersize=10, linewidth=3)

ax.set_title('Hourly Casual Users, Registered Users, and Total Users of Bike Sharing', fontsize=30)
ax.set_xlabel('Hour', fontsize=20)
ax.set_ylabel('Number of Users (in Millions)', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.legend(fontsize=20)
ax.set_xticks(range(0, 24))

ax.grid(True)

st.pyplot(fig)

#Bike Sharing Users Based on Type of Day
main_df['holiday_in_workingday'] = main_df['holiday'] & ~main_df['day_name'].isin(['Sat', 'Sun'])
main_df['weekend'] = main_df['day_name'].isin(['Sat', 'Sun'])

values = {
    'working day': main_df[main_df['workingday']]['total_count'].sum(),
    'weekend': main_df[main_df['weekend']]['total_count'].sum(),
    'holiday in workingday': main_df[main_df['holiday_in_workingday']]['total_count'].sum()
}

values_df = pd.DataFrame(list(values.items()), columns=['Category', 'Value'])

st.title('Bike Sharing Users Based on Type of Day')

plt.figure(figsize=(10, 8))
plt.pie(values_df['Value'], labels=values_df['Category'], autopct='%1.1f%%', textprops={'fontsize': 20})

plt.axis('equal')

plt.title('Bike Sharing Users Based on Type of Day', fontsize=25)

st.pyplot(plt)

#Correlation
st.title('Correlation Between Normalized Temperature, Normalized Humidity, and Normalized Windspeed with Number of Users')
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(13, 10))

sns.regplot(x=main_df['temp'], y=main_df['total_count'], ax=ax1, color='red')
ax1.set(title="Correlation Between Normalized Temperature and Number of Users")

sns.regplot(x=main_df['hum'], y=main_df['total_count'], ax=ax2, color='blue')
ax2.set(title="Correlation Between Normalized Humidity and Number of Users")

sns.regplot(x=main_df['windspeed'], y=main_df['total_count'], ax=ax3, color='green')
ax3.set(title="Correlation Between Normalized Windspeed and Number of Users")

plt.tight_layout()

st.pyplot(plt)


