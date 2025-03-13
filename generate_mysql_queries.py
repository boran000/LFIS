import os
import logging
from app import app, db
from models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, MetaData, Table
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_create_tables_sql():
    """Generate SQL for creating all tables in the database."""
    try:
        output_file = 'mysql_queries.sql'
        with app.app_context():
            # Get all table names
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()

            with open(output_file, 'w') as f:
                # Write header
                f.write("-- MySQL database queries for SchoolHub\n")
                f.write(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # Create database statement
                f.write("-- Create database\n")
                f.write("CREATE DATABASE IF NOT EXISTS schoolhub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
                f.write("USE schoolhub;\n\n")

                # Get metadata
                metadata = MetaData()
                metadata.reflect(bind=db.engine)

                # Generate DROP TABLE statements first
                for table_name in table_names:
                    f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")

                f.write("\n-- Table creation statements\n\n")

                # Generate CREATE TABLE statements for each table
                for table_name in table_names:
                    logger.info(f"Generating CREATE TABLE for {table_name}")
                    table = Table(table_name, metadata, autoload_with=db.engine)

                    # Generate CREATE TABLE statements manually with DROP IF EXISTS
                    columns = []
                    for column in table.columns:
                        col_type = str(column.type)
                        # Adjust column types for MySQL
                        if 'DATETIME' in col_type:
                            col_type = 'DATETIME DEFAULT CURRENT_TIMESTAMP'
                        elif 'BOOLEAN' in col_type:
                            col_type = 'TINYINT(1)'

                        nullable = 'NULL' if column.nullable else 'NOT NULL'
                        auto_inc = 'AUTO_INCREMENT' if column.primary_key and isinstance(column.type,
                                                                                         db.Integer) else ''
                        default = f"DEFAULT '{column.default.arg}'" if column.default is not None and not callable(
                            column.default.arg) else ''

                        columns.append(f"`{column.name}` {col_type} {nullable} {auto_inc} {default}".strip())

                    # Add primary key
                    pkeys = [f"`{pk.name}`" for pk in table.primary_key.columns]
                    if pkeys:
                        columns.append(f"PRIMARY KEY ({', '.join(pkeys)})")

                    # Generate CREATE TABLE statement
                    create_stmt = f"""
CREATE TABLE `{table_name}` (
    {',\n    '.join(columns)}
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

                    # Add comments and write to file
                    f.write(f"-- Table structure for table `{table_name}`\n")
                    f.write("DROP TABLE IF EXISTS `" + table_name + "`;\n")
                    f.write(create_stmt.replace('"', '`') + "\n\n")

                # Generate sample INSERT statements for each table
                f.write("\n-- Sample INSERT statements for each table\n\n")

                for table_name in table_names:
                    # Get a few sample rows
                    table = Table(table_name, metadata, autoload_with=db.engine)
                    result = db.session.query(table).limit(5).all()

                    if result:
                        f.write(f"-- Sample data for table `{table_name}`\n")

                        # Get column names
                        columns = [column.name for column in table.columns]
                        column_str = ", ".join([f"`{col}`" for col in columns])

                        for row in result:
                            # Format values properly for SQL
                            values = []
                            for i, col in enumerate(columns):
                                value = row[i]
                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, (int, float)):
                                    values.append(str(value))
                                elif isinstance(value, datetime):
                                    values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                                elif isinstance(value, bool):
                                    values.append("1" if value else "0")
                                else:
                                    # Escape single quotes in strings
                                    val_str = str(value).replace("'", "''")
                                    values.append(f"'{val_str}'")

                            value_str = ", ".join(values)
                            f.write(f"INSERT INTO `{table_name}` ({column_str}) VALUES ({value_str});\n")

                        f.write("\n")

                # Add indexes and foreign keys
                f.write("\n-- Indexes and foreign keys\n\n")

                for table_name in table_names:
                    # Get foreign keys
                    fks = inspector.get_foreign_keys(table_name)
                    if fks:
                        f.write(f"-- Foreign keys for table `{table_name}`\n")
                        for fk in fks:
                            src_cols = ", ".join([f"`{col}`" for col in fk['constrained_columns']])
                            ref_cols = ", ".join([f"`{col}`" for col in fk['referred_columns']])
                            f.write(
                                f"ALTER TABLE `{table_name}` ADD CONSTRAINT `{fk['name'] if 'name' in fk else f'fk_{table_name}_{fk['referred_table']}'}`\n")
                            f.write(f"  FOREIGN KEY ({src_cols}) REFERENCES `{fk['referred_table']}` ({ref_cols});\n\n")

                # Add users and permissions
                f.write("\n-- Create users and permissions\n")
                f.write("-- Replace 'password' with your actual password\n")
                f.write("CREATE USER IF NOT EXISTS 'schoolhub_user'@'localhost' IDENTIFIED BY 'password';\n")
                f.write("GRANT ALL PRIVILEGES ON schoolhub.* TO 'schoolhub_user'@'localhost';\n")
                f.write("FLUSH PRIVILEGES;\n")

        logger.info(f"Successfully generated MySQL queries in {output_file}")
        return output_file
    except Exception as e:
        import traceback
        logger.error(f"Error generating MySQL queries: {str(e)}")
        logger.error(traceback.format_exc())
        return None


if __name__ == "__main__":
    output_file = generate_create_tables_sql()
    if output_file:
        print(f"MySQL queries successfully generated in {output_file}")
    else:
        print("Failed to generate MySQL queries.")
