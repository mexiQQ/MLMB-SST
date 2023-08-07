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
"""Community Class."""

import uuid
from tools.db_connector import neo4j_driver
from models.agent.base.BaseAgent import BaseAgent

class BaseCommunity:
    def __init__(self, purpose:str, community_name:str):
        self.purpose = purpose
        self.community_name = community_name 
        self.community_id = str(uuid.uuid4())
        # self._create_database()

    def add_directed_relationship(self, from_agent_id: str, to_agent_id: str, relationship_type: str, weight: int):
        with neo4j_driver.session(database=self.community_name) as session:
            session.run("""
                MATCH (a:Agent),(b:Agent)
                WHERE a.id = $from_agent_id AND b.id = $to_agent_id
                MERGE (a)-[r:RELATIONSHIP { type: $relationship_type, weight: $weight }]->(b)
                """, 
                from_agent_id=from_agent_id, to_agent_id=to_agent_id, relationship_type=relationship_type, weight=weight)

    def add_undirected_relationship(self, agent_id_1: str, agent_id_2: str, relationship_type: str, weight: int):
        with neo4j_driver.session(database=self.community_name) as session:
            session.run("""
                MATCH (a:Agent),(b:Agent)
                WHERE a.id = $agent_id_1 AND b.id = $agent_id_2
                MERGE (a)-[r:RELATIONSHIP { type: $relationship_type, weight: $weight }]->(b)
                MERGE (b)-[r2:RELATIONSHIP { type: $relationship_type, weight: $weight }]->(a)
                """, 
                agent_id_1=agent_id_1, agent_id_2=agent_id_2, relationship_type=relationship_type, weight=weight)

    def _create_database(self):
        with neo4j_driver.session(database="system") as session:
            session.run("CREATE DATABASE $name IF NOT EXISTS", name=self.community_name)

    def add_agent(self, agent: BaseAgent):
        with neo4j_driver.session(database=self.community_name) as session:
            session.run("MERGE (a:Agent {id: $id, category: $category, mission: $mission, model_name: $model})",
                        id=agent.agent_id, category=agent.category.value, mission=agent.mission, model=agent.model_name)
            
    def get_agent(self, agent_id: str):
        with neo4j_driver.session(database=self.community_name) as session:
            result = session.run("MATCH (a:Agent {id: $id}) RETURN a", id=agent_id)
            return result.single()[0] if result else None

    def agent_exists(self, agent_id: str):
        with neo4j_driver.session(database=self.community_name) as session:
            result = session.run("RETURN EXISTS((:Agent {id: $id}))", id=agent_id)
            return result.single()[0] if result else False

    def delete_agent(self, agent_id: str):
        with neo4j_driver.session(database=self.community_name) as session:
            session.run("MATCH (a:Agent {id: $id}) DETACH DELETE a", id=agent_id)

    def get_agents_within_distance(self, agent_id: str, distance: int, relationship_type=None, direction=None):
        direction_clause = "->" if direction == "outgoing" else "<-" if direction == "incoming" else "-"
        type_clause = f":{relationship_type}" if relationship_type else ""
        with neo4j_driver.session(database=self.community_name) as session:
            query = f"""
                MATCH (a:Agent){direction_clause}[{type_clause}*..{distance}]-(b:Agent)
                WHERE a.id = $agent_id AND a <> b
                RETURN DISTINCT b
                """
            result = session.run(query, agent_id=agent_id)
            return [record['b'] for record in result]
        
    def count_nodes(self):
        with neo4j_driver.session(database=self.community_name) as session:
            result = session.run("MATCH (a:Agent) RETURN count(a)")
            return result.single()[0]

    def count_edges(self):
        with neo4j_driver.session(database=self.community_name) as session:
            result = session.run("MATCH ()-[r:RELATIONSHIP]->() RETURN count(r)")
            return result.single()[0]

    def envolute():
        raise NotImplementedError("This method should be implemented in child class")
        