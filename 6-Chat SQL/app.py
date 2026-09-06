# Import Streamlit for creating the web application
import streamlit as st

# Import Path to locate the SQLite database file
from pathlib import Path

# Import SQL Agent from LangChain
from langchain_community.agent_toolkits import create_sql_agent

# Import SQLDatabase to connect LangChain with SQL databases
from langchain_community.utilities import SQLDatabase

# Import Streamlit callback handler for showing agent activity
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Import SQL Database Toolkit
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# Import SQLAlchemy engine for database connections
from sqlalchemy import create_engine

# Import SQLite for connecting to the local SQLite database
import sqlite3

# Import quote_plus for safely handling Oracle username and password
from urllib.parse import quote_plus

# Import Groq LLM
from langchain_groq import ChatGroq

# Import dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Import os to read environment variables
import os


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

# Load variables from the .env file
load_dotenv()


# --------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LangChain: Chat with SQL DB",
    page_icon="🦜"
)

# Display the title of the application
st.title("🦜 LangChain: Chat with SQL DB")


# --------------------------------------------------
# DATABASE CONSTANTS
# --------------------------------------------------

# Constant for local SQLite database
LOCALDB = "USE_LOCALDB"

# Constant for Oracle database
MYORACLE = "USE_ORACLE"


# --------------------------------------------------
# DATABASE OPTIONS
# --------------------------------------------------

# Options displayed in the sidebar
radio_opt = [
    "Use SQLLITE 3 Database- ecommerce.db",
    "Connect to your Oracle Database"
]


# Create a radio button for selecting the database
selected_opt = st.sidebar.radio(
    label="Choose the DB which you want to chat",
    options=radio_opt
)


# --------------------------------------------------
# ORACLE DATABASE CONNECTION DETAILS
# --------------------------------------------------

# Check if the user selects the Oracle database option
if radio_opt.index(selected_opt) == 1:

    # Set database URI to Oracle
    db_uri = MYORACLE

    # Get Oracle host name from the user
    oracle_host = st.sidebar.text_input(
        "Provide ORACLE Host name"
    )

    # Get Oracle username from the user
    oracle_user = st.sidebar.text_input(
        "ORACLE User"
    )

    # Get Oracle password from the user
    oracle_password = st.sidebar.text_input(
        "ORACLE password",
        type="password"
    )

    # Get Oracle database/service name from the user
    oracle_db = st.sidebar.text_input(
        "Oracle database"
    )


# --------------------------------------------------
# SQLITE DATABASE SELECTION
# --------------------------------------------------

else:

    # Use local SQLite database
    db_uri = LOCALDB


# --------------------------------------------------
# GROQ API KEY
# --------------------------------------------------

# Get Groq API key from the .env file
api_key = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# DATABASE VALIDATION
# --------------------------------------------------

# Check if database URI is available
if not db_uri:
    st.info("Please enter the database information and uri")
    st.stop()


# --------------------------------------------------
# GROQ API KEY VALIDATION
# --------------------------------------------------

# Check if Groq API key is available in .env
if not api_key:
    st.info("Please add the GROQ_API_KEY to the .env file")


# --------------------------------------------------
# LLM MODEL
# --------------------------------------------------

# Initially keep LLM as None
llm = None

# Create Groq LLM only when API key is available
if api_key:

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="openai/gpt-oss-20b",
        streaming=True
    )


# --------------------------------------------------
# DATABASE CONFIGURATION FUNCTION
# --------------------------------------------------

# Cache the database connection for 2 hours
@st.cache_resource(ttl="2h")
def configure_db(
    db_uri,
    oracle_host=None,
    oracle_user="None",
    oracle_password="None",
    oracle_db="None"
):

    # ----------------------------------------------
    # LOCAL SQLITE DATABASE
    # ----------------------------------------------

    # Check if the selected database is SQLite
    if db_uri == LOCALDB:

        # Get the path of ecommerce.db
        db_filepath = (
            Path(__file__).parent / "ecommerce.db"
        ).absolute()

        # Print database file path
        print(db_filepath)

        # Return SQLite database connection to LangChain
        return SQLDatabase(
            create_engine(
                f"sqlite:///{db_filepath}"
            )
        )


    # ----------------------------------------------
    # ORACLE 12C DATABASE
    # ----------------------------------------------

    # Check if the selected database is Oracle
    elif db_uri == MYORACLE:

        # Check whether all Oracle connection details are provided
        if not (
            oracle_host
            and oracle_user
            and oracle_password
            and oracle_db
        ):

            # Display an error message
            st.error(
                "Please provide all ORACLE connection details."
            )

            # Stop the Streamlit application
            st.stop()


        # Safely encode Oracle username
        encoded_user = quote_plus(
            oracle_user
        )

        # Safely encode Oracle password
        encoded_password = quote_plus(
            oracle_password
        )


        # Create Oracle database connection
        # exclude_tablespaces is an SQLAlchemy Oracle engine option
        return SQLDatabase(
            create_engine(
                f"oracle+oracledb://"
                f"{encoded_user}:"
                f"{encoded_password}"
                f"@{oracle_host}:1521/"
                f"?service_name={oracle_db}",

                # Include tables from SYSTEM tablespace
                # and exclude none of the tablespaces
                exclude_tablespaces=[]
            ),

            # Use the Oracle user's schema
            schema=oracle_user.upper()
        )


# --------------------------------------------------
# CONNECT TO THE SELECTED DATABASE
# --------------------------------------------------

# Check if Oracle database is selected
if db_uri == MYORACLE:

    # Configure Oracle database connection
    db = configure_db(
        db_uri,
        oracle_host,
        oracle_user,
        oracle_password,
        oracle_db
    )


# If SQLite is selected
else:

    # Configure SQLite database connection
    db = configure_db(db_uri)


# --------------------------------------------------
# CREATE SQL TOOLKIT AND SQL AGENT
# --------------------------------------------------

# Initially keep agent as None
agent = None

# Create toolkit and agent only when Groq API key is available
if llm is not None:

    # Create SQL Database Toolkit
    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )

    # Create SQL Agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="tool-calling"
    )


# --------------------------------------------------
# CREATE MESSAGE HISTORY
# --------------------------------------------------

if "messages" not in st.session_state or st.sidebar.button(
    "Clear message history"
):

    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "How can I help you?"
        }
    ]


# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------

for msg in st.session_state.messages:

    st.chat_message(
        msg["role"]
    ).write(
        msg["content"]
    )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

use_query = st.chat_input(
    placeholder="Ask anything from the database"
)


# --------------------------------------------------
# PROCESS USER QUERY
# --------------------------------------------------

if use_query:

    # Add user question to chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": use_query
        }
    )

    # Display user question
    st.chat_message(
        "user"
    ).write(
        use_query
    )


    # Generate assistant response
    with st.chat_message("assistant"):

        # Check whether Groq API key is available
        if agent is None:

            response_text = (
                "Please add the GROQ_API_KEY to the .env file first."
            )

            st.write(response_text)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

        else:

            # Create Streamlit callback handler
            streamlit_callback = StreamlitCallbackHandler(
                st.container()
            )

            # Run SQL Agent
            response = agent.invoke(
                {
                    "input": use_query
                },
                {
                    "callbacks": [
                        streamlit_callback
                    ]
                }
            )

            # Get final answer
            response_text = response["output"]

            # Add assistant response to chat history
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

            # Display response
            st.write(response_text)