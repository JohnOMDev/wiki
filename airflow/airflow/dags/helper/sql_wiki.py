class SqlQueries:
    create_wikipedia_article = ("""
    CREATE TABLE IF NOT EXISTS {} (

             id                             DECIMAL(20,0)   NOT NULL
             ,title                         VARCHAR(50) NOT NULL
             ,description                   VARCHAR(250)
             ,url                           VARCHAR(250)
             ,article                       VARCHAR
             , PRIMARY KEY (id)
             );

            """)

#####################################################################
#####################################################################

    insert_data = ("""
         INSERT INTO {} (
                    id
                    , title
                    , description
                    , url
                    , article
                    ) VALUES(%s, %s, %s, %s, %s);
 """)

#####################################################################
#####################################################################

    drop_table = ("""
        DROP TABLE IF EXISTS {}
  """)
