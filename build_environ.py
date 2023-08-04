import mysql.connector

def create_database_and_table(host: str, user: str, password: str):
    # Connect to the MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS social_sim_db")

    # Connect to the new database
    conn.close()  # Close the old connection first
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="social_sim_db"
    )
    cursor = conn.cursor()

    # Create agent_records table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS agent_records ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "agent_id VARCHAR(255), "
        "create_time TIMESTAMP, "
        "update_time TIMESTAMP, "
        "query TEXT, "
        "response TEXT"
        ")"
    )

    # Create agents table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS agents ("
        "agent_id VARCHAR(255) PRIMARY KEY, "
        "category VARCHAR(255), "
        "mission TEXT, "
        "relations TEXT"
        ")"
    )

    # Close the connection
    conn.close()

# Use the function
create_database_and_table("localhost", "username", "password")
