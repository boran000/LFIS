import os
import logging
from app import app, db
import pymysql
import sqlite3
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mysql_database():
    try:
        # Connect to MySQL server without specifying a database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS schoolhub")
        logger.info("MySQL database created or already exists")

        conn.close()
    except Exception as e:
        logger.error(f"Error creating MySQL database: {e}")
        raise


def migrate_data():
    with app.app_context():
        try:
            # Create all tables in MySQL
            db.create_all()
            logger.info("MySQL tables created successfully")

            # Connect to SQLite database
            sqlite_db_path = os.path.join(app.instance_path, 'schoolhub.db')
            if not os.path.exists(sqlite_db_path):
                logger.error(f"SQLite database not found at {sqlite_db_path}")
                return

            sqlite_conn = sqlite3.connect(sqlite_db_path)
            sqlite_conn.row_factory = sqlite3.Row
            sqlite_cursor = sqlite_conn.cursor()

            # Get all tables from SQLite
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = sqlite_cursor.fetchall()

            # Migrate data table by table
            for table in tables:
                table_name = table[0]
                if table_name == 'sqlite_sequence':
                    continue

                logger.info(f"Migrating data from table: {table_name}")

                # Get table columns
                sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = sqlite_cursor.fetchall()
                column_names = [col[1] for col in columns]

                # Get data from SQLite
                sqlite_cursor.execute(f"SELECT * FROM {table_name}")
                rows = sqlite_cursor.fetchall()

                if not rows:
                    logger.info(f"No data to migrate for table {table_name}")
                    continue

                # Insert data into MySQL
                for row in rows:
                    # Convert row to dictionary
                    row_dict = {column_names[i]: row[i] for i in range(len(column_names))}

                    # Build INSERT statement
                    columns_str = ', '.join(f"`{col}`" for col in row_dict.keys())
                    placeholders = ', '.join(['%s'] * len(row_dict))

                    # Execute insert using SQLAlchemy
                    insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                    # Convert to a dictionary for SQLAlchemy parameterized query
                    params = {}
                    for i, key in enumerate(row_dict.keys()):
                        params[f"p{i}"] = row_dict[key]

                    # Replace placeholders with named parameters
                    named_placeholders = ', '.join([f":p{i}" for i in range(len(row_dict))])
                    named_insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({named_placeholders})"
                    db.session.execute(text(named_insert_sql), params)

                db.session.commit()
                logger.info(f"Data migration completed for table {table_name}")

            sqlite_conn.close()
            logger.info("All data successfully migrated from SQLite to MySQL")

        except Exception as e:
            logger.error(f"Error migrating data: {e}")
            db.session.rollback()


if __name__ == "__main__":
    try:
        create_mysql_database()
        migrate_data()
        logger.info("Migration from SQLite to MySQL completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
