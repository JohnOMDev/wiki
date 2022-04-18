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

def wiki(**kwargs):
    """We want to be able to extract article for a provided keyword on Wikipedia"""
    LOG.info(kwargs)
    try:
        keyword =  kwargs.get("keyword")
        limit =  kwargs.get("limit")
        if limit and isinstance(int(limit), int):
            df = wiki_client.export_raw_data_to_db(keyword, limit)
        else:
            df = wiki_client.export_raw_data_to_db(keyword)
        selected_col = ['id', 'title', 'description', 'url', 'article']
        config = configparser.ConfigParser()
        config.read('./db.cfg')
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['db'].values()))
        cur = conn.cursor()
        wiki_client.insert_statement(cur, df, selected_col)
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
