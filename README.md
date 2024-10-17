# Importing States in PrestaShop from ISO 3166-2

This repository contains a Python script that compares countries and their administrative divisions (states, provinces, regions, etc.) in a PrestaShop database, based on the ISO 3166-2 standard. If missing states are identified for a country, the script automatically inserts them into the `ps_state` table.

## Requirements

- Python 3.x
- `mysql-connector-python` package for MySQL database connection.

You can install the MySQL connection package using `pip`:

`pip install mysql-connector-python`


**Description**

This script performs the following:

- Reads a JSON file with countries and their administrative divisions, based on the ISO 3166-2 standard.
- Queries the ps_country and ps_state tables in the PrestaShop database to get the registered countries and states.
- Compares the current states with those from the JSON file.
- Inserts missing states into the ps_state table, including the active field (enabled by default) and tax_behavior field (defaulted to 0).

**Usage Instructions**

Configure the database connection: Make sure to adjust the database credentials in the connect_to_db() function inside the import_states.py script. Modify your_host, your_user, your_password, and the database name to match your configuration.


```
    def connect_to_db():
    return mysql.connector.connect(
        host="your_host",      # Replace with your database host
        user="your_user",      # Replace with your database user
        password="your_password",  # Replace with your database password
        database="mallhabana-produccion"  # Replace with your database name
    )
```


Adjust table prefixes: PrestaShop uses a table prefix (default is ps_).  If your PrestaShop installation uses a custom prefix, ensure to update the SQL queries in the script to reflect your table prefix.

    For example, if the prefix is custom_, you need to change the queries from ps_country, ps_state, and ps_zone to custom_country, custom_state, and custom_zone.

Place the JSON file: The JSON file with countries and administrative divisions (iso-3166-2.json) can be downloaded from this [GitHub repository](https://github.com/olahol/iso-3166-2.json/blob/master/iso-3166-2.json) . Ensure to place it in the correct path and update the script to point to the right location:


    json_file = 'path_to/iso-3166-2.json'  # Update with the correct path to the JSON file


**Run the script:** Once everything is configured, you can run the script from the terminal with:

`python import_states.py`


The script will look for differences between the states in the database and those in the JSON file, inserting the missing ones.


**Notes**

    This script includes basic error handling for SQL issues, such as escaping apostrophes in state names containing special characters.
    The ps_state table includes the fields active (set to 1 by default) and tax_behavior (set to 0 by default) for each inserted state.



**Contributions**

Contributions are welcome. If you have any improvements or find any issues, please open an issue or create a pull request.
