from opensearchpy import OpenSearch
from core.service import config_service
import sys

sys.path.append("")
sys.dont_write_bytecode = True

""" Configuration Import"""
config = config_service.read_config()

# Initialize the OpenSearch client
client = OpenSearch(
    hosts=[{'host': config['OPENSEARCH']['host'],
            'port': config['OPENSEARCH']['port']}]
)


def create_doc(_id, body, _index):
    client.index(index=_index, id=_id, body=body)
