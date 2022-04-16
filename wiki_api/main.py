#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 16 22:56:35 2022

@author: johnomole
"""
import logging
import os
import time
import click
import sys
import csv
from wiki_api.src.app import WIKIMEDIA
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("WIKI API")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

##############################################################################
LOG.info("init parameters")
#############################################################################

@click.group()
@click.version_option("1.0.0")
def main():
    """Search through WIKIMEDIA API for ARTICLE"""
    pass


@main.command()
@click.argument('keyword', nargs=1)
@click.option('--limit', type=str, help = "provide the limit for the output")
@click.option('--output-format', type=str, help = "The format to export the data e.g csv")
@click.option('--output-path', type=str, help = "The path to export the data e.g desktop or document")
def beer(**kwargs):
    """We want to be able to extract article for a provided keyword on Wikipedia"""
    #Initialize wikipedia API client
    wiki_client = WIKIMEDIA()
    LOG.info(kwargs)
    error={}
    try:
        output_format = kwargs.get("output_format")
        output_path =  kwargs.get("output_path")

        keyword =  kwargs.get("keyword")
        until =  kwargs.get("until")
        if until and isintance(until, int):
            data = wiki_client.search_keywords(keyword, until)
        else:
            data = wiki_client.search_keywords(keyword)
        if output_format.lower() != 'csv':
            LOG.error("We only support 'CSV' as output format at the moment, but you indicate 'output_format' ")
            return

        if output_format is None or output_path is None:
            pass

        else:
            LOG.info("The code below will save the data as CSV in your root directory")
            path =os.getcwd() + '/data'
            filepath = path + "\\" + output_path
            with open(filepath, 'w', encoding='utf8', newline='') as csv_file:
                fc = csv.DictWriter(csv_file,
                                    fieldnames=data[0].keys(),

                                   )
                fc.writeheader()
                fc.writerows(data)
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
