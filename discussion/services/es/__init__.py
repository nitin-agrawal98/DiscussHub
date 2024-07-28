from elasticsearch import Elasticsearch

from config_parser.config import config

es = Elasticsearch(config['es']['url'])
