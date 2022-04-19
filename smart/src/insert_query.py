# -*- coding: utf-8 -*-

#####################################################################
class SqlQueries:
    insert_data = ("""
         INSERT INTO {} (
                    id
                    , title
                    , description
                    , article
                    ) VALUES(%s, %s, %s, %s);
 """)

#####################################################################
