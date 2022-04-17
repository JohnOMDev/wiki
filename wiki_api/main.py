#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 16 22:56:35 2022

@author: johnomole
"""
import logging
import os
import click
import sys
import psycopg2
import configparser
import pandas as pd
from src.app import WIKIMEDIA
from helper.sql_wiki import SqlQueries
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("WIKI API")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

##############################################################################
LOG.info("init parameters")
#Initialize wikipedia API client
wiki_client = WIKIMEDIA()
#############################################################################

@click.group()
@click.version_option("1.0.0")
def main():
    """Search through WIKIMEDIA API for ARTICLE"""
    pass


@main.command()
@click.argument('keyword', nargs=1)
@click.option('--limit', type=int, help = "provide the limit for the output")

def export_raw_data_to_db(keyword, limit=10):
    data_search = wiki_client.search_keywords(keyword, limit)
    data = list()
    try:
        for row in data_search['pages']:
            #row=data_search['pages'][0]
            key = row.get("title")
            id_ = str(row["id"])
            data_article = wiki_client.extract_article(key)
            html = data_article["query"]["pages"][id_]["extract"]
            data_clean = wiki_client.extract_clean_description(html)
            row["article"]=data_clean
            data.append(row)
        df = pd.DataFrame(data)
    except Exception as e:
        LOG.error(e)
    return df

def insert_statement(cur, df, selected_col):
    # df_data = df[selected_col]
    for i in df.index:
        #i=0
        row = df['thumbnail'][i]
        if row is not None and 'url' in row:
            df['uri'] = row['url']
        else:
            df['url'] = ''
        wiki_data = list(df[selected_col].values)
        cur.execute(SqlQueries.insert_data, wiki_data)


def wiki(**kwargs):
    """We want to be able to extract article for a provided keyword on Wikipedia"""
    LOG.info(kwargs)
    error={}
    try:
        keyword =  kwargs.get("keyword")
        limit =  kwargs.get("limit")
        if limit and isinstance(int(limit), int):
            df = export_raw_data_to_db(keyword, limit)
        else:
            df = export_raw_data_to_db(keyword)
        selected_col = ['id', 'title', 'description', 'url', 'article']
        config = configparser.ConfigParser()
        config.read('db.cfg')
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['db'].values()))
        cur = conn.cursor()
        insert_statement(cur, df, selected_col)
        conn.close()
        return
    except Exception as e:
        LOG.error(f"Problem with the command: {e} ")

if __name__ == '__main__':
    try:
        args = sys.argv
        if "--help" in args or len(args) == 1:
            print(args)
        main()
    except Exception as e:
        logging.exception(e)
