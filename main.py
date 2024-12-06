from src.pinecone_class import PineCone
from src.response_class import Response
    
def main():
    while True:
        pine_obj = PineCone()
        chat_obj = Response()
        list_indexes = pine_obj.existing_indexes()
        print("------------------------------------------")
        print("Available indexes:")
        for i, index in enumerate(list_indexes, start=1):
            print(f"{i}. {index}")

        print("\nWhat would you like to do?")
        print("1. Add data to an existing index")
        print("2. Create a new index")
        print("3. Use model based on a specific index")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            index_name = input("Enter the name of index: ")
            if pine_obj.exist_check(index_name):
                data_path = input("Enter the path of data file: ")
                pine_obj.load_json(data_path,index_name)
                print(f"Data inserted to {index_name} successfully!")
            else:
                print("Index with this name don't exist.")    

        elif choice == '2':
            index_name = input("Enter the name of index: ")
            if pine_obj.exist_check(index_name):
                print("Index already exist.")
            else:
                pine_obj.create_index(index_name)
                print(f"{index_name} index created successfully")
                data_path = input("Enter the path of data file: ")
                pine_obj.load_json(data_path,index_name)
                print(f"Data inserted to {index_name} successfully!")

        elif choice == '3':
            index_name = input("Enter the name of Index you want the model to response with respect to: ")
            # Welcome message
            print('''Hello! 👋\nI'm here to assist you with your queries related to Petofy.
            You can ask me anything, and I'll do my best to help.
            To end your session at any time, simply type "exit".
            How can I assist you today?''')
            while True:
                user_query = input("Query: ")
                similarity_result = pine_obj.similarity_search(user_query, index_name)
                if user_query == "exit":
                    break
                print(f"Response: {chat_obj.chat_completion(user_query,similarity_result)}")
            print("Your chat session has ended.")
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
