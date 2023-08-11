
# Import all the relevant libraries and sub-modules
from tableauhyperapi import HyperProcess, Telemetry, Connection, TableDefinition, SqlType, Inserter, CreateMode
import psycopg2
import tableauserverclient as TSC



###
### SECTION: FETCHING DATA FROM POSTGRES
###

# Establish the connection w/ postgres
conn = psycopg2.connect(
    database='<insert-db-name>', user='<insert-db-username>', password='<insert-db-password>', host='127.0.0.1', port='5432'
)
print('\nEstablishing a connection with postgres..')

# Set auto commit to true
conn.autocommit = True

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Retrieve the data
cursor.execute('''SELECT * FROM public."Superstore"''')

# Fetch the the column names & data types
headers = [row[0] for row in cursor.description]
type_codes = [row[1] for row in cursor.description]
data_types = []
for value in type_codes:
    if value == 1043:
        data_types.append(SqlType.text())
    elif value == 23:
        data_types.append(SqlType.int())
    else:
        data_types.append(SqlType.double())

# Feed the column names & data types into a Table Definition list
TD_list = []
for i in range(len(headers)):
    TD_list.append(TableDefinition.Column(headers[i], data_types[i]))

# Fetch all the rows of data and convert a list of tuples into a list of lists
body = cursor.fetchall();
new_body = []
for row in body:
    new_body.append(list(row))

# Close the postgres connection
conn.close()



###
### SECTION: GENERATING THE HYPER FILE
###

# Start a new private local Hyper instance
with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU, 'myapp') as hyper:

    # Create the new extract and insert column names
    with Connection(hyper.endpoint, 'Superstore.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        schema = TableDefinition('Superstore', TD_list)
        connection.catalog.create_table(schema)
        print('\nCreating a new .hyper file..')

        # Insert rows
        with Inserter(connection, schema) as inserter:
            inserter.add_rows(new_body)
            inserter.execute()
            print('\nInserting rows..')

        # Close the hyper db connection
        connection.close()



###
### SECTION: PUBLISHING THE HYPER FILE TO TABLEAU CLOUD/SERVER
###

# Authenticate into Tableau Cloud using a Personal Access Token
tableau_auth = TSC.PersonalAccessTokenAuth('<insert-PAT-name>', '<insert-PAT-secret>', '<insert-Site-name>')
server = TSC.Server('<insert-Server/Cloud-domain>', use_server_version=True)
server.auth.sign_in(tableau_auth)

# Define needed parameters
project_id = ''
file_path = './Superstore.hyper'

# Target the relevant Project by fetching Project ID
all_project_items, pagination_item = server.projects.get()
for proj in all_project_items:
    if proj.name == '<insert-Project-name>':
        project_id = proj.id
        break

# Publish the new data source
new_datasource = TSC.DatasourceItem(project_id)
new_datasource = server.datasources.publish(new_datasource, file_path, 'Overwrite')
print('\nNew datasource published successfully!')

# Sign out of Tableau Cloud
server.auth.sign_out()