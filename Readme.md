
# MLMB-SST

## Multi-Language-Model-Based Social Simulation Tool

The Multi-Language-Model-Based Social Simulation, or MLMB-SS, involves social simulations rooted in artificial intelligence (AI) agents, specifically utilizing large language models (LLMs) in natural language processing. It represents a scientific discipline focused on the simulation of social phenomena through the use of computer-based multi-agent models.

In the MLMB-SS platform, individuals or groups are symbolized by AI agents, which are built upon LLMs. This provides an innovative means of studying and simulating social interactions and behaviors. The MLMB-SS tool blends elements of social science, artificial intelligence, and network simulation, making it a multidisciplinary platform for advanced computational social science.

<!-- ![image info](./assets/logo.jpg) -->

<img src="./assets/logo.jpg" alt= “” width="auto" height="400px">


## Code Tree

<div style="font-size: 0.8em;">

```python
├── src
│   ├── build_database.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── agent
│   │   │   ├── PersonClaudeAgent.py
│   │   │   ├── PersonGPTAgent.py
│   │   │   ├── PersonLLamaAgent.py
│   │   │   ├── __init__.py
│   │   │   └── base
│   │   │       ├── BaseAgent.py
│   │   │       ├── GroupAgent.py
│   │   │       ├── PersonAgent.py
│   │   │       ├── __init__.py
│   │   ├── community
│   │   │   ├── MultiRoundsSocialAlignedCommuity.py
│   │   │   ├── __init__.py
│   │   │   └── base
│   │   │       ├── BaseCommunity.py
│   │   │       ├── GrideCommunity.py
│   │   │       ├── HierarchicalCommunity.py
│   │   │       ├── __init__.py
│   │   └── records
│   │       ├── MultiRoundsRecord.py
│   │       └── base
│   │           ├── BaseRecord.py
│   └── tools
│       ├── __init__.py
│       ├── claude_connector.py
│       ├── data_connector.py
│       ├── db_connector.py
│       ├── gpt_connector.py
│       ├── llama_connector.py
│       └── misc_utils.py
└── structure.txt
```
</div>

## UML Design

![image info](./assets/uml.png)

## Persistence Design

The persistence design of the this simulation tool revolves around two databases: MySQL and Neo4j. Each type of database serves a different purpose.

- Neo4j: This is a graph database used to store and manage the data of BaseAgent objects and the relationships between them. Each BaseAgent is represented as a node in the graph, and the relationships between agents are represented as edges. The Community class is responsible for creating and managing these nodes and relationships. It provides methods to add agents (nodes) to the database, create relationships (edges) between them, and query the graph to find other agents within a given distance. Each community has its own graph (database) in Neo4j.

- MySQL: This is a relational database used to store and manage BaseRecord objects. Each BaseRecord represents a record of a query and its response, along with the IDs of the agents involved. The BaseRecord class provides methods to create, retrieve, search, and delete records in the MySQL database.

This persistence design allows you to take advantage of the strengths of both graph and relational databases. The graph database is used to manage the complex relationships between agents, which can be queried efficiently using Cypher, the query language for Neo4j. On the other hand, the relational database is used to manage the records, which have a simple structure and can be managed efficiently using SQL.

The design also follows the Single Responsibility Principle, with each class having a clear and distinct responsibility. The BaseAgent class represents an agent and its properties, the BaseRecord class manages the records and their persistence in MySQL, and the Community class manages the community of agents and their persistence in Neo4j.

## Requirement

- neo4j
- mysql
- requirement.txt
- openai api support

## Use

To be continued.

## Example

```
bash run.sh
```

## Licence

Apache License, Version 2.0

Copyright (c) 2022 Stable Alignment contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.





