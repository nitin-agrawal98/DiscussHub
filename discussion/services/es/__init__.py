from abc import ABC, abstractmethod

from elasticsearch import Elasticsearch

from config_parser.config import config
from models import Discussion

es = Elasticsearch(config['es']['url'])


class ES(ABC):
    @abstractmethod
    def index(self, obj):
        pass

    @abstractmethod
    def search(self, obj):
        pass

    @abstractmethod
    def delete_index(self, obj):
        pass
