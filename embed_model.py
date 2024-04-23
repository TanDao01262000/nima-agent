""" Embedding Model 😤😤😤"""
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from typing import Optional


def init_embed_model(model_id: str, device: str ) -> Optional[HuggingFaceEmbeddings]:
    embed_model = HuggingFaceEmbeddings(model_name=model_id,
                                model_kwargs={"device":device},
                                encode_kwargs={"device":device,
                                                "batch_size":200}
                                    )
    return embed_model


# if __name__ == '__main__':
#     model = init_embed_model()