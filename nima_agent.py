from langchain_openai import ChatOpenAI
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from pinecone import Pinecone as P
from langchain_pinecone import Pinecone
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from decouple import config
from pydantic import BaseModel
from template import react_agent_template
from agent_tools import init_nima_retriever_tool, init_wiki_searh_tool, init_google_search_tool, init_rag_movie_recommend_tool
from imdb_custom_tool import IMDBFetchTool
from embed_model import init_embed_model
from langchain.memory import ConversationBufferMemory
from redisvl.extensions.llmcache import SemanticCache
from fastapi import FastAPI, HTTPException,  status,Body    
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import time
from functools import wraps
import uvicorn
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "NimaAgent"
os.environ["LANGCHAIN_API_KEY"] = config("LANGCHAIN_API_KEY")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM chat model
llm = ChatOpenAI(model="gpt-4o-mini",
                 temperature=0.3,
                 openai_api_key=config("OPENAI_API_KEY"))

# Add cache to reduce the load of work and increase the performance
set_llm_cache(InMemoryCache())

# Embedding Model 
model_id = "sentence-transformers/all-MiniLM-L6-v2"
device = 'cpu'
embed = init_embed_model(model_id=model_id, device=device)


# Vectorstore 
api_key = config("PINECONE_API_KEY")
pc = P(api_key=api_key)
index_name = "nima"
index = pc.Index(index_name)
vectorstore = Pinecone(
    index, embed, "text" 
)

# New Movie Dataset
api_key_new = config("PINECONE_API_KEY_2")
pc = P(api_key=api_key_new)
index_name_new = "nima1"
index = pc.Index(index_name_new)
vectorstore_new = Pinecone(
    index, embed, "text" 
)


# about-me client for Nima's information rag
api_key_about_me = config("PINECONE_API_KEY_1")
pc_about_me = P(api_key=api_key_about_me)
index_name_1 = "nima-information"
index_about_me = pc_about_me.Index(index_name_1)
vectorstore_about_me = Pinecone(
    index_about_me, embed, "information"
)

# Tools
# retriever tool all info about Nima
nima_retriever_tool = init_nima_retriever_tool(vectorstore=vectorstore_about_me,
                                               name="nima_retriever_tool",
                                               description="Useful for when you answer question about yourself or Nima"
                                               )

# wikipedia search tool
wiki_search_tool = init_wiki_searh_tool(name="wiki_search_tool",
                                        description="Useful for when you need to find information on wikipedia"
                                        )

# google search tool
google_search_tool = init_google_search_tool(name="google_search_tool",
                                             description="Useful for when you need to recommend new movies, or find any information relating to movies."
                                             )

# Recommendation Tools
movie_rag_recommendation_tool= init_rag_movie_recommend_tool(llm=llm,
                              vectorstore=vectorstore_new,
                              name="movie_rag_recommendation_tool",
                              description="Useful for you recommend movies, get stats from a particular movie")
# IMDB movie info fetch
imdb_info_fetch_tool = IMDBFetchTool()

# list of tools
tools = [movie_rag_recommendation_tool, google_search_tool, imdb_info_fetch_tool, wiki_search_tool,
         nima_retriever_tool ]

# Prompt used for Nima
template = react_agent_template()

#create prompt
prompt = PromptTemplate.from_template(template)

# init agent
agent = create_react_agent( llm=llm,
                            tools=tools,
                            prompt=prompt)


# Chat history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Agent executor
agent_executor = AgentExecutor(agent=agent,
                            tools=tools,
                            memory=memory,
                            verbose=True,
                            handle_parsing_errors=True,
                            early_stopping_method="force",
                            max_iterations = 3,
                            max_execution_time=100,
                        )


# LLM Semantic Cache
agentcache = SemanticCache(redis_url=config('REDIS_URL'),
                           distance_threshold=0.1
                           )
agentcache.clear()
agentcache.set_ttl(2*60*60)


def rate_limiter(max_calls: int, time_frame: int):
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper( *args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='Rate limit excceded')

            calls.append(now)
            return await func( *args, **kwargs)
        return wrapper
    return decorator


class Input(BaseModel):
    question: str
    chat_history: list

class Metadata(BaseModel):
    conversation_id: str

class Config(BaseModel):
    metadata: Metadata
    
class RequestBody(BaseModel):
    input: Input 
    config: Config

def handle_bad_response(query: str, memory: list[str]) -> str:
    ERROR_HANDLER_MESSAGE = " Please ask me again, I only slept 2 hours last night 🥹🥹🥹"
    count = 0
    while count < 3:
        answer = agent_executor.invoke({"input": query,
                                                "chat_history":memory})['output']
        if "Agent stopped due to iteration limit or time limit" in answer:
            answer = agent_executor.invoke({"input": query,
                                                "chat_history":memory})['output']
        
            count += 1
        else:
            break
    if count >= 3:
        answer = ERROR_HANDLER_MESSAGE
    return answer
        

@app.post('/nima')
@rate_limiter(max_calls=15, time_frame=60)
async def nima(query: RequestBody = Body(...)):
    try:
        query = query.input.question
        cache = agentcache.check(prompt=query)

        if cache:
            return cache[0]['response']
        else:
            with get_openai_callback() as cb:
                answer = handle_bad_response(query=query, memory=memory)
                print(cb)
                print(answer)
            if answer != " Please ask me again, I only slept 2 hours last night 🥹🥹🥹":
                agentcache.store(prompt=query, response=answer)
            return answer

    except Exception as e:
        # Handle any errors during initialization or execution
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == '__main__':
    nest_asyncio.apply()
    uvicorn.run(app, port=8000)
