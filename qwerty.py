from src.pinecone_class import PineCone

obj=PineCone()
sim=obj.similarity_search("describe petofy","petofy-chunk-index")
print(sim)