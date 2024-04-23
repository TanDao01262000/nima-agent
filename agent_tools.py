from langchain.tools.retriever import create_retriever_tool
from langchain_pinecone import Pinecone
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities import GoogleSerperAPIWrapper
from rag_movie import init_movie_rag
from decouple import config 


#Retriever Tools
def init_nima_retriever_tool(vectorstore: Pinecone, name: str, description: str) -> Tool:
    retriever_tool = create_retriever_tool(retriever=vectorstore.as_retriever(),
                                           name=name,
                                           description=description
                                           )
    return retriever_tool 

# Wiki Search Tool
def init_wiki_searh_tool(name: str, description: str) -> Tool:
    
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    wiki_search_tool = Tool(
        name=name,
        func=wikipedia.run,
        description=description,
    )

    return wiki_search_tool


# Google Search
def init_google_search_tool(name: str, description: str) -> Tool:
    google_search = GoogleSerperAPIWrapper(serper_api_key=config("SERPER_API_KEY"))
    google_search_tool =  Tool(
        name=name,
        func=google_search.run,
        description=description,
        #    description="Useful for all situations,especially when user asks for new information.",
        )
    return google_search_tool


# RAG Movie Recommendation Tool
def init_rag_movie_recommend_tool(llm: ChatOpenAI, vectorstore: Pinecone, name: str, description: str) -> Tool:
    # Initialize RAG pipelines
    movie_recommendation_pipeline = init_movie_rag(llm=llm,
                                                    vectorstore=vectorstore)
    
    movie_rag_recommendation_tool = Tool(func=movie_recommendation_pipeline.invoke,
                                     name=name,
                                     description=description)
    return movie_rag_recommendation_tool

