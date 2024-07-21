from pinecone import Pinecone
import json

pc = Pinecone(api_key="3b40a01e-51af-4ebc-bf71-fe1e7104fa08")
index = pc.Index("web-scrap-index")

with open('vector1_data_for_pinecone.json', 'r') as f:
    vectors = json.load(f)

index.upsert(
    vectors,
    namespace= "ns1"
)
