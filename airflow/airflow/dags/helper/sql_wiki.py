class SqlQueries:
    create_wikipedia_article = ("""
    CREATE TABLE IF NOT EXISTS {} (

             id                             DECIMAL(20,0)   NOT NULL
             ,title                         VARCHAR(50) NOT NULL
             ,description                   VARCHAR(250)
             ,article                       VARCHAR
             , PRIMARY KEY (id)
             );

            """)

#####################################################################
#####################################################################

    drop_table = ("""
        DROP TABLE IF EXISTS {}
  """)


    word_occurence = (
    """ CREATE TABLE {} AS (
            SELECT word, count(*)
            FROM (
              SELECT regexp_split_to_table(article, '\s') as word
              FROM wiki
            ) t
            GROUP BY word
);
    """
    )
