import requests
import logging
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from smart.src.insert_query import SqlQueries

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("PERSONIO DAG")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
class WIKIMEDIA:
    """

    """
    def __init__(self, language='en'):
        """

        Parameters
        ----------
        language : TYPE, optional
            DESCRIPTION. The default is 'en'.

        Returns
        -------
        None.

        """
        self.base_url = 'http://' + language.lower() + '.wikipedia.org/w/'

    def search_keywords(self, keyword, limit):
        """

        Parameters
        ----------
        keyword : TYPE
            DESCRIPTION.
        limit : TYPE, optional
            DESCRIPTION. The default is 10.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        url = f"{self.base_url}rest.php/v1/search/page?q={keyword}&limit={str(limit)}"
        try:
            payload={}
            headers = {

            }
            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()
        except Exception as e:
            LOG.error(e)
        return data

    def extract_article(self, keyword):
        """

        Parameters
        ----------
        keyword : TYPE
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        url = f"{self.base_url}api.php?action=query&prop=extracts&titles={keyword}&format=json"
        try:
            payload={}
            headers = {

            }

            response = requests.request("GET", url, headers=headers, data=payload)

            data = response.json()
        except Exception as e:
            LOG.error(e)
        return data

    def article_view_stats(self, keyword):
        """

        Parameters
        ----------
        keyword : TYPE
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        url = f"{self.base_url}?action=query&prop=pageviews&titles={keyword}&format=json"
        try:
            payload={}
            headers = {

            }

            response = requests.request("GET", url, headers=headers, data=payload)

            data = response.json()
        except Exception as e:
            LOG.error(e)
        return data


    def extract_clean_description(self, html):
        """

        Parameters
        ----------
        html : TYPE
            DESCRIPTION.

        Returns
        -------
        text : TYPE
            DESCRIPTION.

        """
        try:

            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
        except Exception as e:
            LOG.error(e)
        return text

    def export_raw_data_to_db(self, keyword, limit=10):
        data_search = self.search_keywords(keyword, limit)
        data = list()
        try:
            for row in data_search['pages']:
                #row=data_search['pages'][0]
                key = row.get("title")
                id_ = str(row["id"])
                data_article = self.extract_article(key)
                html = data_article["query"]["pages"][id_]["extract"]
                data_clean = self.extract_clean_description(html)
                row["article"]=data_clean
                data.append(row)
            df = pd.DataFrame(data)
        except Exception as e:
            LOG.error(e)
        return df

    def insert_statement(self, cur, df):
        """

        Parameters
        ----------
        cur : TYPE
            DESCRIPTION.
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        for i, row in df.iterrows():
            print(row)
            cur.execute(SqlQueries.insert_data.format("wiki"), list(row))
