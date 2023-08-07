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


import pymysqlpool
from neo4j import GraphDatabase
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

class DbConnector:
    def __init__(self, config: dict):
        pymysqlpool.logger.setLevel(pymysqlpool.logging.DEBUG)
        self.pool = pymysqlpool.ConnectionPool(size=10, name='pool', **config)
        
    def execute_query(self, query: str, values: tuple):
        connection = self.pool.get_connection()
        try:
            with connection.cursor() as cursor:
                result_proxy = cursor.execute(query, values)
            connection.commit()
            if isinstance(result_proxy, list):
                return [dict(row) for row in result_proxy]
        finally:
            # self.pool.release(connection)
            connection.close()

mysql_drive = DbConnector(dbconfig) 
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Li19940426"))
