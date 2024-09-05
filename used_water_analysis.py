import io
import os
import pandas as pd
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt


#capital region, wastewater
data = pd.read_csv('used_water_pollution_data/Renseanl_g(Spildevand)_20240903_203359Hovdestaden.csv', sep="\t", encoding='ISO-8859-1') #encoding='ISO-8859-1'
df = pd.DataFrame(data)

# Sort the DataFrame by date
df_sorted = df.sort_values(by='Stedtekst')

# Select relevant columns
data_frame = df_sorted[['Stedtekst', 'Dato', 'Stofparameter', 'Resultat-attribut', 'Resultat', 'Enhed']]

# Get unique dates
unique = data_frame['Stedtekst'].unique()

# Create separate DataFrames for each unique date
separate_dataframes = {}
count = 0
cnt_avg = 0
for val in unique:
    df_filtered = data_frame[data_frame['Stedtekst'] == val]
    separate_dataframes[val] = df_filtered
    count +=1
print("amount of places are: "+str(count))
print(unique)

print("---------------max results--------------------")
frame1 = ['Dato','Stedtekst','Stofparameter', 'Resultat-attribut', 'Resultat', 'Enhed']
df_ = df[frame1].copy()
df_['Resultat'] = df_['Resultat'].str.replace(',', '.')
df_['Resultat'] = pd.to_numeric(df_['Resultat'], errors='coerce')
df_group = df_.groupby('Stofparameter').agg({'Resultat': 'mean'}).reset_index()




idx = df_.groupby('Stofparameter')['Resultat'].idxmax()

# Use this index to filter the DataFrame
df_max = df_.loc[idx, ['Stedtekst', 'Stofparameter', 'Resultat']]
print(df_max)

for val, df in separate_dataframes.items():
    print(f"\nData for {val}:")
    frame = ['Dato','Stedtekst','Stofparameter', 'Resultat-attribut', 'Resultat', 'Enhed']
    df_2 = df[frame].copy()
    df_2['Resultat'] = df_2['Resultat'].str.replace(',', '.')
    df_2['Resultat'] = pd.to_numeric(df_2['Resultat'], errors='coerce')
    df_grouped = df_2.groupby('Stofparameter').agg({'Resultat': 'mean'}).reset_index()
    print(df_2)

    # Exclude items
    df_2 = df_2[df_2['Stofparameter'] != 'pH']
    df_2 = df_2[df_2['Stofparameter'] != 'pH-målingstemperatur']
    df_2 = df_2[df_2['Stofparameter'] != 'Suspenderede stoffer']

    df_2['Resultat'] = pd.to_numeric(df_2['Resultat'], errors='coerce')
    Stofparameter = df_2['Stofparameter']
    Resultat = df_2['Resultat']

    df_grouped = df_2.groupby('Stofparameter').agg({'Resultat': 'mean'}).reset_index()

    #print("---------------max results--------------------")
    idx = df_2.groupby('Stofparameter')['Resultat'].idxmax()
    #
    ## Use this index to filter the DataFrame
    df_max = df_2.loc[idx, ['Stedtekst', 'Stofparameter', 'Resultat', 'Enhed']]
    print(f"----------data for {val} location-------------")
    print(df_max)



    if val == 'Svaneke Renseanlæg':
       plt.figure(figsize=(10, 6))
       plots = sns.barplot(x=Stofparameter, y=Resultat,  gap=0.1, hue=Stofparameter, legend=False, errorbar=None)
       for bar in plots.patches:
           plots.annotate(format(bar.get_height(), '.2f'),
                          (bar.get_x() + bar.get_width() / 2,
                           bar.get_height()), ha='center', va='center',
                          size=10, xytext=(0, 8),
                          textcoords='offset points')

       plt.title(f"Contaminants in sawege, {val}")
       plt.xlabel('Compounds')
       plt.ylabel('Concentration, mg/L')
       plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels if needed
       plt.tight_layout()  # Adjust layout to fit labels

       plt.savefig(f'contamination_{val}.png')

       plt.show()

