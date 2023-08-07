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

def get_query_questions(source: str, count: int):
    """Sample incoming questions for the conversations"""
    if source == 'hh-rlhf':
        questions = []
        path = f"data/{source}/question.txt"
        with open(path, 'r') as f:
            for line in f:
                questions.append(line.strip())

        return questions[:count if count < len(questions) else len(questions)]
    else:
        raise NotImplementedError