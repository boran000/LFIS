
import pymysql
import os
import sys
import getpass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_mysql():
    print("MySQL Database Setup")
    print("====================")
    
    host = input("Enter MySQL host (default: localhost): ")
    root_user = input("Enter MySQL root username (default: root): ")
    root_password = getpass.getpass("Enter MySQL root password: ")
    
    db_name = input("Enter name for the SchoolHub database (default: schoolhub): ") or "schoolhub"
    db_user = input("Enter username for SchoolHub database (default: schoolhub_user): ") or "schoolhub_user"
    db_password = getpass.getpass("Enter password for SchoolHub database user: ")
    
    try:
        # Connect as root to create database and user
        conn = pymysql.connect(
            host=host,
            user=root_user,
            password=root_password
        )
        
        with conn.cursor() as cursor:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"Database '{db_name}' created successfully")
            
            # Create user and grant privileges
            cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%'")
            cursor.execute("FLUSH PRIVILEGES")
            logger.info(f"User '{db_user}' created with privileges on '{db_name}'")
        
        conn.close()
        
        # Update config.py with new settings
        with open('config.py', 'r') as file:
            config_content = file.read()
        
        # Replace default values
        config_content = config_content.replace("DB_USERNAME = os.environ.get('DB_USERNAME', 'username')", 
                                              f"DB_USERNAME = os.environ.get('DB_USERNAME', '{db_user}')")
        config_content = config_content.replace("DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')", 
                                              f"DB_PASSWORD = os.environ.get('DB_PASSWORD', '{db_password}')")
        config_content = config_content.replace("DB_HOST = os.environ.get('DB_HOST', 'localhost')", 
                                              f"DB_HOST = os.environ.get('DB_HOST', '{host}')")
        config_content = config_content.replace("DB_NAME = os.environ.get('DB_NAME', 'schoolhub')", 
                                              f"DB_NAME = os.environ.get('DB_NAME', '{db_name}')")
        
        with open('config.py', 'w') as file:
            file.write(config_content)
        
        logger.info("Configuration updated successfully")
        logger.info("MySQL setup completed successfully!")
        
        print("\nNext steps:")
        print("1. Run 'python migrate_to_mysql.py' to migrate your data from SQLite to MySQL")
        print("2. Run your application with 'python main.py' to test the MySQL connection")
        
    except pymysql.MySQLError as e:
        logger.error(f"MySQL Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_mysql()
