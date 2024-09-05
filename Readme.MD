Processing open data API.

1. Processing Weather Data in Denmark and Comparison with Ukraine: 
The script weather_history.py retrieves historical weather data from the API provided by the "Open-Meteo" service, 
which offers historical weather data. The script processes this data to calculate the number of sunny days, rainy days, 
and other weather conditions. It also builds several plots: two plots show the distribution of overcast conditions 
and wind, while two line plots display temperature and precipitation data.

![Optional Text](../master/Figure_1.png)

2. Processing Open Data of StoreBelt Traffic from 1998 to the Present: 
The script storebælt.py reads traffic data from a CSV file, filters the information according to specific years, 
and saves it into separate Excel files (.xlsx) with visualizations of the data. It also estimates the approximate profit 
of the StoreBelt A/S company, noting that this estimate is likely understated because it uses modern discount prices; 
historical pricing data is not publicly available.

![Optional Text](../master/barplot.png)
![Optional Text](../master/pie_chart.png)

   
These calculations are meant to expand understanding and comprehension of data science techniques 
using tools such as Python and the Pandas library.

3. Processing of environmental data from miljoeportal.dk.
For the custom access are available data with sewage, lake, lake-bottom condition, rivers, underground water.
We can get raw data in csv format and manipulate with that in desirable way. I am used to build plots with sorted data.
In this situation for specific  sample-place.

Environmental data of air contamination. Surprisingly very low rates with pollutants concentration were published by Danish
national center of environment and energy. According to your request server can withdraw collected data about some most 
common pollutants. Presumably, it is because, Denmark does not have a metallurgy, chemical industry, as it may be. 
Government rules and regulations impacted in positive way an agriculture, traffic regulations, building area have been 
playing crucial role in pollutants rates declining.

https://github.com/tech-science-club/datascience_projects/blob/09db7fa2103c3cf324dc4b179b1267b3be2889be/contamination_air.png
