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
        super().__init__(purpose, compacity=compacity)
        self.community_name = community_name
        self.instruction_prompts = [
            "[Delete]: Review the latest round answer and **remove any words or phrases** that are ##clearly offensive or inappropriate with positive human value##.",
            "[Replace]: Review the latest round answer and **replace any words or phrases** that ##may be seen as insensitive or not fully aligned with positive human values## with more suitable alternatives.",
            "[Insert]: For the latest round answer, **identify any gaps** ##where adding a word or phrase might make the message more inclusive or respectful##, and **insert** appropriate words or phrases as needed.",
            "[Swap]: Prompt: Read the latest round answer. If you find ##any instances where swapping the order of words/sentences or rephrasing can make the message more in line with human values##, please **make those adjustments.**",
            "[Clarify]: Look at the latest round answer. If ##any statements are ambiguous or might be misinterpreted##, **reword them** to make the intended meaning clearer and more aligned with human values.",
            "[Highlight]: Read through the latest round answer. **Highlight** ##any sections that stand out as particularly virtuous or promoting positive values##. Also, indicate any areas that might still need reconsideration or fine-tuning.",
            "[Feedback Loop]: Based on the edited content, **suggest** ##potential areas for improvement or topics that might benefit from deeper exploration to ensure alignment with human values,## and make those adjustments directly within the last round answer."
        ]

        self.instruction_prompts = [
            "[Delete]: Review the latest round answer and remove any words or phrases that are clearly offensive or inappropriate with positive human value.",
            "[Replace]: Review the latest round answer and replace any words or phrases that may be seen as insensitive or not fully aligned with positive human values with more suitable alternatives.",
            "[Insert]: For the latest round answer, identify any gaps where adding a word or phrase might make the message more inclusive or respectful, and insert appropriate words or phrases as needed.",
            "[Swap]: Prompt: Read the latest round answer. If you find any instances where swapping the order of words/sentences or rephrasing can make the message more in line with human values, please make those adjustments.",
            "[Clarify]: Look at the latest round answer. If any statements are ambiguous or might be misinterpreted, reword them to make the intended meaning clearer and more aligned with human values.",
            "[Highlight]: Read through the latest round answer. Highlight any sections that stand out as particularly virtuous or promoting positive values. Also, indicate any areas that might still need reconsideration or fine-tuning.",
            "[Feedback Loop]: Based on the edited content, suggest potential areas for improvement or topics that might benefit from deeper exploration to ensure alignment with human values and make those adjustments directly within the last round answer.",
        ] 

        # self.instruction_prompts = [
        #     "Please review the latest round answer and explicitly delete any words or phrases that come across as offensive or inappropriate in light of positive human values.",
        #     "Thank you for your previous edits. Now, review the adjusted the latest round answer and replace any words or phrases that may seem insensitive or not entirely in sync with positive human values. Please substitute them with more suitable alternatives.",
        #     "Thank you for refining the text. As you review the latest round answer again, identify areas where adding a word or phrase could make the message more inclusive or respectful. Insert appropriate words or phrases where needed.",
        #     "You're doing great. Let's further enhance the content. If you find instances in the latest round answer where changing the order of words/sentences or rephrasing them can reflect human values better, please make those adjustments.",
        #     "Now, let's focus on clarity. Examine the latest round answer and reword any statements that may be ambiguous or easily misinterpreted, ensuring the meaning is clear and aligns with positive human values.",
        #     "Let's identify the strengths and areas of concern. Highlight sections of the latest round answer that promote positive values exceptionally well. Also, underline any areas that might need further reconsideration or adjustments.",
        #     "Based on the edits made so far, please suggest areas in the latest round answer that might benefit from further improvement or deeper exploration to ensure they resonate with human values."
        # ]

        # self.instruction_prompts = [
        #     "[Explicitness in Deleting]: Please review the latest round answer and explicitly delete any words or phrases that come across as offensive or inappropriate in light of positive human values.",
        #     "[Replacement with Context]: Thank you for your previous edits. Now, review the adjusted the latest round answer and replace any words or phrases that may seem insensitive or not entirely in sync with positive human values. Please substitute them with more suitable alternatives.",
        #     "[Insertion for Inclusivity]: Thank you for refining the text. As you review the latest round answer again, identify areas where adding a word or phrase could make the message more inclusive or respectful. Insert appropriate words or phrases where needed.",
        #     "[Order and Rephrasing]: You're doing great. Let's further enhance the content. If you find instances in the latest round answer where changing the order of words/sentences or rephrasing them can reflect human values better, please make those adjustments.",
        #     "[Clarification for Ambiguity]: Now, let's focus on clarity. Examine the latest round answer and reword any statements that may be ambiguous or easily misinterpreted, ensuring the meaning is clear and aligns with positive human values.",
        #     "[Highlighting Virtues and Concerns]: Let's identify the strengths and areas of concern. Highlight sections of the latest round answer that promote positive values exceptionally well. Also, underline any areas that might need further reconsideration or adjustments.",
        #     "[Feedback Loop]: Based on the edits made so far, please suggest areas in the latest round answer that might benefit from further improvement or deeper exploration to ensure they resonate with human values."
        # ]

        # self.instruction_prompts = [
        #     "[Delete]: While keeping the original question in mind, review the latest round answer and remove any words or phrases that are clearly offensive or inappropriate.",
        #     "[Replace]: Reflecting on the core intent of the original question, identify any words or phrases in the latest round answer that may seem insensitive. Replace them with alternatives that are more aligned with positive human values.",
        #     "[Insert]: Ensure the revised answer remains relevant to the initial query. Identify areas where adding words or phrases would make the message more inclusive or respectful without deviating from the main topic.",
        #     "[Swap]: With the original question as a reference, rearrange or rephrase portions of the latest round answer to better convey the message in line with human values.",
        #     "[Clarify]: Stay true to the essence of the original question. If there are ambiguous statements in the latest round answer, reword them for clarity and positive human alignment.",
        #     "[Highlight]: Examine the latest round answer. Mark sections that are particularly aligned with positive values and indicate any areas that might drift from the initial question's focus or need fine-tuning.",
        #     "[Feedback Loop]: Considering the edits made and the original question, suggest areas in the latest round answer that can be improved to ensure they are both aligned with human values and relevant to the initial query."
        # ]


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
        assert level < self.compacity - 1, "Out of compasity"
        query = (
            "\nThe query, most recent answer, and primary instruction are provided below. When crafting your response, please adhere strictly to the main instruction and avoid adding any extra steps.",
            f"\n<QUERY>: {question}",
            f"\n<LATEST ANSWER>: {answers[-1]}",
            f"\n<MAIN INSTRUCTION>: {self.instruction_prompts[level]}"
            # f"\n<Note>: Please pay attention to the content in the instructions highlighted with **sth** (indicating edit action) and ##sth## (indicating target)."
        )

        query += (
            f"\n\n<PREVIOUS INTERACTION ROUND 0>\n",
            f"<Draf_ANS>: {answers[0]}\n"
        )
        
        for i in range(1, len(answers)):
            query += (
                f"\n<PREVIOUS INTERACTION ROUND {i}>\n",
                f"<PREVIOUS INTERACTION>: {self.instruction_prompts[i-1]}\n" 
                f"<PREV_ANS>: {answers[i]}\n"
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
                print(next_level_agent)
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
            


            print("--------------------------") 
            print(f"Question: {question}")
            for i in range(len(responses)):
                print(f"{i}th answer:\n{responses[i]}\n")
            print("--------------------------")
            print("--------------------------\n\n")