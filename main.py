import os
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
from src.client import client_env
from src.pathmaker import env_path

# Load environment variables from the .env file
env_path = find_dotenv("config/.env")
load_dotenv(env_path)

service_endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_RESOURCE_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

chat_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
from pinecone.grpc import PineconeGRPC as Pinecone
from src.client import client_env

client = client_env()
query="what is pet microchip"
query_embedding=client.embeddings.create(input=query, model="text-embedding")

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("web-scrap-index")
# from src.pinecone_upsert import index

similar_queries_obj=index.query(
    namespace="ns1",
    vector=query_embedding.data[0].embedding,
    top_k=3,
    include_values=False,
    include_metadata=True
)

similar_queries=''
# print(similar_queries)
for match in similar_queries_obj['matches']:
    similar_queries+=str(match['metadata'])

# Base prompt
prompt_base = (
    "Based on the following information:"
    f"{similar_queries}"
    "Please provide a direct and concise response for the following question and if the information needed to answer the question is not present in the provided text, reply with 'Sorry, I can't answer that.'\n"
)
prompt = prompt_base + query
# print(similar_queries)

completion = chat_client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "user", "content": prompt},
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": service_endpoint,
                    "index_name": "petofy-vector-data",
                    "authentication": {
                        "type": "api_key",
                        "key": key,
                    },
                },
            }
        ],
    },
)

print(completion.choices[0].message.content)

