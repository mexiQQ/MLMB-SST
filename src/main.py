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
from models.community.MultiRoundsSocialAlignedCommuity import MultiRoundsSocialAlignedCommuity

if __name__=="__main__":
    print("--------------------")
    print("--Start simulation--")
    print("--------------------")

    community_size = (5, 5)
    community = MultiRoundsSocialAlignedCommuity(
        purpose=(
            "As a collaborative community of diverse language models with varying alignment levels, we utilize our collective capabilities to gradually generate aligned text. Our aim is to facilitate a broad spectrum of discussions and dialogues, learning and growing from each other's perspectives and knowledge bases.",
            "Your interaction with us involves a series of information exchanges with different language models. Starting with models that have a lower level of alignment, we gradually move towards higher-aligned models. This process ensures a multi-faceted approach to your queries, providing comprehensive and nuanced responses that balance diverse perspectives.",
            "We look forward to your questions, thoughts, and ideas, and are excited to assist you in exploring the depth and breadth of your inquiries. Please ask your question or start a discussion below."),
        community_name="neo4j",
        width=community_size[0],
        height=community_size[1]
    )

    model_list = [
        # ["Llama_v1"],
        ["text-davinci-001"],
        ["text-davinci-001", "text-davinci-002", "text-davinci-003"], 
        ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"],
        ["gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"], 
        # ["gpt-4", "gpt-4-0314", "Llama_v2"]
    ]
    probability_distribution = [0.5, 0.3, 0.1, 0.1]
    MISSION = "As an advanced language model, you are to act as a virtual agent in a simulated society. Draw from your extensive knowledge and understanding to respond to questions and provide commentary. There is no need to tailor your responses to be overly positive; authenticity and accuracy are key. Our aim is to generate gradually aligned content. Remember to use your inherent values and preferences in forming responses. Let's get started."

    for i in range(community_size[0]):
        for j in range(community_size[1]):
            if community.count_nodes() % 10 == 0:
                print(f"successfully create {community.count_nodes()} agents")
            selected_group = random.choices(model_list, weights=probability_distribution, k=1)[0]
            selected_model = random.choice(selected_group)
            agent = PersonGPTAgent(
                mission=MISSION,
                model_name=selected_model
            ) 
            community.add_agent_with_location(agent=agent, i=i, j=j)

    questions = get_query_questions("hh-rlhf", count=1)

    community.envolute(
        multiple_rounds=3,
        is_target_agent=lambda a: isinstance(a, PersonGPTAgent) and a.model_name == "text-davinci-001",
        questions=questions
    )

