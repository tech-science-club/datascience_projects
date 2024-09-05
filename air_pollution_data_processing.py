import io
import os
import pandas as pd
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt


files_to_merge = ['air_contamination/NO.csv',
                  'air_contamination/NO2.csv',
                  'air_contamination/NOx.csv',
                  'air_contamination/CO.csv',
                  'air_contamination/SO2.csv'
                  ]

cnt = 0
n = 0
frame_list = {}
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

for file in files_to_merge:
    temp_df = pd.read_csv(file, sep=";", encoding='ISO-8859-1')

    file_name = os.path.splitext(file)[0]
    file_name = file_name.replace("/", " ")
    unique_var_name = f"df_{file_name}"
    df = pd.DataFrame(temp_df)
    frame_list[unique_var_name] = df

    year = df.iloc[3:, 0]
    data = df.iloc[3:, 3]

    data_frame = {"a": year, "b": data}
    data_ = pd.DataFrame(data_frame)
    data_['b'] = pd.to_numeric(data_['b'], errors='coerce')
    df_grouped = data_.groupby('a').agg({'b': 'mean'}).reset_index()
    x = df_grouped['a']
    y = df_grouped['b']
    ax = axes[cnt, n]
    plots = sns.barplot(x=x, y=y, data=df_grouped, ax=ax, hue=y, errorbar=None, legend=False)
    for bar in plots.patches:
        ax.annotate(format(bar.get_height(), '.2f'),
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha='center', va='center',
                    size=5, xytext=(0, 5),
                    textcoords='offset points')

    ax.set_title(f"{file_name}", fontsize=10)
    ax.set_xlabel("  ")
    ax.set_ylabel("Concentration μg/m³")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    if n % 2 == 0:
        n += 1
    else:
        n = 0
        cnt += 1
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
fig.suptitle("Air Pollutants, Denmark", fontsize=20)
plt.subplots_adjust(top=0.92, wspace=0.1, hspace=0.3)
plt.show()
plt.savefig(f'contamination_air.png')

#-------------------------to withdraw separate plots----------------------------------
#all_dataframes = []
#for file in files_to_merge:
#    temp_df = pd.read_csv(file, sep=";", encoding='ISO-8859-1')
#    all_dataframes.append(temp_df)
#
#combined_df = pd.concat(all_dataframes, ignore_index=True)
#
#year = combined_df.iloc[3:, 0]
## Convert 'year' to datetime if it represents time-series data
## year = pd.to_datetime(year)  # Uncomment if needed
#
#data = combined_df.iloc[3:, 3]

#    data_frame = {"a": year, "b": data}
#    data_ = pd.DataFrame(data_frame)
#    print(data_)
#    data_['b'] = pd.to_numeric(data_['b'], errors='coerce')
#    df_grouped = data_.groupby('a').agg({'b': 'mean'}).reset_index()
#    x = df_grouped['a']
#    y= df_grouped['b']
#    print(df_grouped)
#    plt.figure(figsize=(15, 8))
#    plots = sns.barplot(x=x, y=y, data=data_frame, gap=0.1, hue=y, legend=False, errorbar=None)  # Remove hue if not desired
#    for bar in plots.patches:
#        plots.annotate(format(bar.get_height(), '.2f'),
#                       (bar.get_x() + bar.get_width() / 2,
#                        bar.get_height()), ha='center', va='center',
#                       size=10, xytext=(0, 8),
#                       textcoords='offset points')
#
#    plt.xlabel("Years")
#    plt.ylabel("Concentration μg/m³")
#    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels if needed
#
#    # Add title if desired based on your analysis
#    plt.title(f"{file_name}")
#
#    plt.show()