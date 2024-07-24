with open('src/system_prompt.txt', 'r') as file:
    sys = file.read()
    

similarity_search_data = "Petofy is a pet care service provider. They offer veterinary services and pet grooming."
user_query = "What services does Petofy offer?"

# Format the prompt with the variables
formatted_prompt = sys.format(
    similarity_search_data=similarity_search_data,
    user_query=user_query
)
print(formatted_prompt)