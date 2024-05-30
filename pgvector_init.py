from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

#to-do
# CSV Loader
# 



# embeding
embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"

# get current device
device = 'cpu'

# init embed model
embed = HuggingFaceEmbeddings(model_name=embed_model_name,\
                                       model_kwargs={"device":device},\
                                       encode_kwargs={"device":device,\
                                       "batch_size":200})



CONNECTION_STRING = "postgresql+psycopg2://postgres:Whatever123:)@localhost:5432/vectorDB_test"
COLLECTION_NAME = 'tan_contract_vector'