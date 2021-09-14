# System imports
from sqlite3 import connect


# *********************************************************************************
# This function creates a table to store the precipitation data
def create_precipitation_table(database_name):
	# Create a database connection
	try:
		connection = connect(database_name) 
	except Exception as exception:
		raise

	# Create the table and commit the changes
	try:
		cursor = connection.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS precipitation ([Xref] INTEGER, [Yref] INTEGER, [Date] TEXT, [Value] INTEGER)''')	  
		connection.commit()
	except Exception as exception:
		raise

	# Close the connection
	finally:
		connection.close()
# *********************************************************************************


# *********************************************************************************
# This function inserts data into the database
def insert(database_name, insert_string):
	# Create a database connection
	try:
		connection = connect(database_name) 
	except Exception as exception:
		raise

	# Insert the data and commit the changes
	try:
		cursor = connection.cursor()
		cursor.execute(f'''{insert_string}''')	  
		connection.commit()
	except Exception as exception:
		raise

	# Close the connection
	finally:
		connection.close()
# *********************************************************************************
