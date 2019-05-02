from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch()

for index in es.indices.get('*'):
  print(index)

res = es.get(index="tweets", doc_type='tweet_table', id =1123765868507406338)
print(res['_source'])

res = es.search(index="tweets", body={"size":1000,"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print(hit["_source"])
