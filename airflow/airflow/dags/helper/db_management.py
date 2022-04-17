import psycopg2
import configparser
from sql_wiki import SqlQueries

config = configparser.ConfigParser()
config.read('db.cfg')



def create_database():
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
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['db'].values()))
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS freenow")
    cur.execute("CREATE DATABASE freenow WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to database
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['freenowdb'].values()))
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
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
    cur.execute(query)
    conn.commit()


def create_tables(cur, conn):
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
    cur.execute(query)
    conn.commit()


def main():
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
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
