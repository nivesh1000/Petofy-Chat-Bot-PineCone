import os
import json
from dotenv import load_dotenv
from pathmaker import env_path
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)
from azure.search.documents import SearchClient

# from vector import generate_embeddings
from client import client_env

client = client_env()
# vectors = generate_embeddings()

# Load environment variables from the .env file
env_path = env_path()
load_dotenv(env_path)

service_endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_RESOURCE_KEY")


def create_index():

    credential = AzureKeyCredential(key)
    index_name = "petofy-vector-data"

    index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)

    index_fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
        SearchableField(name="text_chunk", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="demoHnswProfile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="demoHnsw",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE,
                ),
            ),
        ],
        profiles=[
            VectorSearchProfile(
                name="demoHnswProfile",
                algorithm_configuration_name="demoHnsw",
            ),
        ],
    )

    index = SearchIndex(
        name=index_name,
        fields=index_fields,
        vector_search=vector_search,
    )
    result = index_client.create_or_update_index(index)

    print(f" {result.name} created")
    # Close the search client
    index_client.close()


create_index()


def upload_to_index():
    # Reinitialize the client to interact with the newly created index
    search_client = SearchClient(
        endpoint=service_endpoint,
        index_name="petofy-vector-data",
        credential=AzureKeyCredential(key),
    )
    # Load data from JSON file
    with open("vector_data.json", "r") as json_file:
        vectors = json.load(json_file)

    # Upload the batch to the Azure Search index
    result = search_client.upload_documents(documents=vectors)
    print("Documents uploaded")

    # Close the search client
    search_client.close()


upload_to_index()
