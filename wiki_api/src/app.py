import requests
import logging
import os

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
        self.base_url = 'http://' + language.lower() + '.wikipedia.org/w/api.php'

    def search_keywords(self, keyword, limit=10):
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
        url = f"{self.base_url}/v1/search/page?q={keyword}&limit=str{limit}"
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
        url = f"{self.base_url}?action=query&prop=extracts&titles={keyword}&format=json"
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
