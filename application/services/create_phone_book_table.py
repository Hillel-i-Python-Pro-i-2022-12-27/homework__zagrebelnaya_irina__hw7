from application.services.db_connection import DBConnection


def create_phonebook_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS phone_book (
                                id INTEGER PRIMARY KEY UNIQUE,
                                contact_name TEXT NOT NULL,
                                phone_value text NOT NULL UNIQUE);"""
            )
