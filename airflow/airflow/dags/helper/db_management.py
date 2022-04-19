import psycopg2
import configparser
from sql_wiki import SqlQueries

config = configparser.ConfigParser()
config.read('db.cfg')


class DataManagement:
    def __init__(self, defaultdb, newdb):
        self.defaultdb = defaultdb
        self.newdb = newdb


    def create_database(self):
        """
        Returns
        -------
        cur : TYPE
            DESCRIPTION.
        conn : TYPE
        - Creates and connects tothe db
        - Returns the connection and cursor to db
        """
    
        # connect to default database
        conn = psycopg2.connect(self.defaultdb)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
    
        # create database with UTF8 encoding
        cur.execute("DROP DATABASE IF EXISTS freenow WITH (FORCE)")

        cur.execute("CREATE DATABASE freenow WITH ENCODING 'utf8' TEMPLATE template0")

    
        # close connection to default database
        conn.close()
    
        # connect to database
        self.conn = psycopg2.connect(self.newdb)
        self.cur = self.conn.cursor()
    
        return self.cur, self.conn
    
    
    def drop_tables(self):
        """
        Parameters
        ----------
        cur : TYPE
            DESCRIPTION.
        conn : TYPE
            DESCRIPTION.
        Returns
        -------
        Drops table using the queries `drop_table`.
        """
        query = SqlQueries.drop_table.format("wiki")
        self.cur.execute(query)
        self.conn.commit()

    
    def create_tables(self):
        """
        Parameters
        ----------
        cur : TYPE
        conn : TYPE
        Returns
        -------
        Creates table using the queries `create_wikipedia_article`.
        """
        query = SqlQueries.create_wikipedia_article.format("wiki")
        self.cur.execute(query)
        self.conn.commit()


    def main(self):
        """
        Returns
        -------
        - Drops (if exists) and Creates the database.
        - Establishes connection with the database and gets
        cursor to it.
        - Drops the tables.
        - Creates tables needed.
        - Finally, closes the connection.
        """
        self.create_database()
    
        self.drop_tables()
        self.create_tables()
    
        self.conn.close()


# if __name__ == "__main__":
#     main()
