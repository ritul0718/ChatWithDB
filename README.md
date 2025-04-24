
🤖 Chat with Database - Streamlit App
Welcome to Chat with Database, a simple and interactive Streamlit app that lets you ask questions in natural language and interact with your database directly! With the help of Langchain and ChatOllama, the app turns your questions into SQL queries, runs them against a database, and shows you the results—all in one interface.

✨ Features
Natural Language Interface: Just type your question, and the app will translate it into an SQL query and fetch the data from the connected database.
Multiple Database Support: You can connect to MySQL, PostgreSQL, and Oracle databases.
Flexible Connection Options:
Enter the full Connection URL.
Or input individual database connection details like host, port, username, etc.
Dynamic Querying: Powered by Langchain’s ChatOllama model, which automatically generates SQL queries based on the database schema.

🛠️ Technologies
Streamlit: For building the interactive web interface.
Langchain & ChatOllama: For natural language processing and SQL generation.
SQLAlchemy: To handle database connections and run SQL queries.

📋 Requirements
Before you begin, ensure you have the following installed:

Python 3.8+
Streamlit
Langchain (with ChatOllama model)
SQLAlchemy
Database Drivers: Depending on your database type, you may need:
MySQL: mysql-connector-python
PostgreSQL: psycopg2
Oracle: cx_Oracle

## Setup Instructions

### Prerequisites

- Python 3.8+
- The following Python libraries:
  - `streamlit`
  - `json`
  - `os`
  - `langchain_community`
  - `langchain_core`
  - Database drivers for your chosen database (e.g., `mysql-connector-python`, `psycopg2`, `cx_Oracle`)

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/chat-with-database.git
    cd chat-with-database
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the database drivers for the database you're connecting to:

    - For MySQL:
    
      ```bash
      pip install mysql-connector-python
      ```

    - For PostgreSQL:

      ```bash
      pip install psycopg2
      ```

    - For Oracle:

      ```bash
      pip install cx_Oracle
      ```

4. Run the application:

    ```bash
    streamlit run app.py
    ```

### Connecting to a Database

1. **Connection via URL:**
   - Provide the full connection URL in the sidebar and click on "Connect via URL."

2. **Connection via Individual Components:**
   - Choose the database type (MySQL, PostgreSQL, or Oracle).
   - Enter the host, port, username, password, and database name in the respective fields.
   - Click on "Connect."

Once connected, you can start asking questions in natural language through the chat input, and the application will automatically generate and run SQL queries to retrieve relevant information from the database.

### Example

1. Connect to a MySQL database running on localhost:

   ```
   Host: localhost
   Port: 3306
   Username: root
   Password: your_password
   Database: rag_test
   ```

2. Ask a question like:

   ```
   "What are the top 5 customers with the highest orders?"
   ```

   The application will generate the corresponding SQL query and fetch the results from the database.

## Saving and Loading Connection Info

- The connection information is automatically saved in a `connection_info.json` file for easier reconnection in future sessions.
- The saved connection includes database type, host, port, username, password, and database name.

## Customization

- **LLM Model**: The application uses `ChatOllama` as the default LLM model. You can customize the model by modifying the following line:

    ```python
    llm = ChatOllama(model="llama3")
    ```

- **SQL Query Templates**: Customize the SQL query and result response templates by updating the `getQueryFromLLM` and `getResponseForQueryResult` functions with your desired template text.

## Acknowledgments

- This app uses the [LangChain](https://github.com/hwchase17/langchain) framework for building language model-powered applications.
- Thanks to the Streamlit team for their amazing work on the open-source web framework.
```

