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

from .base.GrideCommunity import GrideCommunity

class MultiRoundsSocialAlignedCommuity(GrideCommunity):
    def __init__(self, purpose: str, community_name: str, width: int, height: int):
        super().__init__(purpose, community_name, width=width, height=height)

    def envolute(self, multiple_rounds: int, is_target_agent: callable):
        for i in range(self.width):
            for j in range(self.height):
                cur_agent = self.graph_space[i][j]
                if is_target_agent(cur_agent):
                    print("--------------------------")
                    print("---------agent------------")
                    print(cur_agent)
                    for k in range(1, multiple_rounds):
                        print("****************************")
                        neighbors_within_distance = self.get_agents_within_distance(cur_agent.agent_id, k)
                        print(f"The {k}th round interaction: {len(neighbors_within_distance)}")
                        for index in range(len(neighbors_within_distance)):
                            print(f"Neighbor {index}: {neighbors_within_distance[index]}")
                            # import pdb; pdb.set_trace()
                        print("****************************")
                    print("--------------------------")
                    print("--------------------------\n\n")
