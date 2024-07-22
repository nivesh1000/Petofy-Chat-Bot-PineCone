from pinecone import Pinecone
import json
from dotenv import load_dotenv, find_dotenv
from src.pathmaker import env_path

env_path = find_dotenv("config/.env")
load_dotenv(env_path)

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key )
index = pc.Index("web-scrap-index")

with open('vector1_data_for_pinecone.json', 'r') as f:
    vectors = json.load(f)

index.upsert(
    vectors,
    namespace= "ns1"
)
