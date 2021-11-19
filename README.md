<h1 align="center">
  <br>
  <img src="https://github.com/Mozaffar-Etezadifar/iAWE_NILM_dataset/blob/5cbe7d11436e2b0c20a02ce757a9e39e7f966d7b/pictures/iAWE_dataset_preprocessing__for_NILM.png" alt="Ax" width="800">
</h1>

#  Description
iAWE is a wonderful dataset for those of us who work on Non-Intrusive Load Monitoring (NILM) algorithms. You can find its main page and description via this [link](https://iawe.github.io/). If you are familiar with NILM-TK API, you probably know that you can work with iAWE hdf5 data file in NILM-TK. However I faced some problems that convinced me to Not use NILM-TK and iAWE hdf5 datafile. Instead, I decided to use the iAWE appliance consumption CSV files and preprocess them myself. So if you have problems with NILM-TK API and iAWE hdf5 data file too, this piece of code may help you to prepare 11 appliance consumption data for your NILM algorithm.

#  Installation
- First, download the iAWE dataset using this [link](https://drive.google.com/drive/folders/1c4Q9iusYbwXkCppXTsak5oZZYHfXPmnp) (also available on iAWE page!).
- Download the **electricity.tar.gz** file.

<h1 align="center">
  <br>
  <img src="https://github.com/Mozaffar-Etezadifar/iAWE_NILM_dataset/blob/2f166a1d3f75960ff2a2e55268312d5abb2351df/pictures/zip%20file.png" alt="Ax" width="400">
</h1>

- Download the repo and all its folders.
- Unzip the **electricity.tar.gz** and copy all 12 CSV file (plus the **labels** file into the electricity folder of the downloaded repo.
- Now everythng is ready for you to start the data preprocessing using the **main.py** file.
But before running the code let me show you what kind of problems we had with the original iAWE hdf5 file.

#  What problems did we solve?
Well, to be honest NILM-TK documentation is not very clear! If you try to use the hdf5 datafile of the datasets that works with NILM-TK, soon you will admit it. Sometimes you find the the similiar questions on stack overflow but when you try them, they simply don't work due to some updates in NILM-TK (undocumented maybe!?). So, having full control on the data was my main incentive to redo the data preprocessing by my self.
You see 12 CSV files in your downloaded files. They belong to:
- main meter (1)
- main meter (2)
- fridge
- air conditioner (1)
- air conditioner (2)
- washing machine
- laptop
- iron
- kitchen outlets
- television
- water filter
- water motor
The publisher of iAWE dataset has recommended to ignore the **water motor** CSV file as it is not accurate (so did we!). Each CSV file consists of `timestamp`, `W`, `VAR`, `VA`, `f`, `V`, `PF` and `A` columns. `timestamp` can be read and converted to read time and date by `Python` libraries. The publisher of dataset have collected time stamps to reduce the size of final data files which means there is no sampling when the appliances are not consuming power. On the other hand the start time of different appliances measurement is not the same so the length, start and end of most csv files are different. When you plot it in NILM-TK it is fine becuase it reads the timestamps and ignores the `NA` time steps. However when you want to feed this data into your algorithm it will be a problem which needs data preprocessing.
To better understand the problem when using the raw data in iAWE dataset, I've plotted `W` (active power) of the air conditioner which is CSV file number 4.

<h1 align="center">
  <br>
  <img src="https://github.com/Mozaffar-Etezadifar/iAWE_NILM_dataset/blob/3d565ffdf3722afd5ce226a38afd980ed73eb26c/pictures/1.png" alt="AC" width="800">
</h1>

As you see, when youplot it in `Python` the `NA` timestamp will be plotted as a direct line between last available data and the next available one. It is neither human readable (to some extents!) nor NILM algorithm readable. In fact what your NILM algorithm will be fed with is the series of these values because your algorithm has nothing to do with timestamps! See this is what NILM algorithm sees as the AC power consumption:

<h1 align="center">
  <br>
  <img src="https://github.com/Mozaffar-Etezadifar/iAWE_NILM_dataset/blob/3d565ffdf3722afd5ce226a38afd980ed73eb26c/pictures/2.png" alt="AC WO" width="800">
</h1>

Now to make it both human readable and NILM algorithm readable, I did as below: (I've commented the code so you can see what is happening in every part of the code)
- Loaded all CSV files in a dictionary of Dataframes with CSV file orders
- Measured the lowes and highest timestamp in order to know the length of the measurement period (they have different lengthes!)
- Created a big dataframe of zeros with from lowest timestamp to the highest one as its index
- Used the `update` method on dataframes to transfer the values of dataframes to the big dataframes of zeros (Now all of them have the same length)
- Putting all dfs into a dictionary of dataframes
- Casting all the dataframes into the efficient  period of sampling (Because now we know which part of sampling is useless)
- Removing `NAN` values
- Dropping unwanted columns
- Filling `NA` values with last available value in dataframes
- Saving all the dataframes as CSV files in the prepared data folder
- Done!

<h1 align="center">
  <br>
  <img src="https://github.com/Mozaffar-Etezadifar/iAWE_NILM_dataset/blob/3d565ffdf3722afd5ce226a38afd980ed73eb26c/pictures/3.png" alt="AC WO" width="800">
</h1>

#  Conclusion
Basically, what we have here after running this code is 11 CSV files of `W`, `VAR`, `VA`, `f`, `V`, `PF` and `A` for 11 different meters. Prepared CSV file are all of the same length without `NAN` or `NA` values which are ready to be fed to any NILM algorithm. Despite the fact that I've done these changes to iAWE dataset, I'm sure the publishers of this dataset have much better solution via NILM-TK to have such an output. However due to lack of documentation or changes in their code I prefered to do this data preprocessing myself. Hope you enjoy it!

