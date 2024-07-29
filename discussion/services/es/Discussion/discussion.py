from services.es import es, ES
from services.es.Discussion.constants import DISCUSSION_INDEX, DEFAULT_SEARCH_SIZE


class DiscussionES(ES):
    def index(self, discussion):
        discussion_json = discussion.serialise()
        discussion_json['hashtags'] = [ht.tag for ht in discussion.hashtags]
        discussion_json['comments'] = [c.text for c in discussion.comments]
        es.index(index=DISCUSSION_INDEX, id=discussion.id, document=discussion_json)

    def search(self, obj):
        must_clauses = []
        query_text = obj.get('query_text', None)
        if query_text:
            must_clauses.append({
                "match": {
                    "text": query_text
                }
            })

        hashtags = obj.get('hashtags', None)
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

    def delete_index(self, discussion):
        es.delete(index=DISCUSSION_INDEX, id=discussion.id)


discussionES = DiscussionES()
