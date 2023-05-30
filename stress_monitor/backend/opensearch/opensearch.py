from opensearchpy import OpenSearch
import sys

sys.path.append("")
sys.dont_write_bytecode = True

""" Configuration Import"""
from backend import read_config
config = read_config()

# Initialize the OpenSearch client
client = OpenSearch(
    hosts=[{'host': config['OPENSEARCH']['host'],
            'port': config['OPENSEARCH']['port']}]
)


def create_doc(_id, body, _index):
    client.index(index=_index, id=_id, body=body)
