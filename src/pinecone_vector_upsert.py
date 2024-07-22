import os
import json
from pathmaker import data_path, env_path
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone

dataset_path = data_path()

env_path = find_dotenv("config/.env")
load_dotenv(env_path)

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key )
index = pc.Index("petofy-chunk-index")

from client import client_env

client = client_env()

def vectorize_and_upsert(data_pair,id):
    meta_data=data_pair
    chunk=data_pair['Prompt']
    vector_data = client.embeddings.create(input=chunk, model="text-embedding")
    vector=[{
        "id": str(id),
        "values": vector_data.data[0].embedding,
        "metadata": meta_data,
        }]
    index.upsert(
    vector,
    namespace= "ns1"
    )    

def load_json():
    combined_data = []
    folder_path = dataset_path
    id=0
    # Traverse through the directory tree using os.walk
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as f:
                    # Load JSON data from the file
                    data = json.load(f)
                    for chunk in data:
                        vectorize_and_upsert(chunk,id)
                        id+=1
                    


load_json()




    