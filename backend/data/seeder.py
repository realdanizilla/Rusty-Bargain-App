import subprocess
import psycopg2
import time
from logging_config import setup_logging


logger = setup_logging()

# Database connection details
DB_HOST = "host.docker.internal"
DB_PORT = "55432"
DB_NAME = "rusty_bargain"
DB_USER = "user"
DB_PASSWORD = "password"
SQL_FILE_PATH = "raw_car_data.sql"

def run_generate_sql_script():
    """Run the script to generate the .sql file.
    """
    try:
        logger.info("Running raw_data_loader.py to create the .sql file...")
        print("Running raw_data_loader.py to create the .sql file...")
        subprocess.run(["python", "data/raw_data_loader.py"], check=True, capture_output=True, text=True)
        logger.info(".sql file generated successfully")
        print(".sql file generated successfully")
    except subprocess.CalledProcessError as e:
        logger.error("Failed to run raw_data_loader.py: {e.stderr}")
        print(f"Failed to run raw_data_loader.py: {e.stderr}")
        raise

def execute_sql_file():
    """Run the .sql file to populate the database."""
    try:
        logger.info("Seeding the database...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        with open(SQL_FILE_PATH, "r") as f:
            cursor.execute(f.read())
        conn.commit()
        print("Database seeded successfully.")
        cursor.close()
        conn.close()
        logger.info("Database seeded successfully.")
    except Exception as e:
        logger.error("Failed to seed the database: {e}")
        print(f"Failed to seed the database: {e}")

def wait_for_table():
    """Wait until the target table is created by SQLAlchemy."""
    while True:
        try:
            logger.info("Checking if the table exists...")
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute("SELECT to_regclass('public.bronze_car_data');")
            result = cursor.fetchone()
            if result and result[0] is not None:
                logger.info("Table exists. Proceeding with seeding.")
                print("Table exists. Proceeding with seeding.")
                cursor.close()
                conn.close()
                break
            else:
                logger.info("Waiting for the table to be created...")
                print("Waiting for the table to be created...")
        except Exception as e:
            logger.error("Database not ready: {e}")
            print(f"Database not ready: {e}")
        time.sleep(5)

if __name__ == "__main__":
    wait_for_table()
    run_generate_sql_script()
    execute_sql_file()
