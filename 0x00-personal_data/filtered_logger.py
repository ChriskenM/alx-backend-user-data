#!/usr/bin/env python3
"""
Logger module
"""
import logging
import re
import os
import mysql.connector
from typing import List

# PII_FIELDS constant at the root of the module
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated."""
    pattern = r'({})=.*?{}'.format('|'.join(fields), re.escape(separator))
    return re.sub(pattern, lambda m: m.group(0).split('=')[0] +
                  '=' + redaction + separator, message)


def get_logger() -> logging.Logger:
    """Returns a logger with redacting formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQL connection object"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    if not database:
        raise ValueError("Database name not provided in environment variable "
                         "PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """Main function that retrieves and logs user data from the database."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor:
        msg = "; ".join([f"{key}={value}" for key, value in row.items()]) + ";"
        logger.info(msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
