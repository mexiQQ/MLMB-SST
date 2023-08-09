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

from .base.PersonAgent import PersonAgent
from tools.gpt_connector import call_gpt

class PersonGPTAgent(PersonAgent):
    def __init__(self, mission: str, model_name: str):
        super().__init__(mission, model_name)        

    @classmethod
    def from_dict(cls, data: dict):
        agent = cls(data['mission'], data['model_name'])
        agent.agent_id = data['id']
        return agent
    
    def decorate_input(self, input: str, description:str):
        return input

    def execute(self, query: str, for_feedback: bool=False, description: str=None):
        input = self.decorate_input(query, description)
        if for_feedback:
            return call_gpt(self.model_name, input, is_central=False)
        else:
            return call_gpt(self.model_name, input)
        
