import io
import os
import pandas as pd
import matplotlib as mpl
import xlsxwriter
from xlsxwriter import Workbook
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
# import BarChart class from openpyxl.chart sub_module
from openpyxl.chart import BarChart,Reference

data = pd.read_csv('trafficdata.csv', sep=";", encoding='ISO-8859-1')

count = 0
start_year = 2024
MC_og_Bil  = 0
Bil_3_6_m = 0
Bil_anhænger = 0
Små_lastbiler = 0
Store_lastbiler = 0
Lastbiler_over_20_meter = 0
Busser = 0
frames = {}

#prices:
MC_og_Bil_price  = 100
Bil_3_6_m_price = 200
Bil_anhænger_price = 300
Små_lastbiler_price = 300
Store_lastbiler_price =936
Lastbiler_over_20_meter_price = 1401
Busser_price = 936

for index, row in data.iterrows():

    filtered_data = data[data['År'] == start_year]
    frames[f'frame_{start_year}'] = filtered_data
    MC_og_Bil= filtered_data['MC og Bil'].sum()
    Bil_3_6_m = filtered_data['Bil 3-6m'].sum()
    Bil_anhænger = filtered_data['Bil+anhænger'].sum()
    Små_lastbiler =filtered_data['Små lastbiler'].sum()
    Store_lastbiler = filtered_data['Store lastbiler'].sum()
    Lastbiler_over_20_meter = filtered_data['Lastbiler over 20 meter'].sum()
    Busser = filtered_data['Busser'].sum()

    items = [
        'MC og Bil', 'Bil 3-6m', 'Bil+anhænger', 'Små lastbiler',
        'Store lastbiler', 'Lastbiler over 20 meter', 'Busser'
    ]
    Sum = [
        MC_og_Bil, Bil_3_6_m, Bil_anhænger, Små_lastbiler,
        Store_lastbiler, Lastbiler_over_20_meter, Busser
    ]
    #-----------------plot for each year---------------------------------------
    plt.figure(figsize=(10, 6))
    sns.barplot(x=items, y=Sum, width=0.5, hue=items )
    plt.xticks(rotation=20, ha='right')
    plt.title(f'Traffic in {start_year}')
    plt.xlabel('Transport type')
    plt.ylabel('Amount vehicles in mln')
    plt.tight_layout()
    #plt.show()
    plt.savefig(f'{start_year}.png')
    plt.close()

    with pd.ExcelWriter(f'sorted_data_traffic_according_to_years/{start_year}.xlsx', engine='xlsxwriter') as writer:
        filtered_data.to_excel(writer, sheet_name='Data', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Data']
        imgdata = io.BytesIO()
        worksheet.insert_image(20, 0, f'{start_year}.png')
    os.remove(f'{start_year}.png')

    print(frames[f'frame_{start_year}'])
    print("MC+small car: " + str(MC_og_Bil))
    print("car 3-6m: "+str(Bil_3_6_m))
    print("Car+trailer: "+str(Bil_anhænger))
    print("Small tracks: " +str(Små_lastbiler))
    print("Big tracks: " + str(Store_lastbiler))
    print("Tracks 20m +: " + str(Lastbiler_over_20_meter))
    print("Buses: "+  str(Busser))

    start_year -= 1
    if start_year < 1998:
        break


val1= data['MC og Bil'].sum()
val2 = data['Bil 3-6m'].sum()
val3 = data['Bil+anhænger'].sum()
val4 = data['Små lastbiler'].sum()
val5 = data['Store lastbiler'].sum()
val6 = data['Lastbiler over 20 meter'].sum()
val7 = data['Busser'].sum()


val1_price = MC_og_Bil_price*val1
val2_price = Bil_3_6_m_price * val2
val3_price =  Bil_anhænger_price *val3
val4_price =  Små_lastbiler_price *val4
val5_price =  Store_lastbiler_price *val5
val6_price =  Lastbiler_over_20_meter_price *val6
val7_price =  Busser_price *val7
total_revenue = val1_price + val2_price + val3_price + val4_price + val5_price + val6_price + val7_price

total_items = [
                'MC+small car',
                'car_3_6m',
                'Car_trailer',
                'Small_tracks',
                'Big_tracks',
                'Tracks_20m',
                'Buses'
              ]

total_amaunt = [
                val1,
                val2,
                val3,
                val4,
                val5,
                val6,
                val7,
                ]
total_rev = [
                val1_price,
                val2_price,
                val3_price,
                val4_price,
                val5_price,
                val6_price,
                val7_price,
            ]

result_df = pd.DataFrame(
    {
        'items':  total_items,
        'amount of vehicles': total_amaunt,
        'total profit': total_rev,
        'currency': "dkk"
    }
)
print("------------------------total----------------------------")
print(result_df)
print(f"total_revenue {total_revenue} dkk")


plt.figure(figsize=(8, 6))
plots = sns.barplot(x=total_items, y=total_amaunt, width=0.75, gap=0.1, hue=items, legend=False)
for bar in plots.patches:
    plots.annotate(format(bar.get_height(), '.2e'),
                   (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='center',
                   size=10, xytext=(0, 8),
                   textcoords='offset points')

plt.xticks(rotation=20, ha='right')  # Rotate x labels for better readability
plt.title('Storbælt traffic 1998-2024 years', ha='center')  
plt.xlabel('Transport type')
plt.ylabel('Amount vehicles in mln')
plt.tight_layout()  # Adjust layout to fit labels
plt.savefig('barplot.png')


#----------------------------------------------------------------------------
#pie chart view

explode = (0, 0.1, 0, 0, 0, 0.35, 0.25)
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))
ax.pie(total_amaunt, autopct='%1.1f%%',  explode = explode, startangle=145, shadow=False, textprops={'size': 'smaller'},  pctdistance = 1.1,  wedgeprops=dict(width=0.5))
plt.text(x=1.5, y=-1.5, s=f"Total revenue:\n{total_revenue} dkk", fontsize=12, color='Black', ha='center')
plt.tight_layout()
ax.legend(total_items, title="Transport", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize='small', shadow=True)
fig.suptitle("Storebelt traffic, 1998-2024 years", fontsize=16)
plt.tight_layout()
plt.savefig('pie_chart.png')
plt.show()

with pd.ExcelWriter('storbelt_data.xlsx', engine='xlsxwriter') as writer:
    # Write the DataFrame to Excel
    data.to_excel(writer, sheet_name='Data', index=False)
    result_df.to_excel(writer, sheet_name='Data', index=False, startrow = 0, startcol = 11)
    workbook = writer.book
    worksheet = writer.sheets['Data']
    #worksheet.write_string(0, 317, out_str)

    imgdata = io.BytesIO()
    worksheet.insert_image(0, 17, 'pie_chart.png')
    worksheet.insert_image(40, 17, 'barplot.png')






