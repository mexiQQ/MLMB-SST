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

import json
from datetime import datetime
from enum import Enum
import uuid

from db_connector import get_connection

class Category(Enum):
    PERSON = "person"
    GROUP = "group"
    MACHINE = "machine"
    TOOL = "tool"

class BaseAgent:
    def __init__(self, category: Category, mission: str):
        self.agent_id = str(uuid.uuid4())
        self.category = category
        self.mission = mission
        self.relations = {"group": [], "peer": []}
        self.records = []

    def execute(self, input: str, description: str):
        raise NotImplementedError("This method should be implemented in child class")

    def write_to_db(self):
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Convert relations to string
        relations_str = json.dumps(self.relations)

        # Create a new agent record
        sql = (
            "INSERT INTO agents (agent_id, category, mission, relations) "
            "VALUES (%s, %s, %s, %s)"
        )
        val = (self.agent_id, self.category.value, self.mission, relations_str)
        cursor.execute(sql, val)
        conn.commit()

        # Return the connection to the pool
        conn.close()

    def fetch_records(self):
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch all records for this agent
        sql = "SELECT * FROM agent_records WHERE agent_id = %s"
        val = (self.agent_id, )
        cursor.execute(sql, val)
        self.records = cursor.fetchall()

        # Return the connection to the pool
        conn.close()

    @classmethod
    def read_from_db(cls, agent_id: str):
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch the agent record
        sql = "SELECT * FROM agents WHERE agent_id = %s"
        val = (agent_id, )
        cursor.execute(sql, val)
        agent_record = cursor.fetchone()

        if agent_record is None:
            raise ValueError(f"No agent found with ID {agent_id}")

        # Convert relations back to dictionary
        relations = json.loads(agent_record[3])

        # Create a new agent object
        agent = cls(Category(agent_record[1]), agent_record[2])
        agent.agent_id = agent_record[0]
        agent.relations = relations

        # Fetch the agent's records
        agent.fetch_records()

        # Return the connection to the pool
        conn.close()

        return agent
