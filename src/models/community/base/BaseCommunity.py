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

class BaseCommunity:
    def __init__(self):
        self.graph = {}

    def add_agent(self, agent):
        self.graph[agent] = []

    def add_relationship(self, agent1, agent2):
        if agent1 not in self.graph:
            self.add_agent(agent1)
        if agent2 not in self.graph:
            self.add_agent(agent2)
        self.graph[agent1].append(agent2)
        self.graph[agent2].append(agent1)  # if the graph is undirected
