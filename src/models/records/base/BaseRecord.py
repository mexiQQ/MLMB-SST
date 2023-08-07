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

import uuid
import time
from tools.db_connector import mysql_drive 

class BaseRecord:
    def __init__(self, from_agent_id: str, to_agent_id: str, query: str, response: str):
        self.record_id = str(uuid.uuid4())
        self.from_agent_id = from_agent_id
        self.to_agent_id = to_agent_id
        self.query = query
        self.response = response
        self.create_time = int(time.time())
        self.update_time = self.create_time

    @classmethod
    def from_dict(cls, data: dict):
        record = cls(data['from_agent_id'], data['to_agent_id'], data['query'], data['response'])
        record.record_id = data['id']
        record.create_time = data['create_time']
        record.update_time = data['update_time']
        return record

    def save(self):
        query = "INSERT INTO records (id, from_agent_id, to_agent_id, query, response, create_time, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.record_id, self.from_agent_id, self.to_agent_id, self.query, self.response, self.create_time, self.update_time)
        self.mysql_drive.execute_query(query, values)

    @staticmethod
    def get_record_with_record_id(record_id: str):
        query = "SELECT * FROM records WHERE id = %s"
        values = (record_id,)
        result = mysql_drive.execute_query(query, values)
        return BaseRecord.from_dict(result[0]) if result else None

    @staticmethod
    def search_records_with_agent_id(agent_id: str, to=False):
        if to:
            query = "SELECT * FROM records WHERE to_agent_id = %s"
        else:
            query = "SELECT * FROM records WHERE from_agent_id = %s"
        values = (agent_id)
        result = mysql_drive.execute_query(query, values)
        return [BaseRecord.from_dict(record) for record in result]

    @staticmethod
    def delete_record(record_id: str):
        query = "DELETE FROM records WHERE id = %s"
        values = (record_id,)
        mysql_drive.execute_query(query, values)
