import streamlit as st
import json
import os
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Path to the connection details file
CONNECTION_FILE = "connection_info.json"

# Function to save connection info to the JSON file
def save_connection_info(data):
    with open(CONNECTION_FILE, "w") as f:
        json.dump(data, f)

# Function to load connection info from the JSON file
def load_connection_info():
    if os.path.exists(CONNECTION_FILE):
        with open(CONNECTION_FILE, "r") as f:
            return json.load(f)
    else:
        return None

# Function to connect to the database using URL
def connectDatabaseFromURL(url):
    try:
        st.session_state.db = SQLDatabase.from_uri(url)
        st.success("Connected successfully via URL")
    except Exception as e:
        st.error(f"Failed to connect via URL: {e}")

# Function to generate connection URL based on database type
def get_connection_url(db_type, username, password, host, port, database):
    if db_type == "MySQL":
        return f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    elif db_type == "PostgreSQL":
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    elif db_type == "Oracle":
        return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{database}"
    else:
        return None

# Function to connect to the database using separate connection details
def connectDatabase(db_type, username, port, host, password, database):
    connection_url = get_connection_url(db_type, username, password, host, port, database)
    if connection_url:
        connectDatabaseFromURL(connection_url)
        # Save connection info to JSON
        connection_info = {
            "db_type": db_type,
            "username": username,
            "port": port,
            "host": host,
            "password": password,
            "database": database
        }
        st.session_state.db_connection_info = connection_info
        save_connection_info(connection_info)
    else:
        st.error("Unsupported database type")

# Load connection info when the app starts
if "db_connection_info" not in st.session_state:
    saved_info = load_connection_info()
    if saved_info:
        st.session_state.db_connection_info = saved_info
    else:
        st.session_state.db_connection_info = {
            "username": "root",
            "port": "3306",
            "host": "localhost",
            "password": "",
            "database": "rag_test"
        }

def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to the database"

def getDatabaseSchema():
    return st.session_state.db.get_table_info() if st.session_state.db else "Please connect to the database"

llm = ChatOllama(model="llama3")

def getQueryFromLLM(question):
    template = """..."""  # Your template for SQL generation
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema()
    })
    return response.content

def getResponseForQueryResult(question, query, result):
    template2 = """..."""  # Your template for generating responses
    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2 | llm
    response = chain2.invoke({
        "question": question,
        "schema": getDatabaseSchema(),
        "query": query,
        "result": result
    })
    return response.content

st.set_page_config(
    page_icon="🤖",
    page_title="Chat with Database",
    layout="centered"
)

question = st.chat_input('Chat with your database')

if "chat" not in st.session_state:
    st.session_state.chat = []

if question:
    if "db" not in st.session_state:
        st.error('Please connect to the database first.')
    else:
        st.session_state.chat.append({"role": "user", "content": question})
        query = getQueryFromLLM(question)
        result = runQuery(query)
        response = getResponseForQueryResult(question, query, result)
        st.session_state.chat.append({"role": "assistant", "content": response})

for chat in st.session_state.chat:
    st.chat_message(chat['role']).markdown(chat['content'])

# Sidebar for Database connection
with st.sidebar:
    st.title('Connect to Database')
    
    # Option to choose between URL or separate fields
    connect_type = st.radio("Connection Method", ["Connection URL", "Individual Components"])

    if connect_type == "Connection URL":
        db_url = st.text_input("Database URL", placeholder="Enter your full database connection URL")
        connectBtn = st.button("Connect via URL")
        if connectBtn and db_url:
            connectDatabaseFromURL(db_url)

    else:
        # Database type selection
        db_type = st.selectbox("Database Type", ["MySQL", "PostgreSQL", "Oracle"], 
                               index=["MySQL", "PostgreSQL", "Oracle"].index(st.session_state.db_connection_info["db_type"]))
        # Fields for individual components
        host = st.text_input(label="Host", value=st.session_state.db_connection_info["host"])
        port = st.text_input(label="Port", value=st.session_state.db_connection_info["port"])
        username = st.text_input(label="Username", value=st.session_state.db_connection_info["username"])
        password = st.text_input(label="Password", value=st.session_state.db_connection_info["password"], type="password")
        database = st.text_input(label="Database", value=st.session_state.db_connection_info["database"])

        connectBtn = st.button("Connect")
        if connectBtn:
            connectDatabase(db_type, username, port, host, password, database)
            st.success(f"Connected to {db_type} database")
