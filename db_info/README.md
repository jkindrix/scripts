# SQL Server Database Information Fetcher

This script fetches and outputs schema information and sample data for all tables in a specified SQL Server database. The output is written to a specified file in a human-readable format.

## Prerequisites

- Python 3.x
- Virtual Environment (optional but recommended)
- Required Python packages: `pyodbc`, `pandas`, `sqlalchemy`
- ODBC Driver for SQL Server

## Installation

### Setting Up the Environment

1. **Install Python 3 and pip** (if not already installed):

    ```sh
    sudo apt update
    sudo apt install python3 python3-pip
    ```

2. **Install `venv` package** (if not already installed):

    ```sh
    sudo apt install python3-venv
    ```

3. **Create and activate a virtual environment**:

    ```sh
    python3 -m venv sqlserver_env
    source sqlserver_env/bin/activate
    ```

4. **Install the required Python packages**:

    ```sh
    pip install pyodbc pandas sqlalchemy
    ```

5. **Install ODBC Driver for SQL Server**:

    ```sh
    # Add Microsoft repository key and repository
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    sudo curl https://packages.microsoft.com/config/debian/10/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

    # Update package list and install ODBC driver
    sudo apt-get update
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
    sudo apt-get install -y unixodbc-dev
    ```

## Configuration

Create a configuration file named `config.ini` with the following content:

```ini
[DEFAULT]
server = your_server_name
database = your_database_name
username = your_sql_username
password = your_sql_password
output_file = path/to/output.txt
```

Replace the placeholders with your actual SQL Server connection details and desired output file path.

## Usage

Run the script with the configuration file as an argument:

```sh
python fetch_db_info.py --config config.ini
```

### Example

```sh
python fetch_db_info.py --config config.ini
```

The script will connect to the specified SQL Server database, fetch schema information and sample data for all tables, and write the output to the specified file.

## Output

The output file will contain the schema and sample data for each table in a clean and human-readable format. Here’s an example of what the output might look like:

```
SQL Server Database Information
===============================

====================
Table: dbo.Customers
====================

Schema:
COLUMN_NAME  DATA_TYPE  IS_NULLABLE  CHARACTER_MAXIMUM_LENGTH
CustomerID   int        NO           None
Name         nvarchar   YES          255
Email        nvarchar   YES          255

Sample Data:
CustomerID  Name         Email
1           John Doe     john.doe@example.com
2           Jane Smith   jane.smith@example.com

...

```

## Logging

The script uses Python's logging module to provide runtime information and debug messages. Logs are printed to the console.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

This version should render properly on GitHub or any other markdown viewer.