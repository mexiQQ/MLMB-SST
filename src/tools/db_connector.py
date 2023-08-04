import atexit
import mysql.connector
import mysql.connector.pooling
import yaml

# Load database configuration from YAML file
with open("configs/db_config.yaml", 'r') as stream:
    database_config = yaml.safe_load(stream)

# Initialize the connection pool
dbconfig = {
  "database": database_config["database"],
  "user":     database_config["user"],
  "password": database_config["password"],
  "host":     database_config["host"],
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 5,
                                                      pool_reset_session = True,
                                                      **dbconfig)

# Function to get connection from the pool
def get_connection():
    return cnxpool.get_connection()

# Function to close all connections
def close_all_connections():
    cnxpool._remove_connections()
