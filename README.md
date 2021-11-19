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
