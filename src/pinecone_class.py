import os
import json
from src.pathmaker import data_path, env_path
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone, ServerlessSpec
from src.client import client_env

class PineCone:
    def __init__(self) -> None:
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=self.pinecone_api_key)

    def exist_check(self,index_name):
        if index_name  in self.pc.list_indexes().names():
            return True
        else:
            return False
        
    def create_index(self,index_name):
        self.datapath=data_path
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws', 
                    region='us-east-1'
                ) 
            ) 

    def load_json(self,datapath,index_name):
        self.index_name = index_name
        self.datapath=datapath
        self.index = self.pc.Index(self.index_name)
        index_stats = self.index.describe_index_stats()
        id=index_stats['total_vector_count']
        for file_name in os.listdir(self.datapath):
            file_path = os.path.join(self.datapath, file_name)
            
            if os.path.isfile(file_path) and file_name.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for chunk in data:
                        self.vectorize_and_upsert(chunk, id)
                        id += 1

    def vectorize_and_upsert(self,data_pair, id):
        client=client_env()
        meta_data = data_pair
        chunk = data_pair['Prompt']
        vector_data = client.embeddings.create(input=chunk, model="text-embedding")
        vector = [{
            "id": str(id),
            "values": vector_data.data[0].embedding,
            "metadata": meta_data,
        }]
        print("Data insertion started.")
        self.index.upsert(vector, namespace="ns1")
        print("Data insertion completed.")


    def similarity_search(self,user_query,index_name):
        client=client_env()
        query_embedding = client.embeddings.create(input=user_query, model="text-embedding")
        index = self.pc.Index(index_name)
        similar_queries_obj = index.query(
        namespace="ns1",
        vector=query_embedding.data[0].embedding,
        top_k=5,
        include_values=False,
        include_metadata=True
        )
        return ' '.join(str(match['metadata'].get('Response')) for match in similar_queries_obj['matches'])
        
    def existing_indexes(self):
        return self.pc.list_indexes().names()    


