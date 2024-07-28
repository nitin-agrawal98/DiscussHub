from services.es import es
from services.es.Discussion.constants import DISCUSSION_INDEX, DEFAULT_SEARCH_SIZE


def index(discussion):
    discussion_json = discussion.serialise()
    discussion_json['hashtags'] = [ht.tag for ht in discussion.hashtags]
    discussion_json['comments'] = [c.text for c in discussion.comments]
    es.index(index=DISCUSSION_INDEX, id=discussion.id, document=discussion_json)


def search(query_text=None, hashtags=None):
    must_clauses = []
    if query_text:
        must_clauses.append({
            "match": {
                "text": query_text
            }
        })

    if hashtags:
        must_clauses.append({
            "terms": {
                "hashtags": hashtags
            }
        })

    search_query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        },
        "size": DEFAULT_SEARCH_SIZE
    }

    response = es.search(index=DISCUSSION_INDEX, body=search_query)
    return [data.get('_source') for data in response['hits']['hits']]


def delete_index(discussion):
    es.delete(index=DISCUSSION_INDEX, id=discussion.id)
