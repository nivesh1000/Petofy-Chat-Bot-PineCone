import os
import json
from pathmaker import data_path, env_path
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone
from client import client_env

# Load the dataset path
dataset_path = data_path()

# Load environment variables from .env file
env_path = find_dotenv("config/.env")
load_dotenv(env_path)

# Initialize Pinecone API
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("petofy-chunk-index")

# Initialize the embedding client
client = client_env()

def vectorize_and_upsert(data_pair: dict, id: int) -> None:
    """
    Vectorizes the input data and upserts it into the Pinecone index.
    
    Args:
        data_pair (dict): The data to be vectorized and upserted.
        id (int): The ID of the data entry.
    """
    meta_data = data_pair
    chunk = data_pair['Prompt']
    vector_data = client.embeddings.create(input=chunk, model="text-embedding")
    vector = [{
        "id": str(id),
        "values": vector_data.data[0].embedding,
        "metadata": meta_data,
    }]
    index.upsert(vector, namespace="ns1")

def load_json(folder_path) -> None:
    """
    Loads JSON files from the dataset path, vectorizes and upserts the data.
    """
    id = 0
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            with open(file_path, 'r') as f:
                for line in f:
                    chunk = json.loads(line)
                    vectorize_and_upsert(chunk, id)
                    id += 1

