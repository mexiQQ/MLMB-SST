#! /usr/bin/env python3
# coding=utf-8

# Jianwei Li @NCSU-DK-LAB 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of thge License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tools.db_connector import DbConnector, mysql_drive

def create_mysql_database(db_connector: DbConnector):
    db_connector.execute_query("CREATE TABLE IF NOT EXISTS records (id VARCHAR(255), from_agent_id VARCHAR(255), to_agent_id VARCHAR(255), query TEXT, response TEXT, create_time INT, update_time INT)", ())

def build_database():
    create_mysql_database(mysql_drive)

build_database()