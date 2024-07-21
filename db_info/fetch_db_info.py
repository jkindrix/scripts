import pyodbc
import pandas as pd
import logging
import sys
import argparse
import configparser
from sqlalchemy import create_engine
import random

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
            f.write(f"\n\nSchema for table {schema}.{table}:\n")
            schema_df.to_csv(f, index=False)
            f.write(f"\n\nSample data for table {schema}.{table}:\n")
            sample_data_df.to_csv(f, index=False)
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
        f.write("")

    for _, row in tables.iterrows():
        schema = row['TABLE_SCHEMA']
        table = row['TABLE_NAME']
        schema_df, sample_data_df = fetch_table_info(engine, schema, table)
        if schema_df is not None and sample_data_df is not None:
            write_table_info(schema_df, sample_data_df, output_file, schema, table)

if __name__ == "__main__":
    main()
