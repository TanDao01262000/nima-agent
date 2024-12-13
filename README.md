# NIMA REST API
 
## NowIMovieAnytime (NIMA)

NIMA is an agentic AI chatbot specializing in movies and related topics. It can not only answer any question within its domain but also engage in extended conversations and provide real-time news updates to users.

## Team NIMA

We are a passionate team of four software engineering students from San Jose State University (SJSU):

1. [Quyen Nguyen](https://github.com/Q1412)
2. [Michael Kao](https://github.com/mkao823) 
3. [Do Tran](https://github.com/nhutdh1103) 
4. [Tan Dao](https://github.com/TanDao01262000)

## Table of Contents

- [NIMA](#NowIMovieAnytime(NIMA))
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [Built With](#built-with)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Contact](#contact)
  - [License](#license)
## About the Project

Do you ever spend a huge amout of time on the internet to just find a movie for you or your family and end up watching nothing? If so, **NIMA** is a solution for you!

**NIMA** is your assistant which can answer any of your question about movie or relating topics such as what movie to watch, awards winners, or even asking about a movie's detail or stats from IMDB.

With **NIMA**, you do more than just asking a question, but you also having a lon conversation with it as two people.

**NIMA** can give you detailed answer, with high accuraccy by using the real time data, large size external movie database from IMDB.

### Built With
- [Python](https://www.python.org/): Programming Language
- [FastAPI](https://fastapi.tiangolo.com/): Platform for building RESTAPI  
- [Langchain](https://www.langchain.com/): Framework used to build application using Large Language Model (LLM)
- [Pinecone](https://www.pinecone.io/): Cloud-based vector database
- [OpenAI GPT-4o-mini](https://openai.com/): Large Language Model (LLM) 


## Getting Started

### Prerequisites

- Python version [3.10](https://www.python.org/downloads/release/python-310/) or higher

### API Keys

Make sure to create a .env file in your project directory and include the following environment variables:

- PINECONE_ENVIRONMENT = "gcp-starter"
- PINECONE_API_KEY = "ca3a0a0a-657a-444e-9064-5743aba25a41"
- PINECONE_API_KEY_1 = "e58475c9-55d6-4b5c-a243-b6fb11d368e9"
- PINECONE_API_KEY_2 = "pcsk_48LYgw_RaWN4cJtswG6iFuDBpRXtX5m1Lf2zypVDiAY1dhS7pMMx1KHTnQGzkcRpQyuBqp"
  
- LANGCHAIN_ENDPOINT = "<YOUR_LANGCHAIN_ENDPOINT>"
- LANGCHAIN_API_KEY = "<YOUR_LANGCHAIN_API_KEY>"
- OPENAI_API_KEY = "<YOUR_OPENAI_API_KEY>"
- HUGGINGFACE_READ_TOKEN = "<YOUR_HUGGINGFACE_READ_TOKEN>"
- SERPER_API_KEY = "<YOUR_SERPER_API_KEY>"
- REDIS_URL = "<YOUR_REDIS_URL>"


### Installation

1. Clone the repo

  ```sh
   git clone https://github.com/TanDao01262000/nima-agent.git
  ```


2. (Optional) Create a virtual environment

Install and create virtual environment
  ```sh
    pip install virtualenv
    virtualenv venv
  ```

Activate created environment

For Mac & Linux: 
  ``` sh
    source venv/bin/activate 
  ```

For Window:
  ``` sh
    venv/Scripts/activate 
  ```

3. Install dependencies

  
  Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   **Note**: Make sure that your current folder include the requirements.txt file

4. Run the application:
   ```sh
   python nima_agent.py
   ```

   The API will run on port 8000


### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Contact

  - Quyen Nguyen: quyennln1412@gmail.com
  - Michael Kao: michael.kao@sjsu.edu
  - Do Tran: dohoangnhu.tran@sjsu.edu
  - Tan Dao: tankhanhdao@gmail.com


