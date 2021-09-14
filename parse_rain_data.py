# System imports
from sys import argv
from os import listdir
from os.path import exists, join, abspath, dirname
from argparse import ArgumentParser
from datetime import datetime

# Local imports
from database import create_precipitation_table, insert

# Constants
DATABASE_NAME = 'precipitation_database'


# *********************************************************************************
# This function parses the command line paramaters and returns the path to the .pre file
def _get_file_path():
	# Instantiate the parser
	parser = ArgumentParser(description='This application parses the precipitation data from a file and inserts it into a local SQLite database.')
	
	# Optional file path argument
	parser.add_argument('file_path', type=str, nargs='?', help='An optional path to a file containing the precipitation data.')
	
	# Parse the file path from the command line arguments
	file_path = parser.parse_args().file_path
	
	# If a file path has not been provided or the file path is invalid
	if file_path is None or not exists(file_path):

		# Get the script path
		root_dir = abspath(dirname(argv[0]))
		
		# Search the script directory for any .pre files and use the first one we find
		for file in listdir(root_dir):
			if file.endswith('.pre'):
				file_path = join(root_dir, file)
				break
				
	# If no .pre files can be located, exit the app
	if file_path is None:
		print('\nCould not find any .pre files.\nExiting app.\n')
		exit()
	else:
		print(f'\nImporting precipitation data from file: {file_path}')
	
	return file_path
# *********************************************************************************


# *********************************************************************************
# This function performs some very basic validation on the precipitation data file 
def _is_file_valid(file_content_list):
	years_present = False
	grid_ref_present = False
	
	# Loop through the rows to see if our required values are present in the precipitation data
	for row in file_content_list:
		if years_present and grid_ref_present:
			break
		if 'years' in row.lower():
			years_present = True
		if 'grid-ref=' in row.lower():
			grid_ref_present = True
	
	return years_present and grid_ref_present
# *********************************************************************************


# *********************************************************************************
# This function parses and returns the year range from the file header data
def _get_year_range(file_content_list):
	# Get the line number for the last line in the file header
	for count, row in enumerate(file_content_list):
		if 'grid-ref=' in row.lower():
			header_end = count -1
			break
	header_last_line = file_content_list[header_end]
			
	# Find the 'Years=' substring from the header data
	start_position = header_last_line.lower().find('years=') + 6
	
	# Parse the start year
	start_year = header_last_line[start_position: start_position +4]
	
	# Parse the end year
	start_position +=5
	end_year = header_last_line[start_position: start_position +4]
	
	return int(start_year), int(end_year), header_end
# *********************************************************************************


# *********************************************************************************
# This function parses and returns the grid reference values
def _get_grid_ref(line):
	# Split the line at the position of the comma
	split_line = line.split(',')
	
	# Filter just the digits from either side of the comma to get the xref and yref
	xref = ''.join(filter(str.isdigit, split_line[0]))
	yref = ''.join(filter(str.isdigit, split_line[1]))
	return xref, yref
# *********************************************************************************


# *********************************************************************************
# This function parses the rain data and formats it into a list of tuples
def _get_rain_data(file_content_list, header_end, start_year):
	# List to store the output
	output_list = []

	# Loop through each of the lines, ignoring the file header
	for count, row in enumerate(file_content_list):
		if count > header_end:
			
			# Get the xref and yref values and reset the current year value 
			if 'grid-ref=' in row.lower():
				current_year = start_year
				xref, yref = _get_grid_ref(row)
			else:
				# Store all of the values for a 12 month period in a list
				months = ','.join(row.split()).split(',')
				
				# Loop through each month, format the data and add it to the output list
				for i in range(len(months)):
					if months[i] != '':
						output_list.append((xref, yref, f'{i+1}/1/{current_year}', months[i]))
						
				# Increment the current year value
				current_year += 1
	
	return output_list
# *********************************************************************************


# *********************************************************************************
# This function generates the insert statement to insert all of the precipitation data
def _compose_precipitation_insert_statement(output_list):
	insert_string = "INSERT INTO 'precipitation' (Xref, Yref, Date, Value) VALUES "
	for count, row in enumerate(output_list):
		if len(row) == 4:
			if count != len(output_list)-1:
				insert_string += f"({row[0]}, {row[1]}, '{row[2]}', {row[3]}),"
			else:
				insert_string += f"({row[0]}, {row[1]}, '{row[2]}', {row[3]});"
		
	return insert_string
# *********************************************************************************


# *********************************************************************************
# Main function
def main():	 
	start_time = datetime.now()
	
	# Get the path to the precipitation data file 
	file_path = _get_file_path()
			
	# Read the file into a list
	file_content_list = []
	with open(file_path, 'r', encoding='UTF-8') as file:
		while (line := file.readline().rstrip()):
			file_content_list.append(line)
	
	# Perfrom some basic validation checks on the file and exit the app if the file is not valid
	if not _is_file_valid(file_content_list):
		print(f'The file does not appear to contain valid precipitation data.\nExiting app.\n')
		exit()
		
	# Parse the start/end year range from the file header
	start_year, end_year, header_end = _get_year_range(file_content_list)

	# Parse the rain data into a list
	output_list = _get_rain_data(file_content_list, header_end, start_year)

	# Compose the SQL insert string
	insert_string = _compose_precipitation_insert_statement(output_list)
	
	try:
		# Create the database table to store the data
		create_precipitation_table(DATABASE_NAME)
	
		# Insert the data into the local SQLite database
		insert(DATABASE_NAME, insert_string)
		print(f'The data has been formatted and exported to a local SQLite database: {join(abspath(dirname(argv[0])), DATABASE_NAME)}')
		
	except Exception as exception:
		print(f'Exception: {exception}')
		
	print(f'Script run time: {datetime.now() - start_time}\n')
# *********************************************************************************


if __name__ == "__main__":
	main()
