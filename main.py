##
from tqdm import tqdm
import numpy as np
import pandas as pd
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import datetime
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import copy
is_ipython = 'inline' in plt.get_backend()
if is_ipython: from IPython import display

## Loading meters CSV file data into a dictionary of data frames
dict_of_df = {}
min_index = np.power(10,10)
max_index = 0
min_meter = 0
max_meter = 0
for i in range(1,12):
    df = pd.read_csv('electricity/{}.csv'.format(i), index_col=0)
    if df.index[0] < min_index:
        min_index = df.index[0]
        min_meter = i
    if  df.index[-1] > max_index:
        max_index = df.index[-1]
        max_meter = i
    key_name = 'df' + str(i)
    dict_of_df[key_name] = copy.deepcopy(df)
    print('Data {} loaded! Min index is: {} from {} and Max index is: {} from {}'.format(i, min_index, min_meter, max_index, max_meter))

## Creating a big 0 data frame for each meter and updating available CSV files into it to make all of them as the same length
with tqdm(total=len(dict_of_df)) as progress_bar:
    for key, df in dict_of_df.items():
        cols = ['W', 'VAR', 'VA', 'f', 'V', 'PF', 'A']
        df_zero = pd.DataFrame(0, index = range(min_index , max_index), columns= cols)
        print("Created df of zeros for {}".format(key))
        df_zero.update(df)
        print("Updated {}".format(key))
        df_zero.to_csv('temp_df/temp_{}.csv'.format(key))
        print("Saved {}".format(key))
        progress_bar.update(1)


## Loading different appliance consumtions into a dictionary of dataframes to do the data preparation
number_of_tests = 1
dict_of_updated_df = {}
for i in tqdm(range(number_of_tests)):
    temp_df = pd.read_csv('temp_df/temp_df{}.csv'.format(i+1))
    dict_of_updated_df['appliance' + str(i+1)] = copy.deepcopy(temp_df)
print('All meters loaded!')

## Casting all dataframes into the range of 1,200,000 to 6,368,000 which is the efficient period of sampling. the index is reset for all DFs
for app_number in tqdm(range(number_of_tests)):
    dict_of_updated_df['appliance' + str(app_number+1)] = dict_of_updated_df['appliance' + str(app_number+1)][1200000:6368000].reset_index()
print('Casting to new time period done!')

## Removing main_1 and main_2 non_float items (string in some rows)
for app_number in tqdm(range(number_of_tests)):
    for column in dict_of_updated_df['appliance' + str(app_number+1)].columns:
        dict_of_updated_df['appliance' + str(app_number + 1)][column] = pd.to_numeric(getattr(dict_of_updated_df['appliance' + str(app_number + 1)], column).astype(str), errors='coerce').fillna(0).astype(int)

print("main_1 and main_2 are cleared of strings!")


## Dropping unnecessary columns of 'index' and 'unnamed: 0' and 'level_0'in all the DFs
for app_number in tqdm(range(number_of_tests)):
    if 'index' in dict_of_updated_df['appliance' + str(app_number + 1)].columns:
        dict_of_updated_df['appliance' + str(app_number + 1)].drop('index', inplace=True, axis=1)
    if 'level_0' in dict_of_updated_df['appliance' + str(app_number + 1)].columns:
        dict_of_updated_df['appliance' + str(app_number + 1)].drop('level_0', inplace=True, axis=1)
    if 'Unnamed: 0' in dict_of_updated_df['appliance' + str(app_number + 1)].columns:
        dict_of_updated_df['appliance' + str(app_number + 1)].drop('Unnamed: 0', inplace=True, axis=1)
print("All unnecessary columns are dropped!")

## Filling all-zero rows that has happened between data due to mis-sampling with the previous data point value
for app_number in tqdm(range(number_of_tests)):
    for i in tqdm(range(len(dict_of_updated_df['appliance' + str(app_number + 1)]))):
        if (dict_of_updated_df['appliance' + str(app_number + 1)].loc[i][:] == 0).all() and (dict_of_updated_df['appliance' + str(app_number + 1)].loc[i-1][:] != 0).any() :
            dict_of_updated_df['appliance' + str(app_number + 1)].loc[i] = dict_of_updated_df['appliance' + str(app_number + 1)].loc[i-1]
            i += 1
    dict_of_updated_df['appliance' + str(app_number + 1)].to_csv("prepared data/app{}.csv".format(app_number+1))
    print("Appliance {} data is prepared and saved".format(app_number+1))
print("All appliances data are cleared and ready to use!")
##

## Ploting all appliances Active power
fig = plt.figure()
# plt.plot(fridge.W, color='blue', label="Fridge W",linewidth=0.5, linestyle=":")
# plt.plot(iron.W, color='red', label="iron W",linewidth=0.5, linestyle="-.")
# plt.plot(ac_2.W, color='green', label="ac_2 W",linewidth=0.5, linestyle="--")
# plt.plot(ac_1.W, color='green', label="ac_1 W",linewidth=0.5, linestyle="--")
# plt.plot(water_filter.W, color='orange', label="water_filter W",linewidth=0.5, linestyle="-")
# plt.plot(tv.W, color='black', label="tv",linewidth=0.5, linestyle=":")
# plt.plot(laptop.W, color='magenta', label="laptop W",linewidth=0.5, linestyle="-.")
# plt.plot(washing_machine.W, color='cyan', label="washing machine W",linewidth=0.5, linestyle="--")
# plt.plot(kitchen_outlet.W, color='cyan', label="kitchen outlet W",linewidth=0.5, linestyle="-")
plt.plot(dict_of_updated_df['appliance1'].W, color='blue', label="main_1 W",linewidth=0.5, linestyle="-")
# plt.plot(main_2.W, color='brown', label="main_2 W",linewidth=0.5, linestyle=":")

fig.tight_layout()
plt.xlabel('Time step (s)', fontsize=18)
plt.ylabel('Values', fontsize=18)
plt.legend(['Fridge', 'Iron', 'ac_1','ac_2', 'Watre filter', 'tv', 'laptop', 'washing machine', 'Kitchen outlet', 'main_1', 'main_2'])
plt.show()

## Ploting four appliances Active power
fig = plt.figure()
plt.plot(fridge.W, color='blue', label="Fridge W",linewidth=0.5)
# plt.plot(fridge.VAR, color='red', label="iron W",linewidth=0.5)
# plt.plot(fridge.f, color='green', label="ac_2 W",linewidth=0.5)
# plt.plot(fridge.VA, color='orange', label="water_filter W",linewidth=0.5)


fig.tight_layout()
plt.xlabel('Time step (s)', fontsize=18)
plt.ylabel('Values', fontsize=18)
plt.legend(['W', 'Q', 'f', 'S'])
plt.show()

## Ploting P and Q of the fridge

fig = plt.figure()
plt.plot(main_1.W, color='blue', label="main_1 W",linewidth=0.5)
plt.plot(main_1.VAR, color='red', label="main_1 Q",linewidth=0.5)
plt.plot(main_1.VA, color='orange', label="main_1 W",linewidth=0.5)
plt.plot(main_1.f, color='green', label="main_1 Q",linewidth=0.5)
plt.plot(main_1.V, color='cyan', label="main_1 W",linewidth=0.5)
plt.plot(main_1.PF, color='magenta', label="main_1 Q",linewidth=0.5)
plt.plot(main_1.A, color='black', label="main_1 W",linewidth=0.5)

fig.tight_layout()
plt.xlabel('Time step (s)', fontsize=18)
plt.ylabel('Values', fontsize=18)
plt.legend(['Main_1 W', 'Main_1 Q','S','f','V','PF','I'])
plt.show()

