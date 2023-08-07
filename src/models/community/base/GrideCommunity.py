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

from .BaseCommunity import BaseCommunity
from models.agent.base import BaseAgent

class GrideCommunity(BaseCommunity):
    def __init__(self, purpose:str, community_name: str, width: int, height: int):
        super().__init__(purpose, community_name)
        self.width = width
        self.height = height
        self._define_community_space()

    def _define_community_space(self):
        self.graph_space = [[None] * self.width for _ in range(self.height)]

    def add_agent_with_location(self, agent: BaseAgent, i: int, j: int):
        self.add_agent(agent=agent)
        if not self.graph_space[i][j]:
            self.graph_space[i][j] = agent
            self._add_relations(agent, i, j)
        else:
            assert False, f"Agent {self.graph_space[i][j].agent_id} \
                  has existed in community {self.community_id} at location row:{i} column:{j}"

    def _get_neighbors(self, width: int, height: int, i: int, j: int):
        """
        Returns the top, left, bottom, right neighbors of a cell at location (i, j) in a grid of size (width x height).
        """
        neighbors = {
            "top": (i-1, j) if i > 0 else None,
            "left": (i, j-1) if j > 0 else None,
            "bottom": (i+1, j) if i < height - 1 else None,
            "right": (i, j+1) if j < width - 1 else None,
        }
        return neighbors

    def _add_relations(self, agent:BaseAgent, row: int, column: int):
        neighbors = self._get_neighbors(self.width, self.height, row, column)
        for _, location in neighbors.items():
            if location is not None:
                neibor_agent = self.graph_space[location[0]][location[1]]
                if neibor_agent:
                    self.add_undirected_relationship(
                        agent.agent_id, 
                        neibor_agent.agent_id, 
                        relationship_type="friend", weight=1)
            