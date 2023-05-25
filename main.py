from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

import os
from dotenv import load_dotenv
import pinecone

# Loads different API keys from .env file
load_dotenv()

#Set up your Apify API token and OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))


embeddings = OpenAIEmbeddings()

index_name = "osrs-wiki-test"

vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever(), 
                                           verbose=True, return_source_documents=True)


query = """
You are a non-player-character in the videogame Old School RuneScape.
You specialize in answering player's question using all your knowledge about the game.
If you do not know an answer, you say so, instead of coming up with a fake answer.
Here is the question you are asked:
"How are Agility Training Areas identified on the map?"
"""

chat_history = []
result = qa({"question": query, "chat_history": chat_history})

#print(result["answer"])
print(result)