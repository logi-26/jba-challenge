# README #  
JBA Code Challenge  

### Details ###  
This is a Python script to parse rain precipitation data from a local file, format the data, create a database table and insert the formatted data into a local SQLite database.  
The script accepts 1 optional parameter, which is the path to a local file containing precipitation data.  
If no parameters are passed to the script, it will search in the local script directory and use the first .pre file that it can find.  

### Usage ###  
The script requires Python 3.8+  
No other libraries are required  

### Clone this repo: ###  
git clone https://github.com/logi-26/jba-challenge  

### Change into the repo directory: ###  
cd jba-challenge/  

### Run the script with no parameters to import the data from the .pre file in the script directory: ###  
python3 parse_rain_data.py  

### Or pass a custom file path to the script as a command line parameter: ###  
python3 parse_rain_data.py /home/username/some_file.pre  

### Output: ###  
The script will generate an SQLite database named 'precipitation_database' in the script directory.  
