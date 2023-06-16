from os import environ

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
OPENAI_API_KEY = "sk-mbpiinYwQgyz9l8OQGPiT3BlbkFJyiCDkjZG44SdReyxAm9As"

## Set up environment variables
environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter

# Use the WebBaseLoader to load specified web pages into documents
loader = WebBaseLoader([
    "https://milvus.io/docs/overview.md",
])

docs = loader.load()

# Split the documents into smaller chunks
text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
docs = text_splitter.split_documents(docs)

# Set up an embedding model to covert document chunks into vector embeddings.
embeddings = OpenAIEmbeddings(model="ada")

# Set up a vector store used to save the vector embeddings. Here we use Milvus as the vector store.
vector_store = Milvus.from_documents(
    docs,
    embedding=embeddings,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
)

query = "What is milvus?"
docs = vector_store.similarity_search(query)

print(docs)

from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI

chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="map_reduce", return_intermediate_steps=True)
query = "What is Milvus?"
chain({"input_documents": docs, "question": query}, return_only_outputs=True)

