"""Weather Visuals - Samantha Song - 2025.02.27"""
# Data from NOAA - https://www.ncei.noaa.gov/data/coop-hourly-precipitation/v2/
# Explainations for CSV
# https://www.ncei.noaa.gov/data/coop-hourly-precipitation/v2/doc/readme.csv.txt

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data
FILE_NAME = 'USC00022754.csv'
data = pd.read_csv(FILE_NAME, low_memory=False)
FOLDER = 'Weather Plots/'

# Replace no data with 0
data = data.replace(-9999, 0)
# Add Columns for Graphs
data['YEAR'] = data['DATE'].str.slice(0,4)
data['MONTH'] = data['DATE'].str.slice(5,7).astype(int)
# Add Daily Rainfall in inches
data['DAILY RAINFALL'] = data['HR00Val']
hour = ''
for i in range(1, 24):
    if i < 10:
        hour = '0' + str(i)
    else:
        hour = str(i)
    hour_data = 'HR' + hour + 'Val'
    data['DAILY RAINFALL'] += data[hour_data].astype(float) / 100

# Yearly Data: 2d Array [year, rainfall]
yearly_data = np.empty((0, 2))
for year in range(1975, 2025):
    year_rainfall = data[data['DATE'].str.startswith(str(year))]['DAILY RAINFALL'].sum()
    yearly_data = np.append(yearly_data, np.array([[year, year_rainfall]]), axis=0)

yearly_graph = sns.lineplot(x=yearly_data[:,0], y=yearly_data[:,1])
yearly_graph.set_title('Total Rainfall (inches) by Year')
yearly_graph.set_xlabel('Year')
yearly_graph.set_xlim(1975, 2024)
yearly_graph.set_ylabel('Rainfall (inches)')
plt.show()

# Histogram - By Year split by Month
year_histogram = sns.histplot(data, x='YEAR', weights='DAILY RAINFALL',
                              hue='MONTH', multiple='stack',
                              palette=sns.color_palette('Spectral', n_colors=12))
year_histogram.tick_params(axis='x', rotation=90)
year_histogram.set_title('Total Rainfall (inches) by Year')
year_histogram.set_xlabel('Year')
year_histogram.set_ylabel('Rainfall (inches)')
plt.savefig(FOLDER + 'Rainfall by Year' + '.png', dpi=300)
plt.show()

# Data - Month
month_box = sns.barplot(data, x='MONTH', y='DAILY RAINFALL',
                        hue='MONTH', legend=False,
                        palette=sns.color_palette('Spectral', n_colors=12))
month_box.set_title('Total Rainfall (inches) by Month')
month_box.set(xlabel='Month', ylabel='Rainfall (inches)')
plt.savefig(FOLDER + 'Rainfall by Month' + '.png', dpi=300)
plt.show()

