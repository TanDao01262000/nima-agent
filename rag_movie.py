from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone


def rag_prompt() -> str:
    template = '''
    You are Nima. You will do your best to recommend movies based on the question and context.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    {context}

    Question: {question}
    Answer:
    '''
    prompt = PromptTemplate(
        template=template,
        input_variables=[
            'context',
            'question',
        ]
    )
    return prompt

def init_movie_rag(llm: ChatOpenAI, vectorstore: Pinecone) -> RetrievalQA:
    
    prompt = rag_prompt()
    # Initialize RAG pipelines
    rag_pipeline = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=vectorstore.as_retriever(),
                                    chain_type_kwargs={"prompt": prompt})
    return rag_pipeline