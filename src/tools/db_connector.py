#! /usr/bin/env python3
# coding=utf-8

# Jianwei Li @NCSU-DK-LAB 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
                                                      pool_size = 10,
                                                      pool_reset_session = True,
                                                      **dbconfig)

# Function to get connection from the pool
def get_connection():
    return cnxpool.get_connection()

# Function to close all connections
def close_all_connections():
    cnxpool._remove_connections()
