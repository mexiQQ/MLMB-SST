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

from BaseCommunity import BaseCommunity
from models.agent.base import BaseAgent

class HierarchicalCommunity(BaseCommunity):
    def __init__(self, purpose: str, compacity=3):
        self.graph = [] 
        self.compacity = compacity

    def _define_community_space(self):
        self.graph_space = [None] * self.compacity

    def add_agent_with_location(self, agent: BaseAgent, index=0):
        if index < 0 or index > self.compacity-1:
            assert False, 'Insert location is out of campasity of community'

        self.add_agent(agent=agent)
        if not self.graph_space[index]]:
            self.graph_space[index] = agent
        else:
            assert False, f"Agent {self.graph_space[index].agent_id} \
                  has existed in community {self.community_id} at hierarchical location {index}"
