# AI-Powered Inventory & Knowledge Graph Chatbots

This project consists of two terminal-based AI agents designed to interact with enterprise data. One queries a relational SQLite database (Inventory Bot), and the other manages a Neo4j graph database (Knowledge Graph Agent).

## 1. Inventory Chatbot (SQL)
An AI agent built with LangGraph that translates natural language into SQLite queries. It features a self-correction loop that automatically fixes syntactically incorrect SQL queries.

### Features
- **Natural Language to SQL**: Converts questions about assets and vendors into executable code.
- **Business Rule Enforcement**: Defaults to "Active" records only.
- **Self-Correction**: An AI node detects execution errors and regenerates the query.
- **Chitchat Recognition**: Handles greetings without querying the database.

## 2. Knowledge Graph Agent (Neo4j)
A CRUD-capable agent that allows users to manage facts within a graph database using natural language commands.

### Features
- **Intent Classification**: Identifies if the user wants to add, inquire, edit, or delete data.
- **Cypher Translation**: Automatically generates and executes Cypher queries.
- **Natural Synthesis**: Provides human-readable summaries of database actions.

## Installation & Setup

### Prerequisites
- Python 3.10+
- SQLite3
- Neo4j Database (Local or AuraDB)

### 1. Clone the Repository
```bash
git clone https://github.com/MalakHisham121/AI--powered-Chatbots.git
cd AI--inventory-Chatbot