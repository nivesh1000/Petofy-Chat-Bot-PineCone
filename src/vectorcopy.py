import json
from loader import load_json
from client import client_env

client = client_env()
combined_data = load_json()
# print(combined_data[0:len(combined_data)])
vectors = []


def generate_embeddings():

    index = 0
    for c in combined_data:
        chunk=c['Prompt']
        # print(chunk)
        vector_data = client.embeddings.create(input=chunk, model="text-embedding")
        vectors.append(
            {
                "id": str(index),
                "values": vector_data.data[0].embedding,
                "metadata": c,
            }
        )
        index += 1

    with open("vector1_data_for_pinecone.json", "w") as json_file:
        json.dump(vectors, json_file)


generate_embeddings()
