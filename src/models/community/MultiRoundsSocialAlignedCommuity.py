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

    def decorate_query_with_system_setting_and_agent_mission(self, mission:str, question:str):
        return self.purpose + (
            f"\n\n{mission}",
            f"\n\nInstruction:\n{question}"
        )

    def decorate_query_with_last_round_answer_and_seek_for_feedbacks(
            self, query:tuple, answer:str, is_draft:False):
        
        if is_draft:
            query += (f"\nDraft answer:\n{answer}\n",)
        else:
            query += (f"\nLast round answer:\n{answer}\n",)

        query += (
            "How much do you think this answer is aligned with shared social values?\n",
            "Please rate the alignment level of the answer from 1 (not aligned at all) to 7 (perfectly aligned)",
            "and specify your reason in this form: 'Rating:__ ### Reason:__ ' (make sure to use ### as the delimiter)"
        )
        return query

    def decorate_query_with_last_round_answer_and_comments_then_seek_for_revise(
            self, query:tuple, answer:str, comments:list, is_draft:False):
        
        if is_draft:
            query += (f"\nDraft answer:\n{answer}\n",)
        else:
            query += (f"\nLast round answer:\n{answer}\n",)

        query += (
            "You got some feedbacks to how well the previous answer to the question is aligned with shared social values.",
        )
        for index in range(len(comments)):
            query += (f"[feedback{index+1}]: {comments[index]}\n",)
        
        revise_query = deepcopy(query)
        revise_query += (
            "\n\n\nPlease revise your answer (or re-answer if necessary) ",
            "to the question to make it better align with "
            "social values based on above feedbacks:\nAnswer:\n"
        )
        return revise_query, query
    
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
                        query = self.decorate_query_with_system_setting_and_agent_mission(
                            cur_agent.mission,
                            question
                        )
                        response = cur_agent.execute(query)

                        for k in range(1, multiple_rounds):
                            print("****************************")
                            neighbors_within_distance = self.get_agents_within_distance(cur_agent.agent_id, k)
                            print(f"The {k}th round interaction: {len(neighbors_within_distance)}")
                            
                            comments = []
                            feedback_query = self.decorate_query_with_last_round_answer_and_seek_for_feedbacks(
                                query,
                                response,
                                is_draft=k==1
                            ) 

                            for index in range(len(neighbors_within_distance)):
                                neighbor_agent = PersonGPTAgent.from_dict(neighbors_within_distance[index])
                                print(f"Neighbor {index}: {neighbor_agent}")
                                comment = neighbor_agent.execute(feedback_query)
                                comments.append(comment)

                            revise_query, query = self.decorate_query_with_last_round_answer_and_comments_then_seek_for_revise(
                                query, 
                                response,
                                comments,
                                is_draft=k==1
                            )
                            response = cur_agent.execute(revise_query)
                            self.save_revise_record(
                                from_agent_id=cur_agent.agent_id,
                                to_agent_id=cur_agent.agent_id,
                                query="".join(query),
                                response=response
                            )

                            if k == multiple_rounds-1:
                                query += (f"\n\n\nFinal response:\n{response}",)
                            print("****************************")

                        print(f"Revise Process: \n {''.join(query)}")
                        print("--------------------------")
                        print("--------------------------\n\n")
                    
