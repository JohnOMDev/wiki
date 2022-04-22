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
from smart.src.wikimedia import WIKIMEDIA
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
@click.option('--m', type=bool, help = "specify to only print the data and not export to db")
@click.option('--limit', type=int, help = "provide the limit for the output")

def wiki(**kwargs):
    """We want to be able to extract article for a provided keyword on Wikipedia"""
    LOG.info(kwargs)
    try:
        keyword =  kwargs.get("keyword")
        limit =  kwargs.get("limit")
        print_ = kwargs.get("m")
        if limit and isinstance(int(limit), int):
            df = wiki_client.export_raw_data_to_db(keyword, limit)
        else:
            df = wiki_client.export_raw_data_to_db(keyword)
        if df.get("error"):
            LOG.info(df)
            return 
        selected_col = ['id', 'title', 'description', 'article']
        df = df[selected_col]

        if not print_:
            # import the db credentials and connect to it.
            config = configparser.ConfigParser()
            config.read('smart/db.cfg')
            conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['db'].values()))
            cur = conn.cursor()
            wiki_client.insert_statement(cur, df)
            conn.commit()
            conn.close()
        else:
            LOG.info(df.to_dict('records'))
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
