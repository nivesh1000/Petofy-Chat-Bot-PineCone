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


from pinecone.grpc import PineconeGRPC as Pinecone
from src.client import client_env

client = client_env()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("web-scrap-index")
# from src.pinecone_upsert import index

print('''Hello! 👋\nI'm here to assist you with your queries related to Petofy.
You can ask me anything, and I'll do my best to help.
To end your session at any time, simply type "exit".
How can I assist you today?''')
query=""
while(query!='exit'):
    query=input("Query: ")

    if query.lower() == "exit":
        break
    query_embedding=client.embeddings.create(input=query, model="text-embedding")



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

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    print(completion.choices[0].message.content)

print("Your session has ended. Thank you and goodbye! 👋")