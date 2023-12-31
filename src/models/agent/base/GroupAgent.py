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
"""GroupAgent Class."""

from BaseAgent import BaseAgent, Category

class GroupAgent(BaseAgent):
    def __init__(self, mission: str):
        super().__init__(Category.GROUP, mission)

    def execute(self, input: str, description: str):
        # TODO: Implement this method
        pass
