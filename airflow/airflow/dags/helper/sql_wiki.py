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
    """
    CREATE TABLE {} AS (
        WITH word_splitting AS (
              SELECT regexp_split_to_table(article, '\s') as word
              FROM {}
        ), find_every_keyword_presence AS (
            SELECT count(*) as total
            FROM word_splitting
            WHERE lower(word) ilike '%taxi%'
        )
        SELECT {} AS keyword, total AS occurence
        FROM find_every_keyword_presence
);
    """
    )
