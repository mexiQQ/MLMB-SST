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
"""Agent Class."""

from neo4j import GraphDatabase, Driver
from enum import Enum
import uuid
import time
from tools.db_connector import mysql_drive, neo4j_driver

class Category(Enum):
    PERSON = "person"
    GROUP = "group"
    MACHINE = "machine"
    TOOL = "tool"

class BaseAgent:
    def __init__(self, category:Category, mission:str, model_name:str):
        self.agent_id = str(uuid.uuid4())
        self.category = category
        self.mission = mission
        self.model_name = model_name
        self.records = []
        self.temp_memory = ""

    @classmethod
    def from_dict(cls, data: dict):
        agent = cls(Category(data['category']), data['mission'], data['model_name'])
        agent.agent_id = data['id']
        return agent
    
    def execute(self, input: str, description: str=None):
        raise NotImplementedError("This method should be implemented in child class")

    # def add_record(self, to_agent_id: str, query: str, response: str):
    #     record = {
    #         "id": str(uuid.uuid4()),
    #         "from": self.agent_id,
    #         "to": to_agent_id,
    #         "query": query,
    #         "response": response,
    #         "create_time": int(time.time()),
    #         "update_time": int(time.time())
    #     }
    #     self.records.append(record)
    #     self.save_record_to_mysql(mysql_drive, record)

    # def save_record_to_mysql(self, record: dict):
    #     query = "INSERT INTO records (id, from_agent_id, to_agent_id, query, response, create_time, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    #     values = (record["id"], record["from"], record["to"], record["query"], record["response"], record["create_time"], record["update_time"])
    #     mysql_drive.execute_query(query, values)

    def __repr__(self) -> str:
        return f"Agent: {self.agent_id}, Category: {self.category}, Model: {self.model_name}"