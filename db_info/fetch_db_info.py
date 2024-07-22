#!/usr/bin/env python
#==============================================================================
#
#          FILE: fetch_sql_info.py
#
#         USAGE: ./fetch_sql_info.py --config <config_file>
#
#   DESCRIPTION: This script fetches SQL Server database information including
#                table schemas and sample data, and writes the information to
#                an output file.
#
#       OPTIONS: --config <config_file> : Path to the configuration file
#  REQUIREMENTS: Must be run in a Python environment with access to the required
#                packages and a valid configuration file.
#         NOTES: Ensure the configuration file contains all required parameters.
#        AUTHOR: Justin Kindrix, jkindrix@gmail.com
#  ORGANIZATION: None
#       CREATED: 2024-07-21
#      REVISION: 1.0
#       LICENSE: MIT License. See LICENSE file in the project root for full 
#                license information.
#
#==============================================================================

import pyodbc
import pandas as pd
import logging
import sys
import argparse
import configparser
from sqlalchemy import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['DEFAULT']

def get_connection_url(server, database, username, password):
    connection_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    return connection_url

def get_tables(engine):
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_SCHEMA, TABLE_NAME
    """
    try:
        tables = pd.read_sql(query, engine)
        logger.info("Fetched table list successfully.")
        return tables
    except Exception as e:
        logger.error(f"Error fetching table list: {e}")
        sys.exit(1)

def fetch_table_info(engine, schema, table):
    # Fetch table schema
    schema_query = f"""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
    """
    # Fetch sample table data
    data_query = f"SELECT * FROM [{schema}].[{table}]"
    try:
        schema_df = pd.read_sql(schema_query, engine)
        data_df = pd.read_sql(data_query, engine)
        sample_data_df = data_df.sample(min(len(data_df), 5))  # Get up to 5 random rows
        logger.info(f"Fetched schema and data for table {schema}.{table} successfully.")
        return schema_df, sample_data_df
    except Exception as e:
        logger.error(f"Error fetching data for table {schema}.{table}: {e}")
        return None, None

def write_table_info(schema_df, sample_data_df, output_file, schema, table):
    try:
        with open(output_file, 'a') as f:
            f.write(f"\n\n====================\n")
            f.write(f"Table: {schema}.{table}\n")
            f.write(f"====================\n\n")
            
            f.write("Schema:\n")
            f.write(schema_df.to_string(index=False))
            f.write("\n\nSample Data:\n")
            if not sample_data_df.empty:
                f.write(sample_data_df.to_string(index=False))
            else:
                f.write("No data available.")
            f.write("\n\n")
            
        logger.info(f"Data for table {schema}.{table} written to {output_file} successfully.")
    except Exception as e:
        logger.error(f"Error writing data to file for table {schema}.{table}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fetch SQL Server database information.")
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
    args = parser.parse_args()

    config = read_config(args.config)
    server = config.get('server')
    database = config.get('database')
    username = config.get('username')
    password = config.get('password')
    output_file = config.get('output_file')

    if not all([server, database, username, password, output_file]):
        logger.error("Missing required configuration parameters.")
        sys.exit(1)

    connection_url = get_connection_url(server, database, username, password)
    engine = create_engine(connection_url)

    tables = get_tables(engine)

    # Clear or create the output file
    with open(output_file, 'w') as f:
        f.write("SQL Server Database Information\n")
        f.write("===============================\n")

    for _, row in tables.iterrows():
        schema = row['TABLE_SCHEMA']
        table = row['TABLE_NAME']
        schema_df, sample_data_df = fetch_table_info(engine, schema, table)
        if schema_df is not None and sample_data_df is not None:
            write_table_info(schema_df, sample_data_df, output_file, schema, table)

if __name__ == "__main__":
    main()
