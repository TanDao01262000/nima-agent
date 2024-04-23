# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Type, Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import ToolException
from imdb import Cinemagoer

# fetch data for movies from imdb and store in an csv
def fetch_movie_info(movie_name: str) -> str:
    cine = Cinemagoer()
    movie_id = cine.search_movie(movie_name)[0].movieID
    movie = cine.get_movie(movie_id)
    
    info_keys =['localized title', 'cast', 'genres', 'runtimes', 'countries', 'plot'
    'box office', 'certificates', 'original air date', 'synopsis', 'rating', 'votes', 'cover url', 'imdbID', 'videos', 'languages',
  'title', 'year', 'kind', 'original title', 'director', 'writer', 'producer', 'composer', 'production companies', 'distributors']
    
    try:
      res = ""
      for key in info_keys:
          info_str = ""
          info_set = movie.get(key)
          if isinstance(info_set, list):
            for i, info in enumerate(info_set[:5]):
              info_str += f"{str(info)}"
              if i != min(len(info_set)-1,4):
                info_str += ", "


          elif isinstance(info_set, dict):
             for key, value in info_set.items():
              info_str += f"{key}: {str(value)}, "

          else:
             info_str =  str(info_set)
          res += f"{key.upper()}: {info_str}./n "

      return res    
    except:
        raise  ValueError("Failed to get information about the movie")
    

class MovieFetchInput(BaseModel):
    movie_name: str = Field(description="the name of a movie to fetch")

class IMDBFetchTool(BaseTool):
    name = 'imdb_movie_fetch'
    description = 'Useful for when you give any information about a particular movie'
    args_schema: Type[BaseModel] = MovieFetchInput


    def _run(
        self, query: str,  run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return fetch_movie_info(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        return fetch_movie_info(query)
    
    def _handle_error(error: ToolException) -> str:
        return (
            "The following errors occurred during tool execution:"
            + error.args[0]
            + "Please try another tool."
        )
    


if __name__ == "__main__":
    test_tool = IMDBFetchTool()
    print(test_tool.run(tool_input='The Shawshank Redemption'))