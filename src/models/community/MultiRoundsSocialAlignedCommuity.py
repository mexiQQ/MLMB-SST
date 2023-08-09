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
from models.agent.PersonGPTAgent import PersonGPTAgent
from models.records.MultiRoundsRecord import MultiRoundsRecord
from copy import deepcopy

class MultiRoundsSocialAlignedCommuity(GrideCommunity):
    def __init__(self, purpose: str, community_name: str, width: int, height: int):
        super().__init__(purpose, community_name, width=width, height=height)

    def decorate_prompt_for_drat_reponse(
        self,
        agent: PersonGPTAgent,
        question: str
    ):
        query = (
            "\nPlease enter your query. In crafting your response, rely on your vast knowledge without over-tailoring it to be overtly positive, as this is an initial draft. Although this draft might not fully align with human values from the outset, it will be iteratively refined based on feedback from other agents in the future steps. Use the following format:\n",
            f"\n<QUERY>: {question}\n",
            f"\n<MAIN INSTRUCTION>: Draw the answer from your inherent understanding and values for this query."
            f"\n<Answer>:"
        )
        return query 

    def decorate_prompt_for_feedback(
        self,
        agent: PersonGPTAgent,
        question: str,
        answers: list,
        comments: list
    ):
        query += (
            "\nPlease enter query and latest response. For follow-up interactions (if exist), provided feedback on previous answers guides the agent's feedback for the latest answer. Use the following format:\n",
            f"\n<QUERY>: {question}\n",
            f"\n<LATEST ANSWER>: {answers[-1]}\n",
            f"\n<MAIN INSTRUCTION>: Considering this query and the evolution of responses, provide feedback for the latest answer:\n",
            "1. Assesses the alignment of the answer with shared human values and preferences.\n",
            "2. Highlights areas for improvement, especially in addressing the underlying reasons or motivations behind the query.\n",
            "3. Suggests potential refinements to ensure the answer is constructive, supportive, and aligns with societal values.\n",
        )

        for i in range(len(answers)-1):
            query += (
                f"\n<ROUND{i+1}>\n",
                f"<PREV_ANS>: {answers[i]}\n"
            )
            for j in range(len(comments[i])):
                if comments[i][j]:
                    query += (
                        f"<FEEDBACK_NEIGHBOR{j}>: {comments[i][j]}\n",
                    )
            query += (
                ",",
            )

        return query

    def decorate_prompt_with_feedback_for_revise(
        self,
        agent: PersonGPTAgent,
        question: str,
        answers: list,
        comments: list 
    ):
        query += (
            "\nPlease enter your query. For follow-up interactions, provided feedback on previous answers guides the agent's revisions. The feedback helps the agent better align with social values and preferences. Use the following format:\n",
            f"\n<QUERY>: {question}\n",
            f"\n<MAIN INSTRUCTION>: Use the feedback below to **significantly revise** the answer from the latest round.\n",
        )

        for i in range(len(answers)):
            query += (
                f"\n<ROUND{i+1}>\n",
                f"<PREV_ANS>: {answers[i]}\n"
            )
            for j in range(len(comments[i])):
                if comments[i][j]:
                    query += (
                        f"<FEEDBACK_NEIGHBOR{j}>: {comments[i][j]}\n",
                    )
            query += (
                ",",
            ) 
        return query
    
    def save_revise_record(self, from_agent_id:str, to_agent_id:str, query:str, response:str):
        record = MultiRoundsRecord(
            from_agent_id=from_agent_id, 
            to_agent_id=to_agent_id, 
            query=query, 
            response=response)
        record.save()

    def envolute(self, 
        multiple_rounds: int, 
        is_target_agent: callable,
        questions: list
    ):
        for question in questions:
            for i in range(self.width):
                for j in range(self.height):
                    cur_agent = self.graph_space[i][j]

                    if is_target_agent(cur_agent):
                        print("--------------------------")
                        print("---------agent------------")
                        print(cur_agent)
                        query = self.decorate_prompt_for_drat_reponse(
                            cur_agent,
                            question
                        )
                        response = cur_agent.execute(query)

                        responses = [response]
                        multi_round_coments = []

                        for k in range(1, multiple_rounds):
                            print("****************************")
                            neighbors_within_distance = self.get_agents_within_distance(cur_agent.agent_id, k)
                            print(f"The {k}th round interaction: {len(neighbors_within_distance)}")
                            
                            comments = []
                            feedback_query = self.decorate_prompt_for_feedback(
                                cur_agent,
                                question,
                                responses,
                                multi_round_coments
                            ) 

                            for index in range(len(neighbors_within_distance)):
                                neighbor_agent = PersonGPTAgent.from_dict(neighbors_within_distance[index])
                                print(f"Neighbor {index}: {neighbor_agent}")
                                comment = neighbor_agent.execute(feedback_query)
                                comments.append(comment)
                            multi_round_coments.append(comments)

                            query = self.decorate_prompt_with_feedback_for_revise(
                                cur_agent, 
                                question,
                                responses,
                                multi_round_coments
                            )
                            response = cur_agent.execute(query)
                            responses.append(response)
                            
                            self.save_revise_record(
                                from_agent_id=cur_agent.agent_id,
                                to_agent_id=cur_agent.agent_id,
                                query="".join(query),
                                response=response
                            )

                            if k == multiple_rounds-1:
                                query += (f"\n\n<FINAL ANSWER>:\n{response}",)
                            print("****************************")

                        print(f"Revise Process: \n {''.join(query)}")
                        print("--------------------------")
                        print("--------------------------\n\n")
                    
