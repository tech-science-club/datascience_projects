import openmeteo_requests
import matplotlib.pyplot as plt
import requests_cache
import pandas as pd
from retry_requests import retry
import seaborn as sns

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
	"latitude": 55.7281,               # Denmark, Svinninge
	"longitude": 11.5409,              #
	#"latitude": 31.392222,            #
	#"longitude": 48.999722,           # Ukraine, Shpola
	"start_date": "2024-05-01",
	"end_date": "2024-09-01",
	"hourly": ["temperature_2m", "cloud_cover" ],
	"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum", "wind_speed_10m_max"],
	"timezone": "Europe/Berlin"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["cloud_cover"] = hourly_cloud_cover



hourly_dataframe = pd.DataFrame(data = hourly_data)

# Count the number of occurrences for each unique date
hourly_dataframe['date_only'] = hourly_dataframe['date'].dt.date

# Group by the extracted date and calculate the mean of each group
daily_averages = hourly_dataframe.groupby('date_only').mean().reset_index()

# Rename columns for clarity (optional)
daily_averages = daily_averages.rename(columns={
	'date_only': 'date',
	'cloud_cover': 'average_cloud_cover'
})

#-----------------------------------------------------------------------------------------------------
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
daily_rain_sum = daily.Variables(3).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max

daily_dataframe = pd.DataFrame(data = daily_data)

print(daily_dataframe.head(20))
#--------------> join 2 tables
daily_dataframe['date'] = daily_dataframe['date'].dt.date

join_tables = pd.merge(daily_dataframe, daily_averages[['date', 'average_cloud_cover']], on='date', how='left')

count_temp = 0
count_temp_min = 0
count_wind = 0
count_rain = 0
count_summer = 0
count_clouds = 0

for index, row in join_tables.iterrows():

	temp = row['temperature_2m_max']
	wind_speed = row['wind_speed_10m_max']
	rain = row['rain_sum']
	cloud_cover = row['average_cloud_cover']
	if cloud_cover < 25:
		count_clouds += 1
	if temp > 22.0:
		count_temp += 1
	if wind_speed < 25:
		count_wind += 1
	if rain < 5.0:
		count_rain += 1
	if temp > 22.0 and  wind_speed < 25 and  rain < 5.0 and cloud_cover < 25:
		count_summer+=1

print(f"Amount of warm days: {count_temp}")
print(f"with out wind: {count_wind}")
print(f"with out rain: {count_rain}")
print(f"with sunny weather, <25% clouds: {count_clouds}")
print(f"Coincidence of factors above, consider as summer: {count_summer}")
#--------------------------create plots---------------------------------------------

#matplotlib
#join_tables.plot('date', 'rain_sum', label='rain_sum', color='red')
#join_tables.plot('date', 'temperature_2m_max', linewidth=2, label='temp', color='blue')
#join_tables.plot('date', 'wind_speed_10m_max', linewidth=2, label='wind_speed_10m_max', color='green')
#join_tables.plot('date','average_cloud_cover', label='overcast stat distirbution % ', color='blue')
#sns.displot(join_tables, x="average_cloud_cover", binwidth=3, stat="density", color="skyblue", label="Overcast stat distib.")
#sns.displot(join_tables, x="wind_speed_10m_max", binwidth=2, stat="density", color="cyan", label="wind speed stat dist.")

#seaborn
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# First plot: Distribution of Cloud Cover
sns.histplot(join_tables, x="average_cloud_cover",  binwidth=2, color="blue", ax=axes[0, 0])
axes[0, 0].set_title("Average Overcast Distribution")
axes[0, 0].set_xlabel(" overcast (%)")
axes[0, 0].set_ylabel("Frequency")

# Second plot: Temperature vs. Cloud Cover
sns.lineplot(join_tables, x="date", y="temperature_2m_max", ax=axes[0, 1], color="red")
axes[0, 1].set_title("Max Temperature")
axes[0, 1].set_xlabel("Date")
axes[0, 1].set_ylabel("Temperature (°C)")

# Third plot: Wind Speed
sns.histplot(join_tables, x="wind_speed_10m_max",  binwidth=2, color="cyan", ax=axes[1, 0])
axes[1, 0].set_title("Wind Speed Distribution")
axes[1, 0].set_xlabel("Wind Speed (km/h)")
axes[1, 0].set_ylabel("Frequency")

# Fourth plot: rain
sns.lineplot(join_tables, x="date", y="rain_sum", ax=axes[1, 1], color="purple")
axes[1, 1].set_title("Precipitation")
axes[1, 1].set_xlabel("Date")
axes[1, 1].set_ylabel("Rain (mm)")

for ax in axes.flat:
	ax.set_xticklabels(ax.get_xticklabels(), rotation=20)# Adjust layout

plt.tight_layout()
fig.suptitle("Multiple Climate Metrics", fontsize=18)
plt.subplots_adjust(top=0.93)

# Add a global title for all plots
fig.suptitle("Climate Data Analysis", fontsize=16)
plt.subplots_adjust(top=0.9)  # Adjust the top to make space for the global title

plt.show()

