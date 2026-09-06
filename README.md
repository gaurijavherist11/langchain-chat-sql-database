# 🦜 LangChain Chat with SQL Database

An AI-powered conversational SQL database assistant built using **LangChain, Groq, SQLite, and Oracle 12c**.

This project allows users to interact with SQL databases using natural language. Instead of writing SQL queries manually, users can ask questions in plain English and the LangChain SQL Agent generates and executes the required SQL queries.

---

## 📌 Project Overview

The application provides a chat-based interface where users can ask questions about their database using natural language.

For example:

> Show me all customers from Maharashtra.

> How many customers are there?

> Show the details of the customer from Mumbai.

The LangChain SQL Agent analyzes the question, identifies the required database tables, generates the SQL query, executes it, and returns the result in a conversational format.

---

## 🚀 Features

- 💬 Natural Language interaction with SQL databases
- 🤖 LangChain SQL Agent
- 🧠 Groq LLM integration
- 🗃️ SQLite database support
- 🏢 Oracle 12c database support
- 🔍 Automatic database table discovery
- ⚡ Automatic SQL query generation
- 📊 SQL query execution and result generation
- 🖥️ Streamlit-based user interface
- 💾 Chat message history
- 🔐 API key stored securely using `.env`

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Streamlit | Web-based user interface |
| LangChain | SQL Agent and database interaction |
| Groq | Large Language Model |
| SQLAlchemy | Database connection and management |
| SQLite | Local database |
| Oracle 12c | Enterprise database |
| Python-dotenv | Environment variable management |

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
Streamlit Chat Interface
  │
  ▼
LangChain SQL Agent
  │
  ▼
SQLDatabaseToolkit
  │
  ├───────────────┐
  ▼               ▼
SQLite          Oracle 12c
  │               │
  └───────┬───────┘
          ▼
      SQL Query
          │
          ▼
    Database Result
          │
          ▼
     AI Response
