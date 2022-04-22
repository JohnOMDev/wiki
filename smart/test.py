"""
Performing some Pytest on the response of the API client
"""
import pandas
import pytest
from smart.src.wikimedia import WIKIMEDIA

wiki_client = WIKIMEDIA()
"""
Testing the endpoint and it's payload

"""
def test_search_keyword_endpoint():
     response = wiki_client.search_keywords(keyword = 'taxi', limit = 'john')
     assert response['httpCode'] != 200

def test_extract_keyword_endpoint():
     response = wiki_client.export_raw_data_to_db(keyword = 'taxi', limit = '10')
     assert isinstance(response, pandas.core.frame.DataFrame)
