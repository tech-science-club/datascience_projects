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

![Optional Text](../master/contamination_Svaneke%20Renseanl%C3%A6g.png)

4. Environmental data of air contamination. Surprisingly very low rates with pollutants concentration were published by Danish
national center of environment and energy. According to your request server can withdraw collected data about some most 
common pollutants. Presumably, it is because, Denmark does not have a metallurgy, chemical industry, as it may be. 
Government rules and regulations impacted in positive way an agriculture, traffic regulations, building area have been 
playing crucial role in pollutants rates declining.

![Optional Text](../master//contamination_air.png)
Interesting things about limit permissible concentrations. To find each value you have to put effords. And different organiastion
has a different opinion about that.
Scientists have decied to convert concentration units into parts per mln, but forgot that each substance molecule has its own waight.
CO2 is heavier then HN3 more then 2 times. If conventional scale was created in 17th century with standarts of meters, kilograms unit etc,
why we have to make new wheel up? 
nobody knows. 
here is a couple of found data about permisssible limit concentration of gases in the Air

![Optional Text](../master//contamination_air.png)
