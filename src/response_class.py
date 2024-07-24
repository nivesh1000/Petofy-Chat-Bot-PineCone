import os
from src.client import client_env

class Response:
    def __init__(self) -> None:
        self.client = client_env()

    def chat_completion(self,user_query,similarity_result):
        with open('src/system_prompt.txt', 'r') as file:
            base_prompt = file.read()   

        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        final_prompt = base_prompt.format(
        similarity_result=similarity_result,
        user_query=user_query
        )
        
        completion = self.client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "user", "content": final_prompt},
            ]
        )
        return completion.choices[0].message.content
