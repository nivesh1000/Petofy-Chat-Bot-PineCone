import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.pathmaker import env_path


# Load environment variables from the .env file
env_path = env_path()
load_dotenv(env_path)


def client_env():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    return client