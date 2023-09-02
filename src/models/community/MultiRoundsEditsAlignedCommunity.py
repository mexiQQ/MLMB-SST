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

from .base.HierarchicalCommunity import HierarchicalCommunity
from models.agent.PersonGPTAgent import PersonGPTAgent
from models.records.MultiRoundsRecord import MultiRoundsRecord
from copy import deepcopy

class MultiRoundsEditsAlignedCommunity(HierarchicalCommunity):
    def __init__(self, purpose: str, community_name: str, compacity:int=8, instruction_prompts=None):
        super().__init__(purpose, community_name, compacity=compacity)
        self.instruction_prompts = [
            "[Delete]: Review the following paragraph and **remove any words or phrases** that are ##clearly offensive or inappropriate##.",
            "[Replace]: Review the following paragraph and **replace any words or phrases** that ##may be seen as insensitive or not fully aligned with positive human values## with more suitable alternatives.",
            "[Insert]: For the following paragraph, **identify any gaps** ##where adding a word or phrase might make the message more inclusive or respectful##, and **insert** appropriate words or phrases as needed.",
            "[Swap]: Prompt: Read the following paragraph. If you find ##any instances where swapping the order of words/sentences or rephrasing can make the message more in line with human values##, please **make those adjustments.**",
            "[Clarify]: Look at the following paragraph. If ##any statements are ambiguous or might be misinterpreted##, **reword them** to make the intended meaning clearer and more aligned with human values."
            "[Highlight]: Read through the paragraph. **Highlight** ##any sections that stand out as particularly virtuous or promoting positive values##. Also, indicate any areas that might still need reconsideration or fine-tuning."
            "[Feedback Loop]: Based on the edited content, **suggest** ##potential areas for improvement or topics that might benefit from deeper exploration to ensure alignment with human values.##"
        ]

    def save_revise_record(self, from_agent_id:str, to_agent_id:str, query:str, response:str):
        record = MultiRoundsRecord(
            from_agent_id=from_agent_id, 
            to_agent_id=to_agent_id, 
            query=query, 
            response=response)
        record.save()

    def decorate_prompt_for_drat_reponse(
        self,
        agent: PersonGPTAgent,
        question: str
    ):
        query = (
            "\nThe query and main instruction are provided below. In crafting your response, rely on your vast knowledge without over-tailoring it to be overtly positive, as this is an initial draft. Although this draft might not fully align with human values from the outset, it will be iteratively refined based on feedback from other agents in the future steps.",
            f"\n<QUERY>: {question}\n",
            f"\n<MAIN INSTRUCTION>: Draw the answer from your inherent understanding and values for this query."
            f"\n<ANSWER>:"
        )
        return query 
    
    def decorate_prompt_for_next_level(
        self,
        agent: PersonGPTAgent,
        question: str,
        answers: list,
        level: int = 0,
    ):
        assert level < self.compacity, "Out of compasity"
        query = (
            "\nThe query, most recent answer, and primary instruction are provided below. When crafting your response, please adhere strictly to the requested edit step and avoid adding any extras. We have a refined iterative process in place that gradually aligns the answer with previous content. Any extra steps may compromise our original purpose.\n",
            f"\n<QUERY>: {question}\n",
            f"\n<LATEST ANSWER>: {answers[-1]}\n",
            f"\n<MAIN INSTRUCTION>: {self.instruction_prompts[level]}"
            f"\n<Note>: Please pay attention to the content in the instructions highlighted with **sth** (indicating edit action) and ##sth## (indicating target)."
        )

        query += (
            "\n\n<Revised Answer>:",
        )
        return query
    
    def envolute(self, 
        questions: list
    ):
        for question in questions:
            cur_agent = self.graph_space[0]
            print("--------------------------")
            print("---------agent------------")
            print(cur_agent)
            draft_query = self.decorate_prompt_for_drat_reponse(
                cur_agent,
                question
            )
            draft_response = cur_agent.execute(draft_query)

            responses = [draft_response]
            for i in range(1, self.compacity):
                next_level_agent = self.graph_space[i]
                next_level_query = self.decorate_prompt_for_next_level(
                    agent=next_level_agent,
                    question=question,
                    answers=responses,
                    level=i-1
                )

                if i == self.compacity - 1: # Feedback loop edit action
                    response = next_level_agent.execute(
                        next_level_query,
                        for_feedback=True
                    ) 
                else:
                    response = next_level_agent.execute(
                        next_level_query,
                    ) 

                responses.append(response)
                
            for i in range(len(responses)):
                print(f"Question: {question}")
                print(f"{i}th answer:\n{responses[i]}\n")
            print("--------------------------")
            print("--------------------------\n\n")