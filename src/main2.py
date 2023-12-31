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

import random
from tools.data_connector import get_query_questions
from models.agent.PersonGPTAgent import PersonGPTAgent
from models.community.MultiRoundsEditsAlignedCommunity import MultiRoundsEditsAlignedCommunity

if __name__=="__main__":
    print("--------------------")
    print("--Start simulation--")
    print("--------------------")

    community_size = 8
    community = MultiRoundsEditsAlignedCommunity(
        purpose=(
            "As a collaborative community of diverse language models with varying alignment levels, we utilize our collective capabilities to gradually generate aligned text. Our aim is to facilitate a broad spectrum of discussions and dialogues, learning and growing from each other's perspectives and knowledge bases.",
            "Your interaction with us involves a series of information exchanges with different language models. Starting with models that have a lower level of alignment, we gradually move towards higher-aligned models. This process ensures a multi-faceted approach to your queries, providing comprehensive and nuanced responses that balance diverse perspectives.",
            "We look forward to your questions, thoughts, and ideas, and are excited to assist you in exploring the depth and breadth of your inquiries. Please ask your question or start a discussion below."),
        community_name="neo4j",
        compacity=community_size
    )

    model_list = [
        "text-davinci-001",
        "text-davinci-003",
        "gpt-3.5-turbo",
        "text-davinci-003",
        "gpt-3.5-turbo",
        "text-davinci-003",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k-0613",
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
        # "gpt-3.5-turbo-16k-0613", 
    ]
    MISSION = "As an advanced language model, you are to act as a virtual agent in a simulated society. Draw from your extensive knowledge and understanding to respond to questions and provide commentary. There is no need to tailor your responses to be overly positive; authenticity and accuracy are key. Our aim is to generate gradually aligned content. Remember to use your inherent values and preferences in forming responses. Let's get started."

    for i in range(community_size):
        selected_model = model_list[i]
        agent = PersonGPTAgent(
            mission=MISSION,
            model_name=selected_model
        ) 
        community.add_agent_with_location(agent=agent, index=i)

    print(f"Total number of agents: {community.count_nodes()}")
    questions = get_query_questions("hh-rlhf", count=1)

    community.envolute(
        questions=questions
    )

