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

def create_database_and_table(host: str, user: str, password: str):
    # Connect to the MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS social_sim_db")

    # Connect to the new database
    conn.close()  # Close the old connection first
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="social_sim_db"
    )
    cursor = conn.cursor()

    # Create agent_records table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS agent_records ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "agent_id VARCHAR(255), "
        "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        "update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, "
        "query TEXT, "
        "response TEXT"
    ")"
    )

    # Create agents table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS agents ("
        "agent_id VARCHAR(255) PRIMARY KEY, "
        "category VARCHAR(255), "
        "mission TEXT, "
        "relations TEXT, "
        "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        "update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ")"
    )

    # Close the connection
    conn.close()

# Use the function
create_database_and_table("localhost", "root", "")
